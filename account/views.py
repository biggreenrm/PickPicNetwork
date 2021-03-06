from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action
from .models import Profile, Contact
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm


def register(request):
    """Регистрация пользователя.
    
    Заполнение формы в блоке 'else'. Проверка правильности формы. Сохранение пользователя
    и пароля без сохранения в БД (применяется шифрование введённого пароля, т.к. в БД нельзя
    хранить наглядные пароли). Финальное сохранение пользователя и пароля в БД и рендер страницы
    окончания регистрации.
    """
    
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаём нового пользователя без сохранения в БД
            new_user = user_form.save(commit=False)
            # Задаём пользователю зашифрованный пароль
            new_user.set_password(user_form.cleaned_data["password"])
            # Сохраняем пользователя в БД
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit_account(request):
    """Редактирование аккаунта.
    
    Путём отправки запроса, имеющем данные о том, какой пользователь его отправляет, загружается
    форма для редактирования аккаунта и затем профиля. После редактирования они отправляются методом
    POST с аргументами содержащими данные о том, кто есть пользователь и редактируемой им информацией.
    После проверки на правильность заполнения форм либо обе сохраняются и рендерится страница с сообщением
    об успешном проведении операции, либо не сохраняются и появляется сообщение об ошибке.  
    """
    
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form,
         "profile_form": profile_form},
    )


@login_required
def dashboard(request):
    #По умолчанию отображаются все действия, кроме собственных
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    
    #Если текущий пользователь подписался на кого-то - отобразить действия только этих пользователей
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    
    #Таким образом сокращается количество обращений ко связанным объектам, уменьшая время запросов
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10]
    return render(request, "account/dashboard.html",
                  {"section": "dashboard",
                   "actions": actions})


def user_login(request):
    """Логирование пользователя.
      
    Пользователь отправляет запрос и получает форму логина, которая заполняется и отправляется
    на сервер POST-запросом. Данные в форме приводятся к единому формату, после чего функция
    authenticate проверяет есть ли в базе юзернейм с введённым паролем. Если есть, он логининится
    в систему, если не логинится, то в зависимости от причины произошедшего рисуется соответствующий
    HttpResponse.   
    """
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        # Этот метод обрезает лишние данные и проверяет их, подгоняя по форматированию
        if form.is_valid():
            cd = (form.cleaned_data)  
            user = authenticate(
                request,
                username=cd["username"],
                password=cd["password"]
            ) 
        if user is not None:
            if user.is_active:
                # В отличии от authenticate() эта функция сохраняет пользовтеля
                # в сессии, а не ищет его наличие в БД
                login(request, user)
                return HttpResponse("Authenticated succesfully")
            else:
                return HttpResponse("Disabled account")
        else:
            return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


# View для отображения списка активных пользователей
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  "account/user/list.html",
                  {'section': 'people',
                   'users': users})


# View вынимает пользователя из БД, принимая на вход запроси его имя
@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request,
                  "account/user/detail.html",
                  {'section': 'people',
                   'user': user})
    

@ajax_required
@require_POST
@login_required
def user_follow(request):
    """ Подписка на пользователя.
    
    Из POST-запроса извлекается id пользователя, на которого нужно подписаться/отписаться,
    а также тип действия. Если все параметры получены, из БД достаётся пользователь по id.
    В случае, если действие - это подписка, создаётся строка в таблице (модели) Contacts,
    связывающая двух пользователей. Если действие - это отписка, то строка в таблице
    удаляется.
    """
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})
