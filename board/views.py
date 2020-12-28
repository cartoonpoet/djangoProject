from django.shortcuts import render, redirect
import json
from  django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg, Max, Min, Sum
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from datetime import datetime
from .models import BoardList
import math
from django.core.paginator import Paginator


# models.py에서 만든 DB 테이블의 데이터를 처리하는 로직을 만들 수 있다.
# Create your views here.
# 로그인
def index(request):
    if request.method == 'GET':
        # 로그인 상태 확인
        if request.user.is_authenticated:
            return redirect('boardlist')
        else:
            return render(request, 'board/index.html')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pw']
        print('아이디 : '+email+', 비번 : '+password)

        user = authenticate(username=email, password=password)

        # 계정이 일치 확인
        if user is not None:
            login(request, user)
            res = JsonResponse({'message': 1})
            return res
        else:
            print('들어옴')
            messages.info(request, '아이디를 확인해주세요.')
            res = JsonResponse({'message': 0})
            return res


# 로그아웃
def logout_action(request):
    logout(request)
    return redirect('index')


# 회원가입
def signup(request):
    if request.method == 'GET':
        return render(request, 'board/signupform.html')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pw']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        nickname = request.POST['nickname']
        gender = request.POST['gender']

        # 해당 계정이 이미 존재하는지 확인하는 과정
        email_cnt = User.objects.filter(username=email).aggregate(Count('username'))
        nickname_cnt = User.objects.filter(nickname=nickname).aggregate(Count('nickname'))

        if email_cnt['username__count'] > 0:
            res = JsonResponse({'message': 0})
            return HttpResponse(res)
        elif nickname_cnt['nickname__count'] > 0:
            res = JsonResponse({'message': 1})
            return HttpResponse(res)
        else:
            res = JsonResponse({'message': 2})
            user = User.objects.create_user(username=email, password=password, last_name=last_name, first_name=first_name, gender=gender, nickname=nickname)
            user.save()
            return HttpResponse(res)


# 게시판 뷰
def boardlist(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            board_data = BoardList.objects.all().order_by('-id') # 게시물 정보
            board_cnt = BoardList.objects.all().aggregate(Count('id'))
            data_num = board_cnt['id__count'] # 게시물 개수
            board_cnt['id__count'] /= 10
            board_cnt['id__count'] = math.ceil(board_cnt['id__count']) # 페이지 수

            paginator = Paginator(board_data, 10)
            page = request.GET.get('page')
            if page is None:
                page = 1
            posts = paginator.get_page(page)

            # if request.GET.get('keyword') is not None: # 검색일 경우
            #     type = request.GET.get('type')
            #     keyword = request.GET.get('keyword')
            #
            #     if type == 'title':
            #         board_data = BoardList.objects.filter(board_title=keyword).all()
            #         board_cnt = BoardList.objects.filter(board_title=keyword).aggregate(Count('id'))
            #     elif type == 'contents':
            #         board_data = BoardList.objects.filter(board_contents=keyword).all()
            #         board_cnt = BoardList.objects.filter(board_contents=keyword).aggregate(Count('id'))
            #
            #     board_cnt['id__count'] /= 10
            #     board_cnt['id__count'] = math.ceil(board_cnt['id__count'])  # 페이지 수
            #
            #     paginator = Paginator(board_data, 10)
            #     page = request.GET.get('page')
            #     if page is None:
            #         page = 1
            #     posts = paginator.get_page(page)
            #
            #     return render(request, 'board/boardlist.html', {'ranges': range(1, board_cnt['id__count'] + 1), 'data_num': data_num, 'posts': posts, 'type': type, 'keyword': keyword})

            return render(request, 'board/boardlist.html', {'ranges':range(1, board_cnt['id__count']+1), 'data_num':data_num, 'posts':posts})
        else:
            return redirect('index')


# 게시물 작성하기
def board_edit(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'board/board_edit.html')
        else:
            return redirect('index')
    elif  request.method == 'POST':
        if request.user.is_authenticated:
            form_data = BoardList()
            form_data.email = request.user.username
            form_data.board_title = request.POST['title']
            form_data.board_contents = request.POST['content']

            files = request.FILES.getlist('file')

            for i in range(len(files)):
                if i == 0:
                    form_data.file1 = request.FILES.getlist('file')[i]
                elif i == 1:
                    form_data.file2 = request.FILES.getlist('file')[i]
                elif i == 2:
                    form_data.file3 = request.FILES.getlist('file')[i]
                elif i == 3:
                    form_data.file4 = request.FILES.getlist('file')[i]
                elif i == 4:
                    form_data.file5 = request.FILES.getlist('file')[i]

            form_data.save()

            return redirect('boardlist')
        else:
            return redirect('index')