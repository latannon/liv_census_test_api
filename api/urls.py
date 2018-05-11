
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api import views

# router = DefaultRouter()
# router.register(r'search', views.CensusSearchResultView)
# router.register(r'variables', views.VariablesView)

urlpatterns = [
    url(r'search', views.CensusSearchResultView.as_view()),
    url(r'variables', views.VariablesView.as_view())
]