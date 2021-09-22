from django.shortcuts import render
#from myapp.models import log, contacts

# Create your views here.
def veri(request):
    return render(request, 'veri.html')
