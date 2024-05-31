from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from core.models import Headline

from datetime import datetime

from core.models import Contact
from django.template.loader import render_to_string
from django.core.mail import send_mail


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Headline, Bookmark
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
#view for scraping new

def scrape(request, name):
    Headline.objects.all().delete() #remove all existing records from table
    session = requests.Session()
    #useragent helps server to identify origin of request
    #we are imitating request as google bot
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    #google bot is crawler program
    #session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    url = f"https://www.theonion.com/{name}"
    content = session.get(url).content
    #print(content)#raw content
    soup = BSoup(content, "html.parser")
    #print(soup)
    # finding all new div using common class
    News = soup.find_all("div", {"class": "sc-cw4lnv-13 hHSpAQ"})
    print(News)
    for article in News:
    #extracting news link,img url,title for each news
        main = article.find_all("a", href=True)
        linkx = article.find("a", {"class": "sc-1out364-0 dPMosf js_link"})
        link = linkx["href"]
        titlex = article.find("h2", {"class": "sc-759qgu-0 cvZkKd sc-cw4lnv-6 TLSoz"})
        title = titlex.text
        imgx = article.find("img")["data-src"]
        #storing extracted data to model
        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = imgx
        new_headline.save()
        #saving details to table
    return redirect("../")

@login_required(login_url='userauths:sign-in')
def news_list(request):
    # Fetch all headlines in reverse order
    headlines = Headline.objects.all().order_by('-id')
    swiper = Headline.objects.all()[:4]

    # Get the list of bookmarked headline IDs for the current user
    user_bookmarked_headline_ids = []
    if request.user.is_authenticated:
        user_bookmarked_headline_ids = request.user.bookmark_set.values_list('headline_id', flat=True)

    # Pagination logic
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
        'user_bookmarked_headline_ids': user_bookmarked_headline_ids,
    }
    return render(request, "core/index.html", context)

@login_required(login_url='userauths:sign-in')
def index(request):
    Headline.objects.all().delete()
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = f"https://www.theonion.com/latest"
    content = session.get(url).content
    soup = BSoup(content, "html.parser")

    News = soup.find_all("div", {"class": "sc-cw4lnv-13 hHSpAQ"})
    count=0
    for article in News:
        count=count+1

        if count<=8:
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
            new_headline.save() ##saving each record to news_headline
    
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    return render(request, "core/index.html", context)

@login_required(login_url='userauths:sign-in')
def about(request):
    context={

    }
    return render(request, "core/about.html", context)

@login_required(login_url='userauths:sign-in')
def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone= request.POST.get('phone')
        message = request.POST.get('message')
        contact=Contact()
        contact.name=name
        contact.email=email
        contact.phone=phone
        contact.message=message
        contact.save()
        messages.success(request,"Thanks for contacting us")
        return redirect("/contact.html")
    return render(request, "core/contact.html")


@login_required(login_url='userauths:sign-in')
def advertise(request):
    context={

    }
    return render(request, "core/advertise.html", context)

@login_required(login_url='userauths:sign-in')
def privacy(request):
    context={

    }
    return render(request, "core/privacy.html", context)


@login_required
def view_bookmarks(request):
     # Get the list of bookmarked headline IDs for the current user
    user_bookmarked_headline_ids = request.user.bookmark_set.values_list('headline_id', flat=True)
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('headline')
    context = {
        'bookmarks': bookmarks,
        'user_bookmarked_headline_ids': user_bookmarked_headline_ids,
    }
    return render(request, 'core/bookmarks.html', context)

@csrf_exempt
@login_required(login_url='userauths:sign-in')
def bookmark_article(request, headline_id):
    if request.method == 'POST':
        headline = get_object_or_404(Headline, id=headline_id)
        Bookmark.objects.get_or_create(user=request.user, headline=headline)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
@login_required(login_url='userauths:sign-in')
def remove_bookmark(request, headline_id):
    if request.method == 'POST':
        Bookmark.objects.filter(user=request.user, headline_id=headline_id).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)