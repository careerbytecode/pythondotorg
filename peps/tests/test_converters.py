from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings

from peps.converters import get_pep0_page, get_pep_page, add_pep_image
from pydotorg.test_utils import captured_stdout

from . import FAKE_PEP_REPO


class PEPConverterTests(TestCase):

    @override_settings(PEP_REPO_PATH='/path/that/does/not/exist')
    def test_converter_path_checks(self):
        with self.assertRaises(ImproperlyConfigured):
            get_pep0_page()

    @override_settings(PEP_REPO_PATH=FAKE_PEP_REPO)
    def test_source_link(self):
        pep = get_pep_page('0525')
        self.assertEqual(pep.title, 'PEP 525 -- Asynchronous Generators')
        self.assertIn(
            'Source: <a href="https://github.com/python/peps/blob/master/'
            'pep-0525.txt">https://github.com/python/peps/blob/master/pep-0525.txt</a>',
            pep.content.rendered
        )

    @override_settings(PEP_REPO_PATH=FAKE_PEP_REPO)
    def test_invalid_pep_number(self):
        with captured_stdout() as stdout:
            get_pep_page('9999999')
        self.assertRegex(
            stdout.getvalue(),
            r"PEP Path '(.*)9999999(.*)' does not exist, skipping"
        )

    @override_settings(PEP_REPO_PATH=FAKE_PEP_REPO)
    def test_add_image_not_found(self):
        with captured_stdout() as stdout:
            add_pep_image('0525', '/path/that/does/not/exist')
        self.assertRegex(
            stdout.getvalue(),
            r"Image Path '(.*)/path/that/does/not/exist(.*)' does not exist, skipping"
        )

    @override_settings(PEP_REPO_PATH=FAKE_PEP_REPO)
    def test_html_do_not_prettify(self):
        pep = get_pep_page('3001')
        self.assertEqual(
            pep.title,
            'PEP 3001 -- Procedure for reviewing and improving standard library modules'
        )
        self.assertIn(
            '<tr class="field"><th class="field-name">Title:</th>'
            '<td class="field-body">Procedure for reviewing and improving '
            'standard library modules</td>\n</tr>',
            pep.content.rendered
        )
