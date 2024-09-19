"""Forms to be used in mailing tests."""

from app.mailing.forms import BaseEmailTemplateForm
from app.mailing.tests.models import MockEmailTemplate


class TestBaseEmailTemplateForm(BaseEmailTemplateForm):
    """Base email template form for testing."""

    class Meta:
        """Metaclass for the form."""
        model = MockEmailTemplate
        fields = "__all__"
