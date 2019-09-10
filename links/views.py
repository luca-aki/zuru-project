from django.shortcuts import render, redirect, get_object_or_404
from links.models import Link, FileObject
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
import random
import string
# Create your views here.

def createRandomSuffix(stringLength = 4):
    l = stringLength
    letters = string.ascii_letters + string.digits
    val = ''.join([random.choice(letters) for i in range(stringLength)])
    try:
        Link.objects.get(suffix=val)
        if Link.is_active:
            return createRandomSuffix(stringLength=l)
        else:
            return val
    except Link.DoesNotExist:
        return val

def home(request):
    print("home called")
    if request.method == 'POST':
        if request.POST['urlinput']:
            print("request ", request.POST['urlinput'])
            link = Link()
            link.to = request.POST['urlinput']
            link.suffix = createRandomSuffix()
            link.is_active = True
            is_onetime_checkbox = request.POST.get('onetimeinput', False)
            if is_onetime_checkbox:
                link.redirects = 1
            datecur = timezone.datetime.now()
            link.expiry = datetime(datecur.year+100, datecur.month, datecur.day)
            
            # if the user is logged in then he will be owner of the link
            # else akshay will be owner 

            # else part
            link.owner = User.objects.get(username='akshay')
            link.save()

            retlink = "localhost:8000/"+link.suffix
            return render(request, 'links/home.html', {'retlink':retlink})
    else:
        return render(request, 'links/home.html')

def homeU(request):
    print("homeU called")
    if request.method == 'POST':
        if request.FILES['fileinput']:
            print("request ", request.FILES['fileinput'])
            fileobject = FileObject()
            fileobject.fileObject = request.FILES['fileinput']
            datecur = timezone.datetime.now()
            fileobject.expiry = datetime(datecur.year+100, datecur.month, datecur.day)
            fileobject.owner = User.objects.get(username='akshay')
            fileobject.link =""
            fileobject.save()

            fileobject.link = "https://zurustorage.blob.core.windows.net/media/" + fileobject.fileObject.name
            fileobject.save()

            # create link for this file

            link = Link()
            link.to = fileobject.link
            link.suffix = createRandomSuffix()
            link.is_active = True
            link.redirects = 1
            datecur = timezone.datetime.now()
            link.expiry = datetime(datecur.year+100, datecur.month, datecur.day)
            link.owner = User.objects.get(username='akshay')
            link.save()

            retlink = "localhost:8000/"+link.suffix
            return render(request, 'links/home.html', {'retlink2':retlink})
    else:
        return render(request, 'links/home.html')

def transfer(request, link_id):
    redirect_link = get_object_or_404(Link, suffix=link_id)
    return redirect(redirect_link.to)