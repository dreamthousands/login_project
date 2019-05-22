from django.db import models

# Create your models here.

class UserInfo(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女')
    )
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    sex = models.CharField(max_length=10, choices=gender, default='男')
    email = models.EmailField(unique=True)
    reg_time = models.DateTimeField(auto_now_add=True)
    has_confirm = models.BooleanField(default=False)

    def __str__(self):
        return '{username:%s}' % self.username

    class Meta:
        db_table = 'user_info'
        ordering = ['reg_time']

class ConfirmString(models.Model):

    code = models.CharField(max_length=256)
    user = models.OneToOneField('UserInfo', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"