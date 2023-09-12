from django.urls import path
from manual.views import GetManualView, CodeView, VersionView, UploadView

app_name = 'manual'

urlpatterns = [
    path('', GetManualView.as_view(), name='get_manual'),
    path('code/', CodeView.as_view(), name='code'),
    path('version/', VersionView.as_view(), name='version'),
    path('upload/', UploadView.as_view(), name='upload'),
]
