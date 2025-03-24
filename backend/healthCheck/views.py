from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from healthCheck.models import Employee


# Create your views here.
def index(request):
    employees = Employee.objects.all()
    template = loader.get_template("healthChecks/index.html")
    context = {
        "employees": employees
    }
    return HttpResponse(template.render(context, request))
