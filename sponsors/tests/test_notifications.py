from model_bakery import baker

from allauth.account.models import EmailAddress
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.test import TestCase

from sponsors import notifications


class AppliedSponsorshipNotificationToPSFTests(TestCase):
    def setUp(self):
        self.notification = notifications.AppliedSponsorshipNotificationToPSF()
        self.user = baker.make(settings.AUTH_USER_MODEL)
        self.sponsorship = baker.make("sponsors.Sponsorship")
        self.subject_template = "sponsors/email/psf_new_application_subject.txt"
        self.content_template = "sponsors/email/psf_new_application.txt"

    def test_send_email_using_correct_templates(self):
        context = {"user": self.user, "sponsorship": self.sponsorship}
        expected_subject = render_to_string(self.subject_template, context).strip()
        expected_content = render_to_string(self.content_template, context).strip()

        self.notification.notify(self.user, self.sponsorship)
        self.assertTrue(mail.outbox)

        email = mail.outbox[0]
        self.assertEqual(expected_subject, email.subject)
        self.assertEqual(expected_content, email.body)
        self.assertEqual(settings.DEFAULT_FROM_EMAIL, email.from_email)
        self.assertEqual([settings.SPONSORS_TO_EMAIL], email.to)


class AppliedSponsorshipNotificationToSponsorsTests(TestCase):
    def setUp(self):
        self.notification = notifications.AppliedSponsorshipNotificationToSponsors()
        self.user = baker.make(settings.AUTH_USER_MODEL, email="foo@foo.com")
        self.verified_email = baker.make(EmailAddress, verified=True)
        self.unverified_email = baker.make(EmailAddress, verified=False)
        self.sponsor_contacts = [
            baker.make(
                "sponsors.SponsorContact", email="foo@example.com", primary=True
            ),
            baker.make("sponsors.SponsorContact", email=self.verified_email.email),
            baker.make("sponsors.SponsorContact", email=self.unverified_email.email),
        ]
        self.sponsor = baker.make("sponsors.Sponsor", contacts=self.sponsor_contacts)
        self.sponsorship = baker.make("sponsors.Sponsorship", sponsor=self.sponsor)
        self.subject_template = "sponsors/email/sponsor_new_application_subject.txt"
        self.content_template = "sponsors/email/sponsor_new_application.txt"

    def test_send_email_using_correct_templates(self):
        context = {"user": self.user, "sponsorship": self.sponsorship}
        expected_subject = render_to_string(self.subject_template, context).strip()
        expected_content = render_to_string(self.content_template, context).strip()

        self.notification.notify(self.user, self.sponsorship)
        self.assertTrue(mail.outbox)

        email = mail.outbox[0]
        self.assertEqual(expected_subject, email.subject)
        self.assertEqual(expected_content, email.body)
        self.assertEqual(settings.DEFAULT_FROM_EMAIL, email.from_email)
        self.assertCountEqual([self.user.email, self.verified_email.email], email.to)

    def test_send_email_to_correct_recipients(self):
        context = {"user": self.user, "sponsorship": self.sponsorship}
        expected_contacts = ["foo@foo.com", self.verified_email.email]
        self.assertCountEqual(
            expected_contacts, self.notification.get_recipient_list(context)
        )
