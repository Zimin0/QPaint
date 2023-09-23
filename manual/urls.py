from django.urls import path
from manual.views import GetManualView, CodeView, VersionView, UploadView, EmailView, ChoosePicView, GetInstruction, EmailSentView, GetPixelsView

app_name = 'manual'

urlpatterns = [
    path('', GetManualView.as_view(), name='get_manual'),
    path('code/', CodeView.as_view(), name='code'),
    path('version/', VersionView.as_view(), name='version'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('email/', EmailView.as_view(), name='email'),
    path('choose-pic/', ChoosePicView.as_view(), name='choose_pic'),
    path('get-instruction/<str:instruction_slug>/', GetInstruction.as_view(), name='get_instruction'),
    path('email-sent/', EmailSentView.as_view(), name='email_sent'),
    path('get-pixels/<str:instruction_slug>/<int:page_num>/', GetPixelsView.as_view(), name='get_pixels'),
]
