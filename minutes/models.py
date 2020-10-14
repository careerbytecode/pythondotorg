from django.conf import settings
from django.urls import reverse
from django.db import models
from ordered_model.models import OrderedModel

from markupfield.fields import MarkupField

from cms.models import ContentManageable

from .managers import MinutesQuerySet

DEFAULT_MARKUP_TYPE = getattr(settings, 'DEFAULT_MARKUP_TYPE', 'restructuredtext')


class Minutes(ContentManageable):
    date = models.DateField(verbose_name='Meeting Date', db_index=True)
    content = MarkupField(default_markup_type=DEFAULT_MARKUP_TYPE)
    is_published = models.BooleanField(default=False, db_index=True)

    objects = MinutesQuerySet.as_manager()

    class Meta:
        verbose_name = 'minutes'
        verbose_name_plural = 'minutes'

    def __str__(self):
        return "PSF Meeting Minutes %s" % self.date.strftime("%B %d, %Y")

    def get_absolute_url(self):
        return reverse('minutes_detail', kwargs={
            'year': self.get_date_year(),
            'month': self.get_date_month(),
            'day': self.get_date_day(),
        })

    # Helper methods for sitetree
    def get_date_year(self):
        return self.date.strftime("%Y")

    def get_date_month(self):
        return self.date.strftime("%m").zfill(2)

    def get_date_day(self):
        return self.date.strftime("%d").zfill(2)


class Concern(models.Model):
    """ A "Concern" is a sort of Organizational Unit
        which can exist in a tree like structure """

    #  Name of the "Concern", Example: PSF Board, Packaging Working Group,
    #  or "Project"
    name = models.CharField(max_length=128)
    #  If applicable, a "parent" concern.
    #  Example: Finance committee of PSF Board,
    #  or "PIP UX Project 2020" under the Packaging Working Group
    parent_concern = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="children_concerns")

    def __str__(self):
        if self.parent_concern_id:
            return f"{self.parent_concern} > {self.name}"
        return self.name

    class Meta:
        verbose_name = "concern"
        verbose_name_plural = "concerns"

    @property
    def concerned_parties(self):
        return ConcernedParty.objects.filter(role__in=self.concernrole_set.all())


class ConcernRole(models.Model):
    """ A User's role within a concern, may be generic and come with
        certain specific items that they are responsible for or allowed
        to provide """
    name = models.CharField(max_length=128)
    concern = models.ForeignKey(Concern, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.concern}: {self.name}"

    class Meta:
        verbose_name = "concern role"
        verbose_name_plural = "concern roles"


class ConcernedPartyQuerySet(models.QuerySet):
    def by_concern(self, concern):
        return self.filter(role__concern__name__iexact=concern)

    def by_concern_role(self, concern, role):
        return self.by_concern(concern).filter(role__name__iexact=role)


class ConcernedParty(models.Model):
    """ Effectively a "Group" for a given concern that makes managing
        access and reminders more straightforward. This may include the ability
        to email a notification that a meeting has been scheduled, remind
        attendees to submit reports, etc. """
    objects = ConcernedPartyQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(ConcernRole, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} as {self.role}"

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = "concerned party"
        verbose_name_plural = "concerned parties"


class Meeting(models.Model):
    title = models.CharField(max_length=500)
    date = models.DateField(db_index=True)
    parties = models.ManyToManyField(ConcernedParty)
    minutes = models.OneToOneField(Minutes, null=True, blank=True, on_delete=models.CASCADE, related_name="meeting")

    def get_content(self):
        content = ""

        # TODO more semantic query
        for item in self.agendaitem_set.all():
            content += f"\n# {item.title}\n"
            content += item.content.raw

        for item in self.minuteitem_set.all():
            content += f"\n{item.content.raw}\n"

        return content.strip()

    def update_minutes(self):
        if not self.minutes:
            self.minutes = Minutes.objects.create(is_published=False, date=self.date)
            self.save()

        if not self.minutes.is_published:
            # TODO; guarantee same markup field types
            self.minutes.content = self.get_content()
            self.minutes.content_markup_type = "markdown"
            self.minutes.save()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "meeting"
        verbose_name_plural = "meetings"


class AgendaItem(OrderedModel):
    """ Class for items such as reports, discussion topics, or
        resolutions which are submitted before a meeting.
        These are constructed together into a completed Agenda object. """
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = MarkupField(default_markup_type=DEFAULT_MARKUP_TYPE)
    owners = models.ManyToManyField(ConcernedParty)
    order_with_respect_to = 'meeting'


class MinuteItem(OrderedModel):
    """ Class for items such as notes or action items generated during a meeting.
        These are constructed together into a completed Minutes object """
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    content = MarkupField(default_markup_type=DEFAULT_MARKUP_TYPE)
    order_with_respect_to = 'meeting'
