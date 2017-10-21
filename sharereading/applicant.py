# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf

from django.core.exceptions import ObjectDoesNotExist

from WebModel.models import Admin
from WebModel.models import Student
from WebModel.models import Applicant
from WebModel.models import ApplicantForm

from . import authorization
from . import mail_handler

import traceback

# 进入申请页面
def applicant(request):
    studentId = request.GET['studentId']
    studentLastName = Student.objects.get(id=studentId).lastName
    return render_to_response('applicate.html', {'selectStudentId': studentId, 'studentLastName': studentLastName})

# 提交申请
@csrf_exempt
def applicate(request):
    applicantForm = ApplicantForm(request.POST)
    if applicantForm.is_valid():    
        applicantForm.save()

    return HttpResponseRedirect('/students')

# 获取申请者列表
def list(request):
    if not authorization.authentic(request):
        return render_to_response('admin.html')

    try:
        applicantList = Applicant.objects.all()
        return render_to_response('applicant_list.html', {'applicantList':applicantList})
    except:
        return render_to_response('admin.html')

# 获取申请者详细
def detail(request):
    if not authorization.authentic(request):
        return render_to_response('admin.html')

    applicantId = request.GET['id']
    if applicantId is None:
        return HttpResponseRedirect('/applicant/list')

    try:
        applicantEntry = Applicant.objects.get(id=applicantId)
        return render_to_response('applicant_detail.html', {'applicant':applicantEntry})
    except:
        return HttpResponseRedirect('/applicant/list')

# 审核通过
def adopt(request):
    if not authorization.authentic(request):
        return render_to_response('admin.html')

    applicantId = request.GET['id']
    if applicantId is None:
        return HttpResponseRedirect('/applicant/list')

    try:
        # 修改申请者状态
        applicantEntry = Applicant.objects.get(id=applicantId)
        applicantEntry.status = 1
        applicantEntry.save()

        # 修改学生状态
        studentEntry = Student.objects.get(id=applicantEntry.selectStudent.id)
        studentEntry.status = 1
        studentEntry.save()

        # 发送邮件
        mail_handler.sendEmail(applicantEntry)
        return HttpResponseRedirect('/applicant/list')
    except e:
        # 修改申请者状态
        applicantEntry = Applicant.objects.get(id=applicantId)
        applicantEntry.status = 0
        applicantEntry.save()

        # 修改学生状态
        studentEntry = Student.objects.get(id=applicantEntry.selectStudent.id)
        studentEntry.status = 0
        studentEntry.save()

        print(e.message)
        return HttpResponseRedirect('/applicant/list')

# 审核拒绝
def reject(request):
    if not authorization.authentic(request):
        return render_to_response('admin.html')
    
    applicantId = request.GET['id']
    if applicantId is None:
        return HttpResponseRedirect('/applicant/list')

    try:
        applicantEntry = Applicant.objects.get(id=applicantId)
        applicantEntry.status = 2
        applicantEntry.save()
        return HttpResponseRedirect('/applicant/list')
    except:
        return HttpResponseRedirect('/applicant/list')