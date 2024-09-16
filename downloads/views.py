import logging
from typing import Any

import requests
from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Prefetch
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, ListView, RedirectView
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
import pytz

from .models import OS, Release, ReleaseFile

logger = logging.getLogger(__name__)

class DownloadLatestPython2(RedirectView):
    """ Redirect to latest Python 2 release """
    permanent = False

    def get_redirect_url(self, **kwargs):
        try:
            latest_python2 = Release.objects.latest_python2()
        except Release.DoesNotExist:
            latest_python2 = None

        if latest_python2:
            return latest_python2.get_absolute_url()
        else:
            return reverse('download')


class DownloadLatestPython3(RedirectView):
    """ Redirect to latest Python 3 release """
    permanent = False

    def get_redirect_url(self, **kwargs):
        try:
            latest_python3 = Release.objects.latest_python3()
        except Release.DoesNotExist:
            latest_python3 = None

        if latest_python3:
            return latest_python3.get_absolute_url()
        else:
            return reverse('download')


class DownloadBase:
    """ Include latest releases in all views """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'latest_python2': Release.objects.latest_python2(),
            'latest_python3': Release.objects.latest_python3(),
        })
        return context


class DownloadHome(DownloadBase, TemplateView):
    template_name = 'downloads/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            latest_python2 = Release.objects.latest_python2()
        except Release.DoesNotExist:
            latest_python2 = None

        try:
            latest_python3 = Release.objects.latest_python3()
        except Release.DoesNotExist:
            latest_python3 = None

        python_files = []
        for o in OS.objects.all():
            data = {
                'os': o,
            }
            if latest_python2 is not None:
                data['python2'] = latest_python2.download_file_for_os(o.slug)
            if latest_python3 is not None:
                data['python3'] = latest_python3.download_file_for_os(o.slug)
            python_files.append(data)

        context.update({
            'releases': Release.objects.downloads(),
            'latest_python2': latest_python2,
            'latest_python3': latest_python3,
            'python_files': python_files,
        })

        return context


class DownloadFullOSList(DownloadBase, ListView):
    template_name = 'downloads/full_os_list.html'
    context_object_name = 'os_list'
    model = OS


class DownloadOSList(DownloadBase, DetailView):
    template_name = 'downloads/os_list.html'
    context_object_name = 'os'
    model = OS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        release_files = ReleaseFile.objects.select_related(
            'os',
        ).filter(os=self.object)
        context.update({
            'os_slug': self.object.slug,
            'releases': Release.objects.released().prefetch_related(
                Prefetch('files', queryset=release_files),
            ).order_by('-release_date'),
            'pre_releases': Release.objects.published().pre_release().prefetch_related(
                Prefetch('files', queryset=release_files),
            ).order_by('-release_date'),
        })
        return context


class DownloadReleaseDetail(DownloadBase, DetailView):
    template_name = 'downloads/release_detail.html'
    model = Release
    context_object_name = 'release'

    def get_object(self):
        try:
            return self.get_queryset().select_related().get(
                slug=self.kwargs['release_slug']
            )
        except self.model.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Manually add release files for better ordering
        context['release_files'] = []

        # Add source files
        context['release_files'].extend(
            list(self.object.files.filter(os__slug='source').order_by('name'))
        )

        # Add all other OSes
        context['release_files'].extend(
            list(
                self.object.files.exclude(
                    os__slug='source'
                ).order_by('os__slug', 'name')
            )
        )

        return context


class ReleaseFeed(Feed):
    """Generate an RSS feed of the latest Python releases.

    .. note:: It may seem like these are unused methods, but the superclass uses them
        using Django's Syndication framework.
        Docs: https://docs.djangoproject.com/en/4.2/ref/contrib/syndication/
    """

    feed_type = Rss201rev2Feed
    title = "Python Releases"
    description = "Latest Python releases from Python.org"

    @staticmethod
    def link() -> str:
        """Return the URL to the main downloads page."""
        return reverse('downloads:download')

    def get_feed(self, obj: Any, request: WSGIRequest) -> Feed:
        """Store the request object for later use."""
        self.request = request
        return super().get_feed(obj, request)

    def items(self) -> list[dict[str, Any]]:
        """Return the latest Python releases."""
        url = self.create_url("/api/v2/downloads/release/")
        logger.info(f"Fetching releases from: {url}")
        try:
            return self._fetch_releases(url)
        except requests.RequestException as e:
            logger.error(f"Error fetching releases from API: {str(e)}")
        except ValueError as e:
            logger.error(f"Error parsing JSON from API response: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in items method: {str(e)}")
        return []

    @staticmethod
    def _fetch_releases(url: str) -> list[dict[str, Any]]:
        """Grabs the latest Python releases from API.


        """
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        sorted_releases = sorted(data, key=lambda x: x["release_date"], reverse=True)
        return sorted_releases[:10]

    def item_title(self, item: dict[str, Any]) -> str:
        """Return the release name as the item title."""
        return item.get("name", "Unknown Release")

    def item_description(self, item: dict[str, Any]) -> str:
        """Return the release version and release date as the item description."""
        version = item.get("version", "Unknown")
        release_date = item.get("release_date", "Unknown")
        return f"Version: {version}, Release Date: {release_date}"

    def item_link(self, item: dict[str, Any]) -> str:
        """Return the URL to the release page on python.org."""
        return reverse("downloads:download_release_detail", args=[item.get("slug", "")])

    @staticmethod
    def item_pubdate(item: dict[str, Any]) -> datetime:
        """Return the release date as the item publication date."""
        try:
            release_date = datetime.strptime(
                item.get("release_date", ""), "%Y-%m-%dT%H:%M:%SZ"
            )
            return pytz.utc.localize(release_date)
        except ValueError:
            logger.error(
                f"Invalid release date format for item: {item.get('name', 'Unknown')}"
            )
            return pytz.utc.localize(datetime.now())

    @staticmethod
    def item_guid(item: dict[str, Any]) -> str:
        """Return the release URI as the item GUID."""
        return item.get("resource_uri", "")

    def create_url(self, path: str) -> str:
        """Create a full URL using the current site domain."""
        current_site = get_current_site(self.request)
        scheme = "https" if self.request.is_secure() else "http"
        return f"{scheme}://{current_site.domain}{path}"
