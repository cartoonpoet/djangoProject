from django.shortcuts import render, redirect
import json
from .models import Account
from django.views import View
from  django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count, Avg, Max, Min, Sum
from django.core import serializers
from django.db.models import Q
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout as auth_logout
import jwt
from .my_settings import SECRET_KEY, ALGORITHM

# models.py에서 만든 DB 테이블의 데이터를 처리하는 로직을 만들 수 있다.
# Create your views here.


def index(request):
    if request.method == 'GET':
        return render(request, 'board/index.html')
    elif request.method == 'POST':
        account = Account()
        account.email = request.POST['email']
        account.pw = request.POST['pw']

        # 계정이 일치 확인
        email_list = Account.objects.filter(Q(email=account.email) & Q(pw=account.pw)).aggregate(Count('email'))
        if email_list['email__count'] == 1: # ID/PW 일치하면 로그인
            # 사용자 데이터 불러온다.
            datas = Account.objects.filter(Q(email=account.email) & Q(pw=account.pw)).values()

            # 사용자 데이터 직렬화
            data = {'email':datas[0]['email'], 'fullname':datas[0]['last_name']+datas[0]['first_name'], 'nickname':datas[0]['nickname']}

            # 토큰 발행
            token = jwt.encode(data, SECRET_KEY, ALGORITHM)
            token = token.decode('utf-8')

            res = JsonResponse({'message': 1})
            res.set_cookie('access_token', token)
            login = AuthenticationForm(request, request.POST)

            # 로그인
            if login.is_valid():
                auth_login(request, login.get_user())
            return HttpResponse(res)
        else: # ID가 없으면
            res = JsonResponse({'message': 0})
            return HttpResponse(res)

def logout(request):
    print(11)
    if request.method == 'POST':
        reset = ''
        res = JsonResponse({'message:'
                            ' 0'})
        res.set_cookie('access_token', reset)
        #auth_logout(request)
        return HttpResponse(res)

def signup(request):
    if request.method == 'GET':
        return render(request, 'board/signupform.html')

    elif request.method == 'POST':
        print('회원가입')
        account = Account()
        account.email = request.POST['email']
        account.pw = request.POST['pw']
        account.last_name = request.POST['last_name']
        account.first_name = request.POST['first_name']
        account.nickname = request.POST['nickname']
        account.gender = request.POST['gender']

        # 해당 계정이 이미 존재하는지 확인하는 과정
        email_cnt = Account.objects.filter(email=account.email).aggregate(Count('email'))
        nickname_cnt = Account.objects.filter(nickname=account.nickname).aggregate(Count('nickname'))

        if email_cnt['email__count'] > 0:
            context = {'message': 0}
            return HttpResponse(json.dumps(context), content_type="application/json")
        elif nickname_cnt['nickname__count'] > 0:
            context = {'message': 1}
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            account.save()
            context = {'message': 2}
            return HttpResponse(json.dumps(context), content_type="application/json")


def boardlist(request):
    if request.method == 'GET':
        print('board 들어옴')
        return render(request, 'board/boardlist.html')

