from django.shortcuts import render
from django.views import View
from django.template.response import TemplateResponse
from main.models import Category, Institution, Donation
from django.core.paginator import Paginator

from django.conf import settings

User = settings.AUTH_USER_MODEL


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
        return TemplateResponse(request, 'form.html')


class Login(View):

    def get(self, request):
        return TemplateResponse(request, 'login.html')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get['name']
        surname = request.POST.get['surname']
        email = request.POST.get['email']
        password = request.POST.get['password']
        password_confirmation = request.POST.get['password2']
        # if password == password_confirmation:
        #     if User.objects.filter(username=username).exists():
        #         ctx['error_message'] = 'Taki użytkownik już istnieje'
        #         return TemplateResponse(request, 'main_app/add_user_form.html', ctx)
        #     elif password != confirmed_password:
        #         ctx['error_message'] = 'Podane hasła różnią się'
        #         return TemplateResponse(request, 'main_app/add_user_form.html', ctx)
        #     else:
        #         user = User.objects.create_user(username=username, password=password, first_name=first_name,
        #                                         last_name=last_name, email=email)
        #         ctx['message'] = 'Dodano użytkownika'
        #         login(request, user)
        #         return redirect('home')
# Create your views here.
