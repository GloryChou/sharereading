"""sharereading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from . import admin
from . import applicant
from . import student

urlpatterns = [
    url(r'^$', admin.index),
    url(r'^admin$', admin.index),
    url(r'^admin/login$', admin.login),
    url(r'^admin/logout$', admin.logout),
    url(r'^admin/verifyCode$', admin.verifyCode), 
    
    url(r'^applicant$', applicant.applicant),
    url(r'^applicant/applicate$', applicant.applicate),
    url(r'^applicant/list$', applicant.list),
    url(r'^applicant/detail$', applicant.detail),
    url(r'^applicant/adopt$', applicant.adopt),
    url(r'^applicant/reject$', applicant.reject),
    
    url(r'^students$', student.list),
    url(r'^student/input$', student.input),
    url(r'^student/submitInput$', student.submitInput),
    url(r'^student/detail$', student.detail),
    url(r'^student/update$', student.update),
]
