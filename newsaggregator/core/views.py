# your_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Headline, Bookmark, Rating, Contact
from django.contrib import messages
from .decorators import custom_login_required  # Import the custom decorator
import requests
from bs4 import BeautifulSoup as BSoup
from django.views.decorators.csrf import csrf_exempt
import json

# def base_view(request):
#     return render(request, 'core/base.html')

@custom_login_required
def scrape(request, name):
    Headline.objects.all().delete()
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = f"https://www.theonion.com/{name}"
    content = session.get(url).content
    soup = BSoup(content, "html.parser")
    News = soup.find_all("div", {"class": "sc-cw4lnv-13 hHSpAQ"})
    for article in News:
        main = article.find_all("a", href=True)
        linkx = article.find("a", {"class": "sc-1out364-0 dPMosf js_link"})
        link = linkx["href"]
        titlex = article.find("h2", {"class": "sc-759qgu-0 cvZkKd sc-cw4lnv-6 TLSoz"})
        title = titlex.text
        imgx = article.find("img")["data-src"]
        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = imgx
        new_headline.save()
    return redirect("../")

# @custom_login_required
# def news_list(request):
#     headlines = Headline.objects.all().order_by('-id')
#     swiper = Headline.objects.all()[:4]
#     user_bookmarked_headline_ids = []
#     if request.user.is_authenticated:
#         user_bookmarked_headline_ids = request.user.bookmark_set.values_list('headline_id', flat=True)
#     page = request.GET.get('page', 1)
#     num_of_items = 9
#     paginator = Paginator(headlines, num_of_items)
#     try:
#         headlines_obj = paginator.page(page)
#     except PageNotAnInteger:
#         headlines_obj = paginator.page(1)
#     except EmptyPage:
#         headlines_obj = paginator.page(paginator.num_pages)
#     context = {
#         "object_list": headlines_obj,
#         "paginator": paginator,
#         'swiper': swiper,
#         'user_bookmarked_headline_ids': user_bookmarked_headline_ids,
#     }
#     return render(request, "core/index.html", context)
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Headline
def news_list(request):
    headlines = Headline.objects.all().order_by('-id')
    swiper = Headline.objects.all()[:4]
    page = request.GET.get('page', 1)
    num_of_items = 9
    paginator = Paginator(headlines, num_of_items)
    try:
        headlines_obj = paginator.page(page)
    except PageNotAnInteger:
        headlines_obj = paginator.page(1)
    except EmptyPage:
        headlines_obj = paginator.page(paginator.num_pages)
    context = {
        "object_list": headlines_obj,
        "paginator": paginator,
        'swiper': swiper,
    }
    return render(request, "core/index.html", context)


# @custom_login_required
def index(request):
    Headline.objects.all().delete()
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = f"https://www.theonion.com/latest"
    content = session.get(url).content
    soup = BSoup(content, "html.parser")
    News = soup.find_all("div", {"class": "sc-cw4lnv-13 hHSpAQ"})
    count = 0
    for article in News:
        count += 1
        if count <= 8:
            main = article.find_all("a", href=True)
            linkx = article.find("a", {"class": "sc-1out364-0 dPMosf js_link"})
            link = linkx["href"]
            titlex = article.find("h2", {"class": "sc-759qgu-0 cvZkKd sc-cw4lnv-6 TLSoz"})
            title = titlex.text
            imgx = article.find("img")["data-src"]
            new_headline = Headline()
            new_headline.title = title
            new_headline.url = link
            new_headline.image = imgx
            new_headline.save()
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    return render(request, "core/index.html", context)

# @custom_login_required
def about(request):
    context = {}
    return render(request, "core/about.html", context)

# @custom_login_required
def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact()
        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.message = message
        contact.save()
        messages.success(request, "Thanks for contacting us")
        return redirect("/contact.html")
    return render(request, "core/contact.html")

# @custom_login_required
def advertise(request):
    context = {}
    return render(request, "core/advertise.html", context)

# @custom_login_required
def privacy(request):
    context = {}
    return render(request, "core/privacy.html", context)

# @custom_login_required
def view_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('headline')
    if bookmarks.exists():
        context = {'bookmarks': bookmarks}
    else:
        context = {'message': 'You have no bookmarks yet.'}
    return render(request, 'core/bookmarks.html', context)

@csrf_exempt
# @custom_login_required
def bookmark_article(request, headline_id):
    if request.method == 'POST':
        headline = get_object_or_404(Headline, id=headline_id)
        Bookmark.objects.get_or_create(user=request.user, headline=headline)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
# @custom_login_required
def remove_bookmark(request, headline_id):
    if request.method == 'POST':
        Bookmark.objects.filter(user=request.user, headline_id=headline_id).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

import json
# @custom_login_required
@csrf_exempt
def rate_headline(request, headline_id):
    if request.method == 'POST':
        headline = get_object_or_404(Headline, id=headline_id)
        try:
            data = json.loads(request.body)
            rating_value_str = data.get('rating')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON'}, status=400)
        if rating_value_str is not None:
            try:
                rating_value = int(rating_value_str)
            except ValueError:
                return JsonResponse({'status': 'fail', 'message': 'Invalid rating value'}, status=400)
        else:
            return JsonResponse({'status': 'fail', 'message': 'Rating value is missing'}, status=400)
        rating, created = Rating.objects.get_or_create(user=request.user, headline=headline)
        rating.rating = rating_value
        rating.save()
        ratings = Rating.objects.filter(headline=headline).exclude(rating__isnull=True)
        headline.rating_count = ratings.count()
        headline.average_rating = sum(r.rating for r in ratings) / headline.rating_count if headline.rating_count > 0 else 0
        headline.save()
        return JsonResponse({'status': 'success', 'average_rating': headline.average_rating, 'rating_count': headline.rating_count})
    return JsonResponse({'status': 'fail'}, status=400)

# @custom_login_required
def top_rated_articles(request):
    top_rated_articles = Headline.objects.filter(average_rating__gte=3.5).order_by('-average_rating')
    paginator = Paginator(top_rated_articles, 9)
    page = request




import requests
from django.http import JsonResponse

def fetch_article_content(request):
    url = request.GET.get('url')
    if not url:
        return JsonResponse({'error': 'URL parameter is missing'}, status=400)

    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'content': content})
