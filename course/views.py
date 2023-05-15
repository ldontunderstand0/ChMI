from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as lg, logout as lout

from lab6.models import User
from .models import *
from .forms import *

def yes_no(request, yes_or_no, answer_id):
    answer = User_Lession.objects.get(id=answer_id)
    answer.complete = yes_or_no
    answer.save()
    les = Lession.objects.get(id=answer.lession_id)
    course = Course.objects.get(id=les.course_id)
    return redirect('/course/lessions/' + str(course.id))

def answer(request, lession_id):
    ans = User_Lession.objects.filter(lession=lession_id)
    ans.delete()
    les = Lession.objects.get(id=lession_id)
    course_id = str(les.course_id)
    if request.method == "POST":
        try:
            form = User_LessionForm(request.POST, request.FILES)
            if form.is_valid():
                
                file = form['file'].value()

                answer = User_Lession(user=User.objects.get(id=request.user.id), lession=Lession.objects.get(id=lession_id), file=file, complete=-1)

                answer.save()

            return redirect('/course/lessions/' + course_id)
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = User_LessionForm()
        return render(request, "course/add.html", {'form': form, 'btn_name': 'Добавить ответ', 'path': 'lessions/' + str(course_id)})

def lessions(request, course_id):
    if request.method == "POST":
        try:
            form = LessionForm(request.POST, request.FILES)
            if form.is_valid():

                title = form['title'].value()
                file = form['file'].value()

                lessions = Lession.objects.filter(course=course_id)
                les_num = len(lessions)

                course = Course.objects.get(id=course_id)

                lession = Lession(course=course, num=les_num + 1, title=title, file=file)
                lession.save()

            return redirect('/course/lessions/' + course_id)
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        lessions = Lession.objects.filter(course=course_id)
        les_num = len(lessions)
        form = LessionForm()

        if not request.user.group_owner:
            user_lession = User_Lession.objects.filter(user=request.user.id)
        else:
            user_lession = []
            for i in lessions:
                for j in User_Lession.objects.filter(lession=i.id):
                    user_lession.append((j, User.objects.get(id=j.user_id)))

        return render(request, "course/lessions.html", {'form': form, 'lessions': lessions, 
        'les_num': les_num + 1, 'course_id': course_id, 'answers': user_lession})

def enter(request, course_id):

    user = User.objects.get(id=request.user.id)
    course = Course.objects.get(id=course_id)

    user_course = User_Course(user=user, course=course)
    user_course.save()

    return redirect('/course/cabinet')

def course(request, id):

    course = Course.objects.get(id=id)

    return render(request, "course/course.html", {'course': course})

def index(request):
    return render(request, "course/index.html")

def cabinet(request):
    products = []
    if request.user.admin:
        out = Course.objects.all()
        for product in out:
            products.append((
                product.id,
                product.title,
                product.prof,
                product.discipline,
                product.description,
                product.duration,
                product.mini_image.url,
                product.image.url,
                product.color
            ))
    elif request.user.group_owner:
        out = Course.objects.all()
        for product in out:
            if product.author_id == request.user.id:
                products.append((
                    product.id,
                    product.title,
                    product.prof,
                    product.discipline,
                    product.description,
                    product.duration,
                    product.mini_image.url,
                    product.image.url,
                    product.color,
                ))
    else:
        out = Course.objects.all()
        for product in out:
            if User_Course.objects.filter(course=product.id, user=request.user.id).exists():
                products.append((
                    product.id,
                    product.title,
                    product.prof,
                    product.discipline,
                    product.description,
                    product.duration,
                    product.mini_image.url,
                    product.image.url,
                    product.color
                ))

    return render(request, "course/cabinet.html", {'products': products, 'path': 'courses'})

def register(request):

    if request.method == "POST":
        try:
            form = RegisterForm(request.POST)
            if form.is_valid():

                email = form['email'].value()
                name = form['name'].value()
                surname = form['surname'].value()
                password = form['password'].value()

                group = User(email=email, name=name, surname=surname, password=password, username=email)
                group.save()
                return redirect('/course/')
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        form = RegisterForm()
        return render(request, "course/add.html", {'form': form, 'btn_name': 'Зарегистрироваться', 'path': 'reg'})

def login(request):
    if request.method == "POST":
        
        form = LoginForm(request.POST)
        if form.is_valid():

            email = form['email'].value()
            password = form['password'].value()

            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    lg(request, user)
                    return redirect('/course/')
                else:
                    return HttpResponse('Disabled account')
        return redirect('/course/')
        
    else:
        form = LoginForm()
        return render(request, "course/add.html", {'form': form, 'btn_name': 'Войти', 'path': 'login'})

def logout(request):
    lout(request)
    return redirect('/course/')

def table(request, path):
        search = request.GET.get("search")
        filter_ = request.GET.get("filter")
        names = []
        products = []

        match path:

            case 'users':
                out = User.objects.all()
                for product in out:
                    products.append((
                        product.id,
                        product.email,
                        product.name,
                        product.surname,
                        product.password,
                        product.group_owner,
                        product.admin
                    ))
                names = ['Id', 'Email', 'Имя', 'Фамилия', 'Пароль', 'Создатель курсов', 'Админ', '']

            case 'courses':
                out = Course.objects.all()
                for product in out:
                    if product.author.id == request.user.id:
                        products.append((
                            product.id,
                            product.title,
                            product.description,
                        ))
                names = ['id', 'title', 'description' '']

            case 'view_courses':

                if request.method == "POST":
                    try:
                        form = SearchForm(request.POST)
                        if form.is_valid():
                            search = form['search'].value()
                            out = Course.objects.all()
                            p = 0
                            c = 0
                            for product in out:
                                if search in product.discipline:
                                    if User_Course.objects.filter(course=product.id, user=request.user.id).exists():
                                        continue
                                    if product.prof == 'Профессия':
                                        p += 1
                                    else:
                                        c += 1
                                    products.append((
                                        product.id,
                                        product.title,
                                        product.prof,
                                        product.discipline,
                                        product.description,
                                        product.duration,
                                        product.mini_image.url,
                                        product.image.url,
                                        product.color
                                    ))
                            
                        return render(request, "course/courses.html", {'products': products, 
                        'path': path, 'form': form, 'search': search, 'prof': p, 'curs': c})

                    except Exception as e:
                        return HttpResponse(f"<h1>{e}</h1>")
                else:

                    form = SearchForm()

                    p = 0
                    c = 0

                    out = Course.objects.all()

                    if not isinstance(search, str):
                        search = ''

                    if not isinstance(filter_, str):
                        filter_ = 'all'

                    for product in out:
                       if search in product.discipline:
                            if User_Course.objects.filter(course=product.id, user=request.user.id).exists():
                                continue
                            if product.prof == 'Профессия':
                                p += 1
                            else:
                                c += 1
                            products.append((
                                product.id,
                                product.title,
                                product.prof,
                                product.discipline,
                                product.description,
                                product.duration,
                                product.mini_image.url,
                                product.image.url,
                                product.color
                            ))
                return render(request, "course/courses.html", {'products': products, 
                'path': path, 'search': '', 'form': form, 'search': search, 'prof': p, 'curs': c, 'filter': filter_})
                

        return render(request, "course/table.html", {'products': products, 'names': names, 'path': path})

def create(request, path):
    if request.method == "POST":
        try:
            match path:
                case 'users':
                    form = UserForm(request.POST)
                    if form.is_valid():

                        name = form['name'].value()
                        surname = form['surname'].value()
                        group_owner = form['group_owner'].value()
                        email = form['email'].value()
                        password = form['password'].value()
                        admin = form['admin'].value()

                        user = User(name=name, surname=surname, group_owner=group_owner, email=email, password=password, 
                        admin=admin, username=email)
                        user.save()

                case 'courses':
                    form = CourseForm(request.POST, request.FILES)
                    if form.is_valid():

                        title = form['title'].value()
                        prof = form['prof'].value()
                        discipline = form['discipline'].value()
                        duration = form['duration'].value()
                        description = form['description'].value()
                        author = request.user.id
                        mini_image = form['mini_image'].value()
                        image = form['image'].value()
                        color = form['color'].value()

                        course = Course(
                          title=title, 
                          author=User.objects.get(id=author), 
                          description=description,
                          prof=prof, 
                          discipline=discipline,
                          duration=duration,
                          image=image,
                          mini_image=mini_image,
                          color=color,
                        )
                        course.save()
                    path = 'cabinet'

            return redirect('/course/' + path)
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        match path:
            case 'users':
                form = UserForm()
                btn_name = 'Создать'
            case 'courses':
                path = 'cabinet'
                form = CourseForm()
                btn_name = 'Создать'
        return render(request, "course/add.html", {'form': form, 'btn_name': btn_name, 'path': path})

def update(request, path, id):
    if request.method == "POST":
        try:
            match path:
                case 'users':
                    form = UserForm(request.POST)
                    if form.is_valid():

                        name = form['name'].value()
                        surname = form['surname'].value()

                        User.objects.filter(id=id).update(name=name, surname=surname)
                case 'courses':
                    form = CourseForm(request.POST, request.FILES)
                    if form.is_valid():

                        title = form['title'].value()
                        prof = form['prof'].value()
                        discipline = form['discipline'].value()
                        description = form['description'].value()
                        duration = form['duration'].value()
                        mini_image = form['mini_image'].value()
                        image = form['image'].value()
                        color = form['color'].value()

                        course = Course.objects.get(id=id)
                        course.title = title
                        course.prof = prof
                        course.discipline = discipline
                        course.description = description
                        course.duration = duration
                        course.mini_image = mini_image
                        course.image = image
                        course.color = color

                        course.save()

                        
                    path = 'cabinet'
                case 'lessions':
                    form = LessionForm(request.POST, request.FILES)
                    if form.is_valid():

                        lession = Lession.objects.get(id=id)
                        course_id = lession.course_id

                        title = form['title'].value()
                        file = form['file'].value()

                        lession.title = title
                        lession.file = file

                        lession.save()
                        
                        return redirect('/course/' + path + '/' + str(course_id))
                        
                        return redirect('/course/' + path + '/' + str(course_id))
            return redirect('/course/' + path)
        except Exception as e:
            return HttpResponse(f"<h1>{e}</h1>")
    else:
        match path:
            case 'users':
                arr = User.objects.get(id=id)
                form = UserForm()
            case 'courses':
                arr = Course.objects.get(id=id)
                form = CourseForm(initial={
                    'title': arr.title,
                    'prof': arr.prof,
                    'discipline': arr.discipline,
                    'description': arr.description,
                    'duration': arr.duration,
                    'mini_image': arr.mini_image,
                    'image': arr.image,
                    'color': arr.color,
                })
                path = 'cabinet'
                
            case 'lessions':
                arr = Lession.objects.get(id=id)
                course_id = arr.course_id
                path += '/' + str(course_id)
                form = LessionForm(initial={
                    'title': arr.title,
                    'file': arr.file,
                })

        return render(request, "course/add.html", {'form': form, 'btn_name': 'Сохранить изменения', 
        'path': path, 'arr': arr})

def delete(request, path, id):
    try:
        match path:
            case 'users':
                user = User.objects.get(id=id)
                user.delete()
            case 'courses':
                course = Course.objects.get(id=id)
                course.delete()
            case 'view_courses':
                user_course = User_Course.objects.get(id=id)
                user_course.delete()
            case 'lessions':
                lession = Lession.objects.get(id=id)
                course_id = lession.course_id
                lession.delete()

                lessions = Lession.objects.filter(course_id=course_id)
                for i in lessions:
                    num = i.num
                    idx = i.id
                    Lession.objects.filter(id=idx).update(num=num-1)

                return redirect('/course/' + path + '/' + str(course_id))
            
            case 'answer':
                answer = User_Lession.objects.filter(lession=id)
                l = answer[0].lession_id
                p = Lession.objects.get(id=l).course_id

                answer.delete()
                return redirect('/course/lessions/' + str(p))
        return redirect('/course/' + path)
    except Exception as e:
        return HttpResponse(f"<h1>{e}</h1>")
