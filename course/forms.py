from django import forms
from lab6.models import User


class SearchForm(forms.Form):
    search = forms.CharField(label="", empty_value="", required=False)


class User_LessionForm(forms.Form):
    file = forms.FileField(label="Файл", required=False)


class LessionForm(forms.Form):
    title = forms.CharField(label="Название", max_length=41)
    file = forms.FileField(label="Файл", required=False)


class LoginForm(forms.Form):
    email = forms.EmailField(label="email", max_length=20)
    password = forms.CharField(label="password", max_length=20, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(label="email", max_length=20)
    name = forms.CharField(label="name", max_length=20)
    surname = forms.CharField(label="surname", max_length=20)
    password = forms.CharField(label="password", max_length=20, widget=forms.PasswordInput)


class UserForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=20)
    name = forms.CharField(label="Имя", max_length=20)
    surname = forms.CharField(label="Фамилия", max_length=20)
    password = forms.CharField(label="Пароль", max_length=20, widget=forms.PasswordInput)
    group_owner = forms.IntegerField(label="Создатель курсов (0 или 1)")
    admin = forms.IntegerField(label="Администратор (0 или 1)")


class CourseForm(forms.Form):
    title = forms.CharField(label="Название курса", max_length=41)
    prof = forms.CharField(label="Профессия / Курс", max_length=40)
    discipline = forms.CharField(label="Дисциплина", max_length=40)
    description = forms.CharField(label="Описание", max_length=150)
    duration = forms.CharField(label="Длительность", max_length=20)
    mini_image = forms.ImageField(label="Миниатюра курса", required=False)
    image = forms.ImageField(label="Изображение курса", required=False)
    color = forms.CharField(label="Цвет курса", max_length=41)
    