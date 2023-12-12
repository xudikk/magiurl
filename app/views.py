from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from methodism import generate_key
from app.models.short import ShortUrls


def index(request):
    return render(request, 'index.html', {})


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

        new_url = ShortUrls(long_url=long_url, short_url=CustomShortUrl or generate_key(size=4), user=user)
        new_url.save()
        return HttpResponse(new_url.short_url)
    raise Http404("Page Not Found")


def qr_short_url(request):
    if request.method == "POST":
        long_url = request.POST['qrInput']
        shortUrl = generate_key(size=4)
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
