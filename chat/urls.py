from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name="chat_page"),               # Home UI
    path('api/chat/', views.chat_api, name="chat_api"),        # Chat API
    path('clear-chat/', views.clear_chat, name="clear_chat"),  # Clear messages
    path('export/txt/', views.export_txt, name="export_txt"),  # Download TXT
    path('export/pdf/', views.export_pdf, name="export_pdf"),  # Download PDF
]
