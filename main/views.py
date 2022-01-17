from django.shortcuts import render
from django.views import View
from django.template.response import TemplateResponse


class LandingPage(View):

    def get(self, request):
        return TemplateResponse(request, 'base.html')


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
