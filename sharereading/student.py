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
from WebModel.models import StudentForm

from . import authorization

# 进入学生信息录入页面
def input(request):
    if not authorization.authentic(request):
        return render_to_response('admin.html')

    return render_to_response('input.html')

# 提交录入学生信息
@csrf_exempt
def submitInput(request):
    if not authorization.authentic(request):
        return render_to_response('admin.html')
    
    studentForm = StudentForm(request.POST)
    if studentForm.is_valid():
        studentForm.save()
        return HttpResponseRedirect('/students')
    else:
        return HttpResponse('提交失败！')

# 获取学生信息详细
def detail(request):
    if not authorization.authentic(request):
        return render_to_response('admin.html')

    studentId = request.GET['id']
    if studentId is None:
        return render_to_response('applicant_list.html')

    try:
        studentEntry = Student.objects.get(id=studentId)
        return render_to_response('student_detail.html', {'student':studentEntry})
    except:
        return render_to_response('applicant_list.html')

# 更新学生信息
@csrf_exempt
def update(request):
    if not authorization.authentic(request):
        return render_to_response('admin.html')
    
    studentId = request.POST['id']
    studentEntry = Student.objects.get(id=studentId)
    
    studentForm = StudentForm(request.POST, instance=studentEntry)
    if studentForm.is_valid():
        print("hello")
        studentForm.save()

    return HttpResponseRedirect('/applicant/list')

# 获取学生信息列表
def list(request):
    isAdmin = False
    if authorization.authentic(request):
        isAdmin =  True

    studentList = Student.objects.all()
    return render_to_response('student_list.html', {'studentList': studentList, 'isAdmin': isAdmin})