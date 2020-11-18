import json
from model_bakery import baker
from itertools import chain

from django.contrib import messages
from django.conf import settings
from django.core import mail
from django.urls import reverse, reverse_lazy
from django.test import TestCase
from django.contrib.messages import get_messages

from .utils import get_static_image_file_as_upload
from ..models import (
    Sponsor,
    SponsorshipProgram,
    SponsorshipBenefit,
    Sponsor,
    SponsorContact,
    Sponsorship,
)

from sponsors.forms import SponsorshiptBenefitsForm, SponsorshipApplicationForm


def assertMessage(msg, expected_content, expected_level):
    assert msg.level == expected_level, f"Message {msg} level is not {expected_level}"
    assert (
        str(msg) == expected_content
    ), f"Message {msg} content is not {expected_content}"


class SelectSponsorshipApplicationBenefitsViewTests(TestCase):
    url = reverse_lazy("select_sponsorship_application_benefits")

    def setUp(self):
        self.psf = baker.make("sponsors.SponsorshipProgram", name="PSF")
        self.wk = baker.make("sponsors.SponsorshipProgram", name="Working Group")
        self.program_1_benefits = baker.make(
            SponsorshipBenefit, program=self.psf, _quantity=3
        )
        self.program_2_benefits = baker.make(
            SponsorshipBenefit, program=self.wk, _quantity=5
        )
        self.user = baker.make(settings.AUTH_USER_MODEL, is_staff=True, is_active=True)
        self.client.force_login(self.user)

    def test_display_template_with_form_and_context(self):
        psf_package = baker.make("sponsors.SponsorshipPackage")
        extra_package = baker.make("sponsors.SponsorshipPackage")

        r = self.client.get(self.url)
        packages = r.context["sponsorship_packages"]

        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "sponsors/sponsorship_benefits_form.html")
        self.assertIsInstance(r.context["form"], SponsorshiptBenefitsForm)
        self.assertEqual(r.context["benefit_model"], SponsorshipBenefit)
        self.assertEqual(2, packages.count())
        self.assertIn(psf_package, packages)
        self.assertIn(extra_package, packages)

    def test_display_form_with_errors_if_invalid_post(self):
        r = self.client.post(self.url, {})
        form = r.context["form"]

        self.assertIsInstance(form, SponsorshiptBenefitsForm)
        self.assertTrue(form.errors)

    def test_login_required(self):
        redirect_url = f"{settings.LOGIN_URL}?next={self.url}"
        self.client.logout()

        r = self.client.get(self.url)

        self.assertRedirects(r, redirect_url)

    def test_staff_required(self):
        redirect_url = f"{settings.LOGIN_URL}?next={self.url}"
        self.user.is_staff = False
        self.user.save()
        self.client.force_login(self.user)

        r = self.client.get(self.url)

        self.assertRedirects(r, redirect_url, fetch_redirect_response=False)

    def test_valid_post_redirect_user_to_next_form_step_and_save_info_in_cookies(self):
        package = baker.make("sponsors.SponsorshipPackage")
        for benefit in self.program_1_benefits:
            benefit.packages.add(package)

        data = {
            "benefits_psf": [b.id for b in self.program_1_benefits],
            "benefits_working_group": [b.id for b in self.program_2_benefits],
            "package": package.id,
        }
        response = self.client.post(self.url, data=data)

        self.assertRedirects(response, reverse("new_sponsorship_application"))
        cookie_value = json.loads(
            response.client.cookies["sponsorship_selected_benefits"].value
        )
        self.assertEqual(data, cookie_value)

    def test_populate_form_initial_with_values_from_cookie(self):
        initial = {
            "benefits_psf": [b.id for b in self.program_1_benefits],
            "benefits_working_group": [b.id for b in self.program_2_benefits],
            "package": "",
        }
        self.client.cookies["sponsorship_selected_benefits"] = json.dumps(initial)
        r = self.client.get(self.url)

        self.assertEqual(initial, r.context["form"].initial)


class NewSponsorshipApplicationViewTests(TestCase):
    url = reverse_lazy("new_sponsorship_application")

    def setUp(self):
        self.user = baker.make(
            settings.AUTH_USER_MODEL, is_staff=True, email="bernardo@companyemail.com"
        )
        self.client.force_login(self.user)
        self.psf = baker.make("sponsors.SponsorshipProgram", name="PSF")
        self.program_1_benefits = baker.make(
            SponsorshipBenefit, program=self.psf, _quantity=3
        )
        self.package = baker.make("sponsors.SponsorshipPackage")
        for benefit in self.program_1_benefits:
            benefit.packages.add(self.package)
        self.client.cookies["sponsorship_selected_benefits"] = json.dumps(
            {
                "package": self.package.id,
                "benefits_psf": [b.id for b in self.program_1_benefits],
            }
        )
        self.data = {
            "name": "CompanyX",
            "primary_phone": "+14141413131",
            "mailing_address": "4th street",
            "contact-0-name": "Bernardo",
            "contact-0-email": self.user.email,
            "contact-0-phone": "+1999999999",
            "contact-0-primary": True,
            "contact-TOTAL_FORMS": 1,
            "contact-MAX_NUM_FORMS": 5,
            "contact-MIN_NUM_FORMS": 1,
            "contact-INITIAL_FORMS": 1,
            "web_logo": get_static_image_file_as_upload("psf-logo.png", "logo.png"),
        }

    def test_display_template_with_form_and_context(self):
        r = self.client.get(self.url)

        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "sponsors/new_sponsorship_application_form.html")
        self.assertIsInstance(r.context["form"], SponsorshipApplicationForm)
        self.assertEqual(r.context["sponsorship_package"], self.package)
        self.assertEqual(
            len(r.context["sponsorship_benefits"]), len(self.program_1_benefits)
        )
        self.assertEqual(
            r.context["sponsorship_price"], self.package.sponsorship_amount
        )
        for benefit in self.program_1_benefits:
            self.assertIn(benefit, r.context["sponsorship_benefits"])

    def test_return_package_as_none_if_not_previously_selected(self):
        self.client.cookies["sponsorship_selected_benefits"] = json.dumps(
            {
                "benefits_psf": [b.id for b in self.program_1_benefits],
            }
        )
        r = self.client.get(self.url)
        self.assertIsNone(r.context["sponsorship_package"])
        self.assertIsNone(r.context["sponsorship_price"])

    def test_no_sponsorship_price_if_customized_benefits(self):
        extra_benefit = baker.make(SponsorshipBenefit)
        benefits = self.program_1_benefits + [extra_benefit]
        self.client.cookies["sponsorship_selected_benefits"] = json.dumps(
            {
                "package": self.package.id,
                "benefits_psf": [b.id for b in benefits],
            }
        )

        r = self.client.get(self.url)

        self.assertEqual(r.context["sponsorship_package"], self.package)
        self.assertIsNone(r.context["sponsorship_price"])
        for benefit in benefits:
            self.assertIn(benefit, r.context["sponsorship_benefits"])

    def test_display_form_with_errors_if_invalid_post(self):
        r = self.client.post(self.url, {})
        form = r.context["form"]

        self.assertIsInstance(form, SponsorshipApplicationForm)
        self.assertTrue(form.errors)

    def test_login_required(self):
        redirect_url = f"{settings.LOGIN_URL}?next={self.url}"
        self.client.logout()

        r = self.client.get(self.url)

        self.assertRedirects(r, redirect_url)

    def test_redirect_user_back_to_benefits_selection_if_no_selected_benefits_cookie(
        self,
    ):
        redirect_msg = "You have to select sponsorship package and benefits before."
        redirect_lvl = messages.INFO

        self.client.cookies.pop("sponsorship_selected_benefits")
        r = self.client.get(self.url)
        r_messages = list(get_messages(r.wsgi_request))
        assertMessage(r_messages[0], redirect_msg, redirect_lvl)
        self.assertRedirects(r, reverse("select_sponsorship_application_benefits"))

        self.client.cookies["sponsorship_selected_benefits"] = ""
        r = self.client.get(self.url)
        self.assertRedirects(r, reverse("select_sponsorship_application_benefits"))

        self.client.cookies["sponsorship_selected_benefits"] = "{}"
        r = self.client.get(self.url)
        self.assertRedirects(r, reverse("select_sponsorship_application_benefits"))

        self.client.cookies["sponsorship_selected_benefits"] = "invalid"
        r = self.client.get(self.url)
        self.assertRedirects(r, reverse("select_sponsorship_application_benefits"))

    def test_create_new_sponsorship(self):
        self.assertFalse(Sponsor.objects.exists())

        r = self.client.post(self.url, data=self.data)
        self.assertEqual(r.context["sponsorship"].sponsor.name, "CompanyX")
        self.assertEqual(r.context["notified"], ["bernardo@companyemail.com"])

        self.assertTrue(Sponsor.objects.filter(name="CompanyX").exists())
        self.assertTrue(
            SponsorContact.objects.filter(
                sponsor__name="CompanyX", user=self.user
            ).exists()
        )
        sponsorship = Sponsorship.objects.get(sponsor__name="CompanyX")
        self.assertTrue(sponsorship.benefits.exists())
        self.assertTrue(sponsorship.level_name)
        self.assertEqual(
            r.client.cookies.get("sponsorship_selected_benefits").value, ""
        )
        self.assertTrue(mail.outbox)

    def test_redirect_user_back_to_benefits_selection_if_post_without_valid_set_of_benefits(
        self,
    ):
        redirect_msg = "You have to select sponsorship package and benefits before."
        redirect_lvl = messages.INFO

        self.client.cookies.pop("sponsorship_selected_benefits")
        r = self.client.post(self.url, data=self.data)
        self.assertRedirects(r, reverse("select_sponsorship_application_benefits"))
        r_messages = list(get_messages(r.wsgi_request))
        assertMessage(r_messages[0], redirect_msg, redirect_lvl)
        self.assertRedirects(r, reverse("select_sponsorship_application_benefits"))

        self.data["web_logo"] = get_static_image_file_as_upload(
            "psf-logo.png", "logo.png"
        )
        self.client.cookies["sponsorship_selected_benefits"] = ""
        r = self.client.post(self.url, data=self.data)
        self.assertRedirects(r, reverse("select_sponsorship_application_benefits"))

        self.data["web_logo"] = get_static_image_file_as_upload(
            "psf-logo.png", "logo.png"
        )
        self.client.cookies["sponsorship_selected_benefits"] = "{}"
        r = self.client.post(self.url, data=self.data)
        self.assertRedirects(r, reverse("select_sponsorship_application_benefits"))

        self.data["web_logo"] = get_static_image_file_as_upload(
            "psf-logo.png", "logo.png"
        )
        self.client.cookies["sponsorship_selected_benefits"] = "invalid"
        r = self.client.post(self.url, data=self.data)
        self.assertRedirects(r, reverse("select_sponsorship_application_benefits"))
