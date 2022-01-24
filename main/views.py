from django.shortcuts import render, redirect
from django.views import View
from django.template.response import TemplateResponse
from main.models import Category, Institution, Donation, MyUser, INSTITUTIONS
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
import json


class LandingPage(View):

    def get(self, request):
        donations = Donation.objects.all()
        foundations_list = list(Institution.objects.filter(type=1))
        ngos_list = list(Institution.objects.filter(type=2))
        local_initiatives_list = list(Institution.objects.filter(type=3))

        foundations_paginator = Paginator(foundations_list, 5)
        ngos_paginator = Paginator(ngos_list, 5)
        local_initiatives_paginator = Paginator(local_initiatives_list, 5)
        page = request.GET.get('page')
        foundations = foundations_paginator.get_page(page)
        ngos = ngos_paginator.get_page(page)
        local_initiatives = local_initiatives_paginator.get_page(page)

        donated_bags = 0
        for donation in donations:
            donated_bags += donation.quantity
        donated_institutions = []
        for donation in donations:
            if donation.institution not in donated_institutions:
                donated_institutions.append(donation.institution)
        if not donated_institutions:
            donated_institutions_number = 0
        else:
            donated_institutions_number = len(donated_institutions)
        ctx = {
            'donated_bags': donated_bags,
            'donated_institutions_number': donated_institutions_number,
            'foundations': foundations,
            'ngos': ngos,
            'local_initiatives': local_initiatives
        }
        return render(request, 'base.html', ctx)


class AddDonation(View):

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        categories_serializable = categories.values('name')
        institutions_serializable = institutions.values('name', 'description', 'type', 'categories')
        ctx = {
            'categories': categories,
            'institutions': institutions,
            'categories_json': json.dumps(list(categories_serializable)),
            'institutions_json': json.dumps(list(institutions_serializable)),
        }
        if request.user.is_authenticated:
            return TemplateResponse(request, 'form.html', ctx)
        else:
            return TemplateResponse(request, 'base.html')

    # def post(self, request):
    #     category = request.POST.get('categories')
    #     quantity = request.POST.get('bags')
    #     organization = request.POST.get('organization')
    #     address = request.POST.get('address')
    #     city = request.POST.get('city')
    #     postcode = request.POST.get('postcode')
    #     phone = request.POST.get('phone')
    #     date = request.POST.get('data')
    #     time = request.POST.get('time')
    #     comment = request.POST.get('more_info')
    #     print(category)
    #     print(quantity)
    #     print(organization)
    #     print(address)
    #     print(city)
    #     print(postcode)
    #     print(phone)
    #     print(date)
    #     print(time)
    #     print(comment)
    #     return render(request, 'form-confirmation.html')


class Login(View):

    def get(self, request):
        return TemplateResponse(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        logged_user = authenticate(email=email, password=password)
        if logged_user:
            login(request, logged_user)
            url_next = request.GET.get('next', '/')
            return redirect(url_next)
        else:
            return render(request, 'register.html')


class Logout(View):

    def get(self, request):
        logout(request)
        return TemplateResponse(request, 'base.html')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password2')
        if name and surname and email and password == password_confirmation:
            user = MyUser.objects.create_user(email=email,
                                              password=password,
                                              first_name=name,
                                              last_name=surname)
            return render(request, 'login.html')
        else:
            return render(request, 'register.html')
