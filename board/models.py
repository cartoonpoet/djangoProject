from django.db import models


# 데이터베이스 테이블을 만들고 그안의 필드를 생성 및 수정하는 역할을 함
class Account(models.Model):
    email = models.EmailField(max_length=40, unique=True)
    pw = models.CharField(max_length=40)
    last_name = models.CharField(max_length=5)
    first_name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=40)
    gender = models.CharField(max_length=10)

    class Meta:
        db_table = 'account_info'


class BoardList(models.Model):
    email = models.EmailField(max_length=40, unique=True)
    nickname = models.CharField(max_length=20)
    board_num = models.IntegerField()
    board_title = models.CharField(max_length=50)
    board_contents = models.TextField()
    board_date =models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'boardlist'
