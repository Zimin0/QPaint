from django.urls import path
from manual.views import GetManualView, CodeView, VersionView, UploadView, UseManualView, EmailView, ChoosePicView

app_name = 'manual'

urlpatterns = [
    path('', GetManualView.as_view(), name='get_manual'),
    path('code/', CodeView.as_view(), name='code'),
    path('version/', VersionView.as_view(), name='version'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('email/', EmailView.as_view(), name='email'),
    path('use-manual/', UseManualView.as_view(), name='use_manual'),
    path('choose-pic/', ChoosePicView.as_view(), name='choose_pic')
]
