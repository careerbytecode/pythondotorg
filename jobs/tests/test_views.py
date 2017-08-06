from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Job
from ..factories import (
    ApprovedJobFactory, DraftJobFactory, JobCategoryFactory, JobTypeFactory,
    ReviewJobFactory
)
from users.factories import StaffUserFactory


class JobsViewTests(TestCase):
    def setUp(self):
        self.job_category = JobCategoryFactory(
            name='Game Production',
            slug='game-production'
        )

        self.job_type = JobTypeFactory(
            name='FrontEnd Developer',
            slug='frontend-developer'
        )

        self.job = ApprovedJobFactory(
            description='Lorem ipsum dolor sit amet',
            category=self.job_category,
            city='Memphis',
            region='TN',
            country='USA',
            email='hr@company.com',
            is_featured=True,
            telecommuting=True,
        )
        self.job.job_types.add(self.job_type)

        self.job_draft = DraftJobFactory(
            description='Lorem ipsum dolor sit amet',
            category=self.job_category,
            city='Memphis',
            region='TN',
            country='USA',
            email='hr@company.com',
            is_featured=True
        )
        self.job_draft.job_types.add(self.job_type)

    def test_job_list(self):
        url = reverse('jobs:job_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/base.html')
        self.assertTemplateUsed(response, 'jobs/job_list.html')

        url = reverse('jobs:job_list_type', kwargs={'slug': self.job_type.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertTemplateUsed(response, 'jobs/base.html')
        self.assertTemplateUsed(response, 'jobs/job_list.html')

        url = reverse('jobs:job_list_category', kwargs={'slug': self.job_category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertTemplateUsed(response, 'jobs/base.html')
        self.assertTemplateUsed(response, 'jobs/job_list.html')

        url = reverse('jobs:job_list_location', kwargs={'slug': self.job.location_slug})
        response = self.client.get(url)
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/base.html')
        self.assertTemplateUsed(response, 'jobs/job_list.html')

    def test_job_list_mine(self):
        url = reverse('jobs:job_list_mine')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        username = 'kevinarnold'
        email = 'kevinarnold@example.com'
        password = 'secret'

        User = get_user_model()
        creator = User.objects.create_user(username, email, password)

        self.job = ApprovedJobFactory(
            description='My job listing',
            category=self.job_category,
            city='Memphis',
            region='TN',
            country='USA',
            email='hr@company.com',
            creator=creator,
            is_featured=True
        )

        self.client.login(username=username, password=password)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(response.context['jobs_count'], 2)
        self.assertTemplateUsed(response, 'jobs/base.html')
        self.assertTemplateUsed(response, 'jobs/job_list.html')

    def test_job_edit(self):
        username = 'kevinarnold'
        email = 'kevinarnold@example.com'
        password = 'secret'

        User = get_user_model()
        creator = User.objects.create_user(username, email, password)

        job = ApprovedJobFactory(
            description='My job listing',
            category=self.job_category,
            city='Memphis',
            region='TN',
            country='USA',
            email='hr@company.com',
            creator=creator,
            is_featured=True
        )

        self.client.login(username=username, password=password)
        url = reverse('jobs:job_edit', kwargs={'pk': job.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/base.html')

        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/jobs/%d/edit/' % job.pk)

    def test_job_detail(self):
        url = self.job.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['jobs_count'], 1)
        self.assertTemplateUsed(response, 'jobs/base.html')

        # Test 401 unauthorized
        url = self.job_draft.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_job_detail_security(self):
        """
        Ensure the public can only see approved jobs, but staff can view
        all jobs
        """
        staff_user = StaffUserFactory()

        response = self.client.get(self.job.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # Normal users can't see non-approved Jobs
        response = self.client.get(self.job_draft.get_absolute_url())
        self.assertIn(response.status_code, [401, 404])

        # Staff can see everything
        self.client.login(username=staff_user.username, password='password')
        response = self.client.get(self.job.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.job_draft.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_job_create(self):
        mail.outbox = []
        url = reverse('jobs:job_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/jobs/create/')

        post_data = {
            'category': self.job_category.pk,
            'job_types': [self.job_type.pk],
            'company_name': 'Some Company',
            'company_description': 'Some Description',
            'job_title': 'Test Job',
            'city': 'San Diego',
            'region': 'CA',
            'country': 'USA',
            'description': 'Lorem ipsum dolor sit amet',
            'requirements': 'Some requirements',
            'email': 'hr@company.com'
        }

        # Check that anonymous posting is not allowed. See #852.
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/jobs/create/')

        # Now test job submitted by logged in user
        post_data['company_name'] = 'Other Studio'

        username = 'kevinarnold'
        email = 'kevinarnold@example.com'
        password = 'secret'

        User = get_user_model()
        creator = User.objects.create_user(username, email, password)
        self.client.login(username=creator.username, password='secret')
        response = self.client.post(url, post_data, follow=True)

        # Job was saved in draft mode
        jobs = Job.objects.filter(company_name='Other Studio')
        self.assertEqual(len(jobs), 1)
        job = jobs[0]

        preview_url = reverse('jobs:job_preview', kwargs={'pk': job.pk})
        self.assertRedirects(response, preview_url)

        self.assertNotEqual(job.created, None)
        self.assertNotEqual(job.updated, None)
        self.assertEqual(job.creator, creator)
        self.assertEqual(job.status, 'draft')

        self.assertEqual(len(mail.outbox), 0)

        # Submit again to save
        response = self.client.post(preview_url, {'action': 'review'})

        # Job was now moved to review status
        job = Job.objects.get(pk=job.pk)
        self.assertEqual(job.status, 'review')

        # One email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Job Submitted for Approval: {}".format(job.display_name)
        )

        del mail.outbox[:]

    def test_job_create_prepopulate_email(self):
        create_url = reverse('jobs:job_create')
        user_data = {
            'username': 'phrasebook',
            'email': 'hungarian@example.com',
            'password': 'hovereel',
        }

        User = get_user_model()
        creator = User.objects.create_user(**user_data)

        # Logged in, email address is prepopulated.
        self.client.login(username=user_data['username'],
                          password=user_data['password'])
        response = self.client.get(create_url)

        self.assertEqual(response.context['form'].initial,
                         {'email': user_data['email']})

    def test_job_types(self):
        job_type2 = JobTypeFactory(
            name='Senior Developer',
            slug='senior-developer'
        )

        url = reverse('jobs:job_types')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.job_type, response.context['types'])
        self.assertNotIn(job_type2, response.context['types'])

    def test_job_categories(self):
        job_category2 = JobCategoryFactory(
            name='Web Development',
            slug='web-development'
        )

        url = reverse('jobs:job_categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.job_category, response.context['categories'])
        self.assertNotIn(job_category2, response.context['categories'])

    def test_job_locations(self):
        job2 = ReviewJobFactory(
            description='Lorem ipsum dolor sit amet',
            category=self.job_category,
            city='Lawrence',
            region='KS',
            country='USA',
            email='hr@company.com',
        )
        job2.job_types.add(self.job_type)

        url = reverse('jobs:job_locations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.job, response.context['jobs'])
        self.assertNotIn(job2, response.context['jobs'])

        content = str(response.content)
        self.assertIn('Memphis', content)
        self.assertNotIn('Lawrence', content)

    def test_job_telecommute(self):
        url = reverse('jobs:job_telecommute')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.job, response.context['jobs'])

    def test_job_display_name(self):
        self.assertEqual(self.job.display_name,
            "%s, %s" % (self.job.job_title, self.job.company_name))

        self.job.company_name = 'ABC'
        self.assertEqual(self.job.display_name,
            "%s, %s" % (self.job.job_title, self.job.company_name))

        self.job.company_name = ''
        self.assertEqual(self.job.display_name,
            "%s, %s" % (self.job.job_title, self.job.company_name))

    def test_job_display_about(self):
        self.job.company_description.raw = 'XYZ'
        self.assertEqual(self.job.display_description.raw, self.job.company_description.raw)

        self.job.company_description = '     '
        self.assertEqual(self.job.display_description.raw, self.job.company_description.raw)

    def test_job_list_type_404(self):
        url = reverse('jobs:job_list_type', kwargs={'slug': 'invalid-type'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_job_list_category_404(self):
        url = reverse('jobs:job_list_category', kwargs={'slug': 'invalid-type'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class JobsReviewTests(TestCase):
    def setUp(self):

        self.super_username = 'kevinarnold'
        self.super_email = 'kevinarnold@example.com'
        self.super_password = 'secret'

        self.creator_username = 'johndoe'
        self.creator_email = 'johndoe@example.com'
        self.creator_password = 'secret'
        self.contact = 'John Doe'

        self.another_username = 'another'
        self.another_email = 'another@example.com'
        self.another_password = 'secret'

        User = get_user_model()
        self.creator = User.objects.create_user(
            self.creator_username,
            self.creator_email,
            self.creator_password
        )

        self.superuser = User.objects.create_superuser(
            self.super_username,
            self.super_email,
            self.super_password
        )

        self.another = User.objects.create_user(
            self.another_username,
            self.another_email,
            self.another_password
        )

        self.job_category = JobCategoryFactory(
            name='Game Production',
            slug='game-production'
        )

        self.job_type = JobTypeFactory(
            name='FrontEnd Developer',
            slug='frontend-developer'
        )

        self.job1 = ReviewJobFactory(
            company_name='Kulfun Games',
            description='Lorem ipsum dolor sit amet',
            category=self.job_category,
            city='Memphis',
            region='TN',
            country='USA',
            email=self.creator.email,
            creator=self.creator,
            contact=self.contact
        )
        self.job1.job_types.add(self.job_type)

        self.job2 = ReviewJobFactory(
            company_name='Kulfun Games',
            description='Lorem ipsum dolor sit amet',
            category=self.job_category,
            city='Memphis',
            region='TN',
            country='USA',
            email=self.creator.email,
            creator=self.creator,
            contact=self.contact
        )
        self.job2.job_types.add(self.job_type)

        self.job3 = ReviewJobFactory(
            company_name='Kulfun Games',
            description='Lorem ipsum dolor sit amet',
            category=self.job_category,
            city='Memphis',
            region='TN',
            country='USA',
            email=self.creator.email,
            creator=self.creator,
            contact=self.contact
        )
        self.job3.job_types.add(self.job_type)

    def test_job_review(self):
        # FIXME: refactor to separate tests cases for clarity?
        mail.outbox = []
        url = reverse('jobs:job_review')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.super_username, password=self.super_password)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)
        self.assertIn(self.job1, response.context['object_list'])
        self.assertIn(self.job2, response.context['object_list'])
        self.assertIn(self.job3, response.context['object_list'])

        # no email notifications sent before offer is approved
        self.assertEqual(len(mail.outbox), 0)
        self.client.post(url, data={'job_id': self.job1.pk, 'action': 'approve'})
        j1 = Job.objects.get(pk=self.job1.pk)
        self.assertEqual(j1.status, Job.STATUS_APPROVED)
        # exactly one approval notification email should sent
        # to the offer creator
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, [self.creator.email, 'jobs@python.org'])
        self.assertIn(self.contact, message.body)
        mail.outbox = []

        # no email notifications sent before offer is rejected
        self.assertEqual(len(mail.outbox), 0)
        self.client.post(url, data={'job_id': self.job2.pk, 'action': 'reject'})
        j2 = Job.objects.get(pk=self.job2.pk)
        self.assertEqual(j2.status, Job.STATUS_REJECTED)
        # exactly one rejection notification email should sent
        # to the offer creator
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, [self.creator.email, 'jobs@python.org'])
        self.assertIn(self.contact, message.body)
        mail.outbox = []

        self.client.post(url, data={'job_id': self.job3.pk, 'action': 'remove'})
        j3 = Job.objects.get(pk=self.job3.pk)
        self.assertEqual(j3.status, Job.STATUS_REMOVED)

        response = self.client.post(url, data={'job_id': 999999, 'action': 'approve'})
        self.assertEqual(response.status_code, 302)

    def test_job_comment(self):
        mail.outbox = []
        self.client.login(username=self.creator_username, password=self.creator_password)
        url = reverse('jobs:job_review_comment_create')
        form_data = {
            'job': self.job1.pk,
            'comment': 'Lorem ispum',
        }
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.creator.email, 'jobs@python.org'])

    def test_job_comment_401(self):
        mail.outbox = []
        self.client.login(username=self.another_username, password=self.another_password)
        url = reverse('jobs:job_review_comment_create')
        form_data = {
            'job': self.job1.pk,
            'comment': 'Foooo',
        }
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(mail.outbox), 0)

    def test_job_comment_401_approve(self):
        mail.outbox = []
        self.client.login(username=self.creator_username, password=self.creator_password)
        url = reverse('jobs:job_review_comment_create')
        form_data = {
            'job': self.job1.pk,
            'action': 'approve',
        }
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(mail.outbox), 0)
