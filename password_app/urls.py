from .views import *
from django.urls import path

urlpatterns=[
    
        path('save_get_password/<int:user_id>/', SaveAndGetMessage.as_view(),name='sample=view'),
        path('auth/google/', GoogleLoginApi.as_view(),name='google_api'),
        
]

