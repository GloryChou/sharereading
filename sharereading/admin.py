# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
import hashlib
from io import BytesIO

from WebModel.models import Admin
from WebModel.models import Applicant
from . import authorization
from . import vericode

 
def index(request):
    return render_to_response('admin.html')

# 登录
@csrf_exempt
def login(request):  
    request.encoding='utf-8'

    # 账号、密码验证
    userName = request.POST['userName']
    password = request.POST['password']
    
    ctx = {}
    if userName == '':
        ctx['hint'] = '用户名不能为空'
        return render_to_response('admin.html', ctx)

    if password == '':
        ctx['hint'] = '密码不能为空'
        return render_to_response('admin.html', ctx)
    else:
        md5Encriptor = hashlib.md5()
        md5Encriptor.update(password.encode('utf-8'))
        encriptPwd = md5Encriptor.hexdigest()
        
        try:
            adminEntry = Admin.objects.get(userName=userName)
        except:
            ctx['hint'] = '账户不存在'
            return render_to_response('admin.html', ctx)
            
        realPwd = adminEntry.password
        
        if not encriptPwd[0:16] == realPwd:
            ctx['hint'] = '密码错误'
            return render_to_response('admin.html', ctx)

        
        vericode = request.session.get("vericode").upper()
        submitcode = request.POST.get("vericode").upper()
        if not submitcode == vericode:
            ctx['hint'] = '验证码错误'
            return render_to_response('admin.html', ctx)


        request.session["user"] = adminEntry.userName
        request.session["password"] = adminEntry.password

        return HttpResponseRedirect("/applicant/list")

# 注销
def logout(request):
    try:
        del request.session['user']
        del request.session['password']
    except KeyError:
        print("ERROR")
    return render_to_response('admin.html')

# 获取验证码
def verifyCode(request):
    f = BytesIO()
    code,image = vericode.veri_code()
    image.save(f,'jpeg')
    request.session['vericode'] = code
    return HttpResponse(f.getvalue())