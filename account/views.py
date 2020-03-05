from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm

# Create your views here.


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаём нового пользователя без сохранения в БД
            new_user = user_form.save(commit=False)
            # Задаём пользователю зашифрованный пароль
            new_user.set_password(user_form.cleaned_data["password"])
            # Сохраняем пользователя в БД
            new_user.save()
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = (
                form.cleaned_data
            )  # этот метода обрезает лишние данные и проверяет их, подгоняя по форматированию
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )  # данная функция проверяет есть ли в базе данный юзернейм с указанным паролем. Есть - окей. Нет - вернётся None
        if user is not None:
            if user.is_active:
                login(
                    request, user
                )  # в отличии от authenticate() эта функция сохраняет пользовтеля в сессии, а не ищет его наличие в БД
                return HttpResponse("Authenticated succesfully")
            else:
                return HttpResponse("Disabled account")
        else:
            return HttpResponse("Invalid login")
    else:  # на практике сначала будет выполняться вот эта часть кода, когда пользователь отправляет GET-запрос
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})
    # с помощью section каким-то образом становится понятно какой раздел просматривает пользователь (хз как)

