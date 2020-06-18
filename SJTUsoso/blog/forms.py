from django import forms
from captcha.fields import CaptchaField
from .models import Blog, BlogType
from ckeditor.fields import RichTextFormField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

class UserspaceForm(forms.Form):
    gender = (
        ('private', '内緒だよ〜'),
        ('male', '男'),
        ('female', '女'),
    )
    nickname = forms.CharField(label="用户昵称", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="电话号码", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender, widget=forms.Select(attrs={'class': 'form-control'}))
    intro = forms.CharField(label="个性签名", max_length=1024, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

class UpdateAvatarForm(forms.Form):
    img = forms.ImageField(label="头像", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

class UploadCoverForm(forms.Form):
    img = forms.ImageField(label="封面", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

class WBlogForm(forms.Form):
    title = forms.CharField(label="文章标题", widget=forms.TextInput(attrs={'class': 'form-control'}))
    # blog_type = forms.ChoiceField(label="文章类型", choices=BlogType, widget=forms.Select(attrs={'class': 'form-control'}))
    content = RichTextFormField()
    # created_time = forms.DateTimeField(label="时间", widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    #img_url = forms.ImageField(label="封面", widget=forms.FileInput(attrs={'class': 'form-control'}))