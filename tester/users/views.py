from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import User
from .forms import CustomUserCreationForm, ResetPassForm, ChangePassForm, ProfileForm
from django.contrib.auth.decorators import login_required
from datetime import date


def create_groups(request):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    new_group = Group(name="Editors")
    new_group.save()

    # Get the content type for the Article model
    test_content_type = ContentType.objects.get_for_model(User)

    # Fetch the required permissions
    add_permission = Permission.objects.get(codename="add_test", content_type=test_content_type)
    change_permission = Permission.objects.get(codename="change_test", content_type=test_content_type)
    delete_permission = Permission.objects.get(codename="delete_test", content_type=test_content_type)

    new_group.permissions.add(add_permission, change_permission, delete_permission)
    new_group.save()


@login_required
def edit_profile(request):
    user = request.user
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            return redirect('my_profile')
    now = date.today().year
    from_year = now - 100
    context = {'form': form, 'now': now, 'from_year': from_year}

    return render(request, 'users/profile/profile_form.html', context)


@login_required
def user_profile(request):
    user = request.user

    context = {'user': user,}
    return render(request, 'users/profile/profile.html', context)


def landing_login(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Указанный пользователь не зарегистрирован!')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return redirect('/')


def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = {}

    return render(request, 'landing.html', context)


# Главная страница для авторизованных пользователей
def home(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'users/home.html', context)
    else:
        return redirect('login')


# Страница авторизации
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Пользователь с таким логином не найден!')
            print('Пользователь с таким логином не найден!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
    return redirect('login')


# Страница подтверждения регистрации
def register_confirmation(request):
    if request.user.is_authenticated:
        context = {'username': request.user.username, 'password': request.session.get('user_pass')}
        return render(request, 'users/register_confirmation.html', context)
    else:
        return redirect('login')


# Регистрация аккаунта
def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        data = request.POST
        data._mutable = True
        if data.get('first_name') != '' and data.get('patronymic') != '' and data.get('last_name') != '':
            data['username'] = data.get('first_name')[0].lower() + data.get('patronymic')[0].lower() + data.get('last_name').lower()
            data._mutable = False
            updated_request = data.copy()

            updated_form = CustomUserCreationForm(updated_request)

            if updated_form.is_valid():
                user = form.save(commit=False)
                user.save()

                messages.success(request, f'Аккаунт успешно создан!')

                login(request, user)
                request.session['user_pass'] = data.get("password1")
                return HttpResponseRedirect('confirmation')
            else:
                print(updated_form.errors)
                messages.error(request, 'Обнаружены некорректно заполненные поля формы!')
                messages.error(request, form.errors)
        else:
            messages.error(request, 'Укажите ФИО!')
            messages.error(request, form.errors)

    context = {'page': page, 'form': form,}
    return render(request, 'users/login_register.html', context)


def password_change_pre_done(request):
    if request.user.is_authenticated:
        request.session['status'] = 'pass_change'
        return redirect('confirmation_pass')
    return redirect('login')


def password_change_done(request):
    if request.user.is_authenticated:
        if request.session.get('status') == 'pass_change':
            print('Отображаю подтверждение')
            context = {'status': 'pass_change'}
            return render(request, 'users/password/password_change_done.html', context)
        else:
            messages.success(request, f'Пароль успешно изменен.')
            return redirect('home')
    return redirect('login')


# Сброс пароля
def reset_pass(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = ResetPassForm()

    if request.method == 'POST':
        form = ResetPassForm(request.POST)
        if form.is_valid():
            username = request.POST['username'].lower()
            year_of_birth = request.POST['year_of_birth']
            new_password = request.POST['new_password']

            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, 'Пользователь с таким логином не найден!')
            if str(user.year_of_birth) == str(year_of_birth):
                user.set_password(new_password)
                user.save()
            else:
                messages.error(request, 'Указан неверный год рождения пользователя!')

            logout(request)
            print('Разлогинился')
            login(request, user)
            print(f'Залогинился как {user}')
            request.session['status'] = 'pass_change'
            return redirect('confirmation_pass')
            # return HttpResponseRedirect('confirmation_pass')
        else:
            print(form.errors)
            print(form.non_field_errors())
            messages.success(request, 'Во время регистрации возникла ошибка')
            messages.error(request, form.errors)
    now = date.today().year
    from_year = now - 100
    context = {'now': now, 'from_year': from_year}
    return render(request, 'users/password/password_reset_form.html', context)


# Смена пароля
def change_pass(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = ChangePassForm()

    if request.method == 'POST':
        print('POST запрос')
        form = ChangePassForm(request.POST)
        if form.is_valid():
            username = request.user.username
            old_password = request.POST['old_password']
            new_password_1 = request.POST['new_password_1']
            new_password_2 = request.POST['new_password_2']

            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, 'Пользователь с таким логином не найден!')
                return redirect('logout')
            if user.check_password(old_password):
                if new_password_1 == new_password_2:
                    user.set_password(new_password_1)
                    user.save()

                    logout(request)
                    login(request, user)
                    request.session['status'] = 'pass_change'
                    return redirect('confirmation_pass')
                else:
                    messages.error(request, 'Новые пароли не совпадают друг с другом!')
            else:
                messages.error(request, 'Указан неверный текущий пароль!')
        else:
            print(form.errors)
            print(form.non_field_errors())
            messages.success(request, 'В форме обнаружены ошибки.')
            messages.error(request, form.errors)

    return render(request, 'users/password/password_change_form.html')