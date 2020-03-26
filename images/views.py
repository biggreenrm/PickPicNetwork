from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action
from common.decorators import ajax_required

# Create your views here.
@login_required
def image_list(request):
    """Список изображений.
      
    В переменную складываются все объекты модели Image. Paginator делит весь объём на пулы по 8 штук.
    Далее пробуем вынуть из GET-запроса номер страницы, которую хочет получить пользователь. Если 8 штук
    не набирается, значит "страниц меньше чем одна" и на первой рисуется то, что есть. Если странциа больше,
    чем насчитал Paginator - рисуется '' (то есть ничто). Дальше происходит рендеринг страниц, где страница
    с ajax вложена в html-страницу со списком.
    """
      
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                   {'section': 'images', 'images': images})


# view достающее объект из БД(Images) по id и slug, и рисующее его
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request, "images/image/detail.html", {"section": "images", "image": image}
    )


@login_required
def image_create(request):
    """Создание изображения.
     
    Подгружается форма для создания изображений, где картинка берётся из
    GET-запроса (при помощи jQuery-скрипта по выниманию картинок с других
    ресурсов). Когда запрос становится не GET, а POST - форма проверяется
    на правильность, форматируется по единому образцу, сохраняется без
    добавления в БД, получает имя юзера исходя из того, кто отправляет
    запрос. После всего этого она уже сохраняется в БД как объект,
    пользователь редиректится на ту страницу, которая будет являться
    адресом данного изображения.
    """
    
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, "Image added succesfully")
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request, "images/image/create.html", {"form": form})


@ajax_required
@login_required
@require_POST
def image_like(request):
    """Лайк для изображений.
      
    Из POST-запроса вынимаются параметры id и action, происходит обращение к БД с попыткой найти
    изображение с указанным id. И если действие в POST-запросе 'like' - к объекту БД он добавляется,
    в противном случае - удаляется. После всего view возращает JsonResponse в котором сообщает,
    что всё чики-пики.
    """
    
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except:
            pass
    return JsonResponse({"status": "ok"})

