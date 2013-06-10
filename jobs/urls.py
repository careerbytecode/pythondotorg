from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('',
    url(r'^$', views.JobList.as_view(), name='job_list'),
    url(r'^create/$', views.JobCreate.as_view(), name='job_create'),
    url(r'^mine/$', views.JobListMine.as_view(), name='job_list_mine'),
    url(r'^review/$', views.JobReview.as_view(), name='job_review'),
    url(r'^location/(?P<slug>[-_\w]+)/$', views.JobListLocation.as_view(), name='job_list_location'),
    url(r'^type/(?P<slug>[-_\w]+)/$', views.JobListType.as_view(), name='job_list_type'),
    url(r'^category/(?P<slug>[-_\w]+)/$', views.JobListCategory.as_view(), name='job_list_category'),
    url(r'^company/(?P<slug>[-_\w]+)/$', views.JobListCompany.as_view(), name='job_list_company'),
    url(r'^(?P<pk>\d+)/archive/$', views.JobArchive.as_view(), name='job_archive'),
    url(r'^(?P<pk>\d+)/edit/$', views.JobEdit.as_view(), name='job_edit'),
    url(r'^(?P<pk>\d+)/publish/$', views.JobPublish.as_view(), name='job_publish'),
    url(r'^(?P<pk>\d+)/review/$', views.JobDetailReview.as_view(), name='job_detail_review'),
    url(r'^(?P<pk>\d+)/$', views.JobDetail.as_view(), name='job_detail'),
)
