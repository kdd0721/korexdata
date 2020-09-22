from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from address.views import BrTitleInfoViewSet, UnitViewSet

router = DefaultRouter()
router.register('brtitleinfos', BrTitleInfoViewSet)
router.register('units', UnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
