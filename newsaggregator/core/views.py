from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# @login_required(login_url='userauths:sign-in')
# def home(request):
#     context={

#     }
#     return render(request, "core/home.html", context)