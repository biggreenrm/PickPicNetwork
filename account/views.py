from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .forms import LoginForm

# Create your views here.


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

