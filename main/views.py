from django.shortcuts import render, redirect
from django.views import View
from django.template.response import TemplateResponse
from main.models import Category, Institution, Donation, MyUser, INSTITUTIONS
from main.forms import AddUserForm, LoginForm, DonationForm
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, QueryDict
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

    def post(self, request):
        data = json.load(request)
        data['bags'] = int(data['bags'])
        data['categories'] = int(data['categories'])
        query_dict = QueryDict('', mutable=True)
        query_dict.update(data)
        form = DonationForm(query_dict)
        if form.is_valid():
            quantity = data['bags']
            categories = data['categories']
            institution = Institution.objects.get(name=data['organization'])
            address = data['address']
            phone = data['phone']
            city = data['city']
            postcode = data['postcode']
            pick_up_date = data['data']
            pick_up_time = data['time']
            pick_up_comment = data['more_info']
            user = request.user
            donation = Donation.objects.create(quantity=quantity,
                                               institution=institution,
                                               address=address,
                                               phone_number=phone,
                                               city=city,
                                               zip_code=postcode,
                                               pick_up_date=pick_up_date,
                                               pick_up_time=pick_up_time,
                                               pick_up_comment=pick_up_comment,
                                               user=user
                                               )
            donation.categories.add(categories)
            return JsonResponse({'url': '/confirm'})
        else:
            return TemplateResponse(request, 'base.html')


class Login(View):

    def get(self, request):
        return TemplateResponse(request, 'login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        print(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            logged_user = authenticate(email=email, password=password)
            if logged_user:
                login(request, logged_user)
                url_next = request.GET.get('next', '/')
                return redirect(url_next)
            else:
                return render(request, 'register.html')
        else:
            return TemplateResponse(request, 'login.html')


class Logout(View):

    def get(self, request):
        logout(request)
        return TemplateResponse(request, 'base.html')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password2']
            if name and surname and email and password == password_confirmation:
                user = MyUser.objects.create_user(email=email,
                                                  password=password,
                                                  first_name=name,
                                                  last_name=surname)
                return render(request, 'login.html')
            else:
                return render(request, 'register.html')
        else:
            return render(request, 'register.html')


class Confirmation(View):

    def get(self, request):
        return render(request, 'form-confirmation.html')