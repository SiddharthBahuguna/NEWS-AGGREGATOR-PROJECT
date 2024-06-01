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
from core.forms import ContactForm
from django.template.loader import render_to_string
from django.core.mail import send_mail


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Headline, Bookmark, Rating
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
def contact(request):
    today_date = datetime.now().strftime('%Y-%m-%d')
    if request.method == "POST":
        form = ContactForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            content = form.cleaned_data['content']

            html = render_to_string('components/email.html', {
                'name': name,
                'email': email,
                'phone': phone,
                'content': content,
            })

            send_mail("The contact form subject", 'this is the message', email, ['email@gmail.com'], html_message=html)
            messages.success(request, 'Form submitted successfully!')
            return redirect("core:index")
    else:
        form = ContactForm()

    context={
        'today_date': today_date,
        'form': form,
    }
    return render(request,"core/contact.html",context)

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


# @login_required(login_url='userauths:sign-in')
# def view_bookmarks(request):
#     # Get the list of bookmarked headlines for the current user
#     bookmarks = Bookmark.objects.filter(user=request.user).select_related('headline')
    
#     if bookmarks.exists():
#         context = {'bookmarks': bookmarks}
#     else:
#         context = {'message': 'You have no bookmarks yet.'}


#     return render(request, 'core/bookmarks.html', context)
def view_bookmarks(request):
    if request.user.is_authenticated:
        # Get the list of bookmarked headlines for the current user
        bookmarks = Bookmark.objects.filter(user=request.user).select_related('headline')
        
        if bookmarks.exists():
            context = {'bookmarks': bookmarks}
        else:
            context = {'message': 'You have no bookmarks yet.'}
        
        return render(request, 'core/bookmarks.html', context)
    else:
        message = 'Sign in to view bookmarks.'
        return render(request, 'core/index.html', {'message': message})
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
import json
@login_required
@csrf_exempt
def rate_headline(request, headline_id):
    if request.method == 'POST':
        headline = get_object_or_404(Headline, id=headline_id)
        
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Print the entire JSON payload for debugging
            rating_value_str = data.get('rating')
            # print("rating_value_str:", rating_value_str)  # Add this line for debugging
        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON'}, status=400)

        if rating_value_str is not None:
            try:
                rating_value = int(rating_value_str)
            except ValueError:
                return JsonResponse({'status': 'fail', 'message': 'Invalid rating value'}, status=400)
        else:
            return JsonResponse({'status': 'fail', 'message': 'Rating value is missing'}, status=400)
        
        # Check if the user has already rated this headline
        rating, created = Rating.objects.get_or_create(user=request.user, headline=headline)
        rating.rating = rating_value
        rating.save()
        
        # Update headline average rating and rating count
        ratings = Rating.objects.filter(headline=headline).exclude(rating__isnull=True)
        headline.rating_count = ratings.count()
        headline.average_rating = sum(r.rating for r in ratings) / headline.rating_count if headline.rating_count > 0 else 0
        headline.save()

        return JsonResponse({'status': 'success', 'average_rating': headline.average_rating, 'rating_count': headline.rating_count})
    return JsonResponse({'status': 'fail'}, status=400)
from django.shortcuts import render
from .models import Headline

def top_rated_articles(request):
    if request.user.is_authenticated:
        top_rated_articles = Headline.objects.filter(average_rating__gte=3.5).order_by('-average_rating')
    else:
        top_rated_articles = Headline.objects.none()

    paginator = Paginator(top_rated_articles, 9)  # 9 items per page

    page = request.GET.get('page')
    try:
        top_rated_articles_obj = paginator.page(page)
    except PageNotAnInteger:
        top_rated_articles_obj = paginator.page(1)
    except EmptyPage:
        top_rated_articles_obj = paginator.page(paginator.num_pages)

    context = {
        'object_list': top_rated_articles_obj,
        'paginator': paginator
    }
    return render(request, 'core/index.html', context)
