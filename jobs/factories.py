import factory

from .models import JobType, JobCategory, Job
from companies.factories import CompanyFactory


class JobCategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = JobCategory
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = factory.Sequence(lambda n: 'Job Category {0}'.format(n))


class JobTypeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = JobType
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = factory.Sequence(lambda n: 'Job Type {0}'.format(n))


class JobFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Job

    category = factory.SubFactory(JobCategoryFactory)
    company = factory.SubFactory(CompanyFactory)
    city = 'Lawrence'
    region = 'KS'
    country = 'US'

    @factory.post_generation
    def job_types(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of job_types were passed in, use them
            for job_type in extracted:
                self.job_types.add(job_type)


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
