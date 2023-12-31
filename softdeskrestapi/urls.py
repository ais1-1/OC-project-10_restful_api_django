"""
URL configuration for softdeskrestapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import authentication.views
import projectmanager.views

# create router
router = routers.SimpleRouter()


router.register("user", authentication.views.UserViewset, basename="user")
router.register("project", projectmanager.views.ProjectViewset, basename="project")
router.register(
    "contributor", projectmanager.views.ContributorViewset, basename="contributor"
)
router.register("issue", projectmanager.views.IssueViewset, basename="issue")
router.register("comment", projectmanager.views.CommentViewset, basename="comment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/signup/', authentication.views.UserSignupView.as_view(), name='signup'),
    path("api/", include(router.urls)),
]
