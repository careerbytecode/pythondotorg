from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField

from cms.models import NameSlugModel


DEFAULT_MARKUP_TYPE = getattr(settings, 'DEFAULT_MARKUP_TYPE', 'restructuredtext')


class Company(NameSlugModel):
    about = MarkupField(blank=True, default_markup_type=DEFAULT_MARKUP_TYPE)
    contact = models.CharField(null=True, blank=True, max_length=100)
    email = models.EmailField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
