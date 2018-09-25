import datetime
import factory

from django.contrib.auth.models import Group
from django.utils import timezone

from faker.providers import BaseProvider

from users.factories import UserFactory

from .models import (
    JobType, JobCategory, Job, City, Region, Country,
)


class CitiesProvider(BaseProvider):

    countries = [
        'United States',
        'Germany',
        'Turkey',
        'Middle Earth',
    ]

    regions = [
        'New York',
        'Berlin',
        'Istanbul',
        'Kansas',
        'Mordor',
    ]

    cities = [
        'New York',
        'Berlin',
        'Istanbul',
        'Lawrence',
        'Mordor',
    ]

    def job_city(self):
        return self.random_element(self.cities)

    def job_region(self):
        return self.random_element(self.regions)

    def job_country(self):
        return self.random_element(self.countries)

factory.Faker.add_provider(CitiesProvider)


class JobProvider(BaseProvider):

    job_types = [
        'Big Data',
        'Cloud',
        'Database',
        'Evangelism',
        'Systems',
        'Test',
        'Web',
        'Operations',
    ]

    job_categories = [
        'Software Developer',
        'Software Engineer',
        'Data Analyst',
        'Administrator',
    ]

    job_titles = [
        'Senior Python Developer',
        'Django Developer',
        'Full Stack Python/Django Developer',
        'Machine Learning Engineer',
        'Full Stack Developer',
        'Python Data Engineer',
        'Senior Test Automation Engineer',
        'Backend Python Engineer',
        'Python Tech Lead',
        'Junior Developer',
    ]

    def job_type(self):
        return self.random_element(self.job_types)

    def job_category(self):
        return self.random_element(self.job_categories)

    def job_title(self):
        return self.random_element(self.job_titles)


factory.Faker.add_provider(JobProvider)


class CountryFactory(factory.DjangoModelFactory):

    class Meta:
        model = Country
        django_get_or_create = ('name',)

    name = factory.Faker('job_country')


class RegionFactory(factory.DjangoModelFactory):

    class Meta:
        model = Region
        django_get_or_create = ('name', 'country')

    name = factory.Faker('job_region')


class CityFactory(factory.DjangoModelFactory):

    class Meta:
        model = City
        django_get_or_create = ('name', 'region')

    name = factory.Faker('job_city')
    country = factory.SubFactory(CountryFactory)
    region = factory.SubFactory(
        RegionFactory,
        country=factory.SelfAttribute('..country'),
    )


class JobCategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = JobCategory
        django_get_or_create = ('name',)

    name = factory.Faker('job_category')
    active = True


class JobTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = JobType
        django_get_or_create = ('name',)

    name = factory.Faker('job_type')


class JobFactory(factory.DjangoModelFactory):

    class Meta:
        model = Job

    creator = factory.SubFactory(UserFactory)
    category = factory.SubFactory(JobCategoryFactory)
    job_title = factory.Faker('job_title')
    location = factory.SubFactory(CityFactory)
    company_name = factory.Faker('company')
    company_description = factory.Faker('sentence', nb_words=10)
    contact = factory.Faker('name')
    email = factory.Faker('email')
    url = 'https://www.example.com/'

    description = 'Test Description'
    requirements = 'Test Requirements'

    @factory.lazy_attribute
    def expires(self):
        return timezone.now() + datetime.timedelta(days=30)

    @factory.post_generation
    def job_types(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of job_types were passed in, use them
            for job_type in extracted:
                self.job_types.add(job_type)


class LegacyJobFactory(JobFactory):
    city = 'Lawrence'
    region = 'KS'
    country = 'US'
    location = None


class ApprovedLegacyJobFactory(LegacyJobFactory):
    status = Job.STATUS_APPROVED


class ApprovedJobFactory(JobFactory):
    status = Job.STATUS_APPROVED


class ArchivedJobFactory(JobFactory):
    status = Job.STATUS_ARCHIVED


class DraftJobFactory(JobFactory):
    status = Job.STATUS_DRAFT


class ExpiredJobFactory(JobFactory):
    status = Job.STATUS_EXPIRED


class RejectedJobFactory(JobFactory):
    status = Job.STATUS_REJECTED


class RemovedJobFactory(JobFactory):
    status = Job.STATUS_REMOVED


class ReviewJobFactory(JobFactory):
    status = Job.STATUS_REVIEW


class JobsBoardAdminGroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group
        django_get_or_create = ('name',)

    name = 'Job Board Admin'


def initial_data():
    return {
        'jobs': [
            ArchivedJobFactory(),
            DraftJobFactory(),
            ExpiredJobFactory(),
            RejectedJobFactory(),
            RemovedJobFactory(),
        ] + ApprovedJobFactory.create_batch(size=5) + ReviewJobFactory.create_batch(size=3),
        'groups': [
            JobsBoardAdminGroupFactory(),
        ],
    }
