from django.urls import path
from .views import chatbot_page, chatbot_api, submit_complaint

urlpatterns = [
    path('', chatbot_page, name='chatbot_page'),
    path('api/', chatbot_api, name='chatbot_api'),
    path('submit-complaint/', submit_complaint, name='submit_complaint'),
]
