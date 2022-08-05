from django.urls import include, path
from . import views
from . import procore
import debug_toolbar
from django.conf import settings

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('', views.index, name='index'),
    path('api/', views.apiOverview, name='apiOverview'),
    path('copyfroms3/', views.copyfroms3, name='copyfroms3'),
    path('list_users/', views.alluser, name='list_users'),
    path('manual_create', views.manual_create, name='manual_create'),
    path('merge/', views.merge, name='merge'),
    path('toc/', views.toc, name='toc'),
    path('ocr/', views.ocr, name='ocr'),
    path('uploadS3', views.uploadS3, name='uploadS3'),
    path('get_closeout_manual/', views.get_closeout_manual, name='get_closeout_manual'),
    path('procoreCommitments', procore.procoreCommitments, name='procoreCommitments'),
    path('procoreinspections', procore.inspections, name='inspections'),
    path('projectDates', procore.ProjectDates, name='ProjectDates'),
    path('all_project', procore.all_project, name='all_project'),
    path('bambo', views.training_data_company, name='training_data_company'),
    path('mergerfi', views.RFIMerge, name='RFIMerge'),
    path('qrcode', views.qrcode, name='qrcode'),
    path('busybusy', views.busybusy, name='busybusy'),
]
