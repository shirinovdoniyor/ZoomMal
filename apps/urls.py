from django.urls import path

from apps.views import TestTemplateView, HomeTemplateView

urlpatterns=[
    path('test',TestTemplateView.as_view()),
    path('',HomeTemplateView.as_view(),name='home')
]