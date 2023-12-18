from contextlib import closing

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from methodism import dictfetchall
from django.db import connection
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from methodism import generate_key
from app.models.short import ShortUrls


def index(request):
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})


def dashboard(request, user_id=None):
    user_urls_result = []

    if user_id or user_id == 0:
        GetUserLinks = f'''
                        SELECT id, long_url, short_url, used FROM app_shorturls as2 
                        {f'WHERE user_id == {user_id}' if user_id else 'WHERE user_id is null'}
                      '''
        with closing(connection.cursor()) as cursor:
            cursor.execute(GetUserLinks)
            user_urls_result = dictfetchall(cursor)

    with closing(connection.cursor()) as cursor:
        page_number = request.GET.get("page", 1)
        limit = 50
        offset = (page_number - 1) * limit
        sql = f'''
            Select id as user_id, is_active,
            CASE 
                when is_active is false then 'bg-gradient-danger' 
                else 'bg-gradient-success' 
                END  as html_class,
            last_login
            from auth_user 
            order by id DESC 
            limit {limit} offset {offset}
         '''
        cursor.execute(sql)
        result = dictfetchall(cursor)

        pagination = result
        paginator = Paginator(pagination, limit)
        paginated = paginator.get_page(page_number)

        ctx = {
            'user_urls': user_urls_result,
            'user_id': user_id,
            "roots": paginated,
            "pos": "list"
        }
    if request.user.is_staff:
        return render(request, 'dashboard/tables.html', ctx)
    return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('/')


def shorten_url(request):
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        long_url = request.POST['urlInput']
        CustomShortUrl = request.POST.get('backHalfInput', None)

        existing_url = ShortUrls.objects.filter(short_url=CustomShortUrl).first()
        if existing_url:
            return HttpResponse("The custom short URL already exists.", status=403)

        new_url = ShortUrls(long_url=long_url, short_url=CustomShortUrl or generate_key(size=3), user=user)
        new_url.save()
        return HttpResponse(new_url.short_url)
    raise Http404("Unusable page")


def qr_short_url(request):
    if request.method == "POST":
        long_url = request.POST['qrInput']
        shortUrl = generate_key(size=3)
        user = request.user if request.user.is_authenticated else None

        existing_url = ShortUrls.objects.filter(short_url=shortUrl).first()
        if existing_url:
            return JsonResponse({'error': 'The custom short URL already exists.'}, status=403)

        new_url = ShortUrls(long_url=long_url, short_url=shortUrl, user=user)
        new_url.save()

        return JsonResponse({'short_url': shortUrl})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def go_to(request, pk):
    try:
        url_details = ShortUrls.objects.get(short_url=pk)
        url_details.used += 1
        url_details.save()
        return redirect(url_details.long_url)
    except ShortUrls.DoesNotExist:
        raise Http404("Short URL does not exist")


def banned(request, pk):
    user = User.objects.filter(id=pk).first()
    if not user or request.user == user:
        return redirect('dashboard')
    user.is_active = not user.is_active
    user.save()
    return redirect('dashboard')


def delete_url(request, url_id):
    url = ShortUrls.objects.filter(id=url_id).first()
    if not url:
        return redirect('user_urls', user_id=0)
    user_id = url.user_id
    url.delete()
    return redirect('user_urls', user_id=user_id or 0)
