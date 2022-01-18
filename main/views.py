from django.shortcuts import render, redirect
from django.views import View
from django.template.response import TemplateResponse
from main.models import Category, Institution, Donation, MyUser
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout


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
        if request.user.is_authenticated:
            return TemplateResponse(request, 'form.html')
        else:
            return TemplateResponse(request, 'base.html')


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

