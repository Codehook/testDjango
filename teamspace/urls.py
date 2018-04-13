"""
URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls import url
from teamspace.views import frontend
from teamspace.views import dashboard
from teamspace.views import organization
from teamspace.views import team
from teamspace.views import google

handler404 = 'teamspace.views.errors.handler404'

urlpatterns = [

    # Frontend routes
    url(r'^', include([
        url(r'^$', frontend.home, name='home'),
        url(r'^about/$', frontend.about, name='about'),
        url(r'^login/$', frontend.login, name='login'),
        url(r'^logout/$', frontend.logout, name='logout'),
        url(r'^signup/$', frontend.signup, name='signup'),
    ], namespace='frontend')),

    # Dashboard routes
    url(r'^d/', include([

        # Root dashboard routes
        url(r'^$', dashboard.home, name='home'),

        # Account management routes
        url(r'^u/', include([
            url(r'^edit/$', dashboard.user_edit, name='edit'),
            url(r'^password/$', dashboard.user_password, name='password'),
        ], namespace='user')),

        # Organization access/creation routes
        url(r'^o/', include([
            url(r'^view/$', dashboard.orgs_view, name='view'),
            url(r'^create/$', dashboard.orgs_create, name='create'),
        ], namespace='organization')),

    ], namespace='dashboard')),

    # Organization routes
    url(r'^o/([0-9]+)/', include([

        # Root organization routes
        url(r'^$', organization.home, name='home'),
        url(r'^users/$', organization.users, name='users'),
        url(r'^leave/$', organization.leave, name='leave'),
        url(r'^delete/$', organization.delete, name='delete'),

        # Organization management routes
        url(r'^m/', include([
            url(r'^edit/$', organization.manage_edit, name='edit'),
            url(r'^users/$', organization.manage_users, name='users'),
        ], namespace='manage')),

        # Team access/creation routes
        url(r'^t/', include([
            url(r'^view/$', organization.teams_view, name='view'),
            url(r'^create/$', organization.teams_create, name='create'),
        ], namespace='team')),

    ], namespace='organization')),

    # Team routes
    url(r'^t/([0-9]+)/', include([

        # Root team routes
        url(r'^$', team.home, name='home'),
        url(r'^leave/$', team.leave, name='leave'),
        url(r'^delete/$', team.delete, name='delete'),
        url(r'^events/$', team.events, name='events'),
        url(r'^files/$', team.files, name='files'),
        url(r'^chat/$', team.chat, name='chat'),
        url(r'^users/$', team.users, name='users'),

        # Team management routes
        url(r'^m/', include([
            url(r'^edit/$', team.manage_edit, name='edit'),
            url(r'^users/$', team.manage_users, name='users'),
        ], namespace='manage')),

    ], namespace='team')),

    # Provider routes
    url(r'^providers/', include([

        url(r'^google/$', google.index, name='google'),

    ], namespace='providers')),

]
