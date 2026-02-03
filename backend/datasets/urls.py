from django.urls import path
from .views import (
    DatasetUploadView, DatasetListView, DatasetSummaryView, 
    DatasetTableView, DatasetReportView, DatasetCleanDownloadView, SignupView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('datasets/upload/', DatasetUploadView.as_view(), name='dataset-upload'),
    path('datasets/', DatasetListView.as_view(), name='dataset-list'),
    path('datasets/<uuid:pk>/analytics/', DatasetSummaryView.as_view(), name='dataset-analytics'),
    path('datasets/<uuid:pk>/summary/', DatasetSummaryView.as_view(), name='dataset-summary'),
    path('datasets/<uuid:pk>/table/', DatasetTableView.as_view(), name='dataset-table'),
    path('datasets/<uuid:pk>/report/', DatasetReportView.as_view(), name='dataset-report'),
    path('datasets/<uuid:pk>/download_clean/', DatasetCleanDownloadView.as_view(), name='dataset-download-clean'),
]
