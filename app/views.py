from contextlib import closing

from django.core.paginator import Paginator
from methodism import dictfetchall
from django.db import connection
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from nanoid import generate
from app.models.short import ShortUrls


def index(request):
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})


def dashboard(request, user_id=None, null_user=None):
    sql = '''SELECT au.id as user_id, au.email, au.last_login, au.is_active, su.long_url, su.short_url, su.used
            FROM auth_user au
            JOIN app_shorturls su
            group by au.id
             '''
    null = f"""SELECT * from app_shorturls as2 where as2.user_id is Null"""
    GetUserLinks = f'''SELECT long_url, short_url, used FROM app_shorturls as2 WHERE user_id == {user_id}'''

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchall(cursor)
        if null_user == 'True':
            cursor.execute(null)
        null_users = dictfetchall(cursor)
        if user_id:
            cursor.execute(GetUserLinks)
        user_urls_result = dictfetchall(cursor)

        displayed_emails = set()
        unique_result = []
        for i in result:
            if i['email'] not in displayed_emails:
                unique_result.append(i)
                displayed_emails.add(i['email'])

        pagination = result
        paginator = Paginator(pagination, 50)
        page_number = request.GET.get("page", 1)
        paginated = paginator.get_page(page_number)

        ctx = {
            'user_urls': user_urls_result,
            'user_id': user_id,
            'null_users': null_users, 'null_user_status': null_user, "roots": paginated, "pos": "list"
        }
    return render(request, 'dashboard/tables.html', ctx)


def user_urls(request, user_id=None):
    GetUserLinks = f'''SELECT long_url, short_url, used FROM app_shorturls as2 WHERE user_id == {user_id}'''

    with closing(connection.cursor()) as cursor:
        cursor.execute(GetUserLinks)
        user_urls_result = dictfetchall(cursor)

        ctx = {
            'user_urls': user_urls_result,
            'user_id': user_id,
        }
    return render(request, 'dashboard/tables.html', ctx)


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

        new_url = ShortUrls(long_url=long_url, short_url=CustomShortUrl or generate(size=5), user=user)
        new_url.save()
        return HttpResponse(new_url.short_url)
    raise Http404("Page Not Found")


def qr_short_url(request):
    if request.method == "POST":
        long_url = request.POST['qrInput']
        shortUrl = generate(size=5)
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
