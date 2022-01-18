from django.shortcuts import render
from django.views import View
from django.template.response import TemplateResponse
from main.models import Category, Institution, Donation


class LandingPage(View):

    def get(self, request):
        donations = Donation.objects.all()
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
            'donated_institutions': donated_institutions_number
        }
        return TemplateResponse(request, 'base.html', ctx)


class AddDonation(View):

    def get(self, request):
        return TemplateResponse(request, 'form.html')


class Login(View):

    def get(self, request):
        return TemplateResponse(request, 'login.html')


class Register(View):

    def get(self, request):
        return TemplateResponse(request, 'register.html')
# Create your views here.
