from django.shortcuts import render, redirect, get_object_or_404
from links.models import Link, FileObject
from accounts.models import Account
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

def createSuffix(v):
    vArr = v.split('/')
    suf = vArr[-1]
    if suf.isalnum():
        try:
            Link.objects.get(suffix=suf)
            if Link.is_active:
                return createRandomSuffix(), False
            else:
                return suf, True
        except Link.DoesNotExist:
            return suf, True
    else:
        return createRandomSuffix(), False

def home(request):
    print("home called")
    if request.method == 'POST':
        if request.POST['urlinput']:
            _user = request.user.is_authenticated
            if _user:
                print("user-mode")
            print("request ", request.POST['urlinput'])
            link = Link()
            link.to = request.POST['urlinput']
            result = False
            if _user:
                if request.POST['suffixinput']:
                    link.suffix, result = createSuffix(request.POST['suffixinput'])
                else:
                    result = True
                    link.suffix = createRandomSuffix()
            else:
                result = True
                link.suffix = createRandomSuffix()
            
            link.is_active = True
            is_onetime_checkbox = request.POST.get('onetimeinput', False)
            if is_onetime_checkbox:
                link.redirects = 1
            datecur = timezone.datetime.now()
            link.expiry = datetime(datecur.year+100, datecur.month, datecur.day)
            
            if _user:
                link.owner = request.user
                user_account = Account.objects.get(username=request.user)
                user_account.linkset.append(link)
                user_account.save()
            else:
                link.owner = User.objects.get(username='akshay')
            link.save()

            retlink = "zuru.io/"+link.suffix
            error = "Sorry! That URL is not available."
            if not result:
                return render(request, 'links/home.html', {'retlink1':retlink, 'error':error})
            else:
                return render(request, 'links/home.html', {'retlink1':retlink})
    else:
        return render(request, 'links/home.html')

def homeU(request):
    print("homeU called")
    if request.method == 'POST':
        if request.FILES['fileinput']:
            _user = request.user.is_authenticated
            if _user:
                print("user mode")
            print("request ", request.FILES['fileinput'])
            fileobject = FileObject()
            fileobject.name = str(request.FILES['fileinput'])
            fileobject.fileObject = request.FILES['fileinput']
            datecur = timezone.datetime.now()
            fileobject.expiry = datetime(datecur.year+100, datecur.month, datecur.day)
            if _user:
                fileobject.owner = request.user
            else:
                fileobject.owner = User.objects.get(username='akshay')
            fileobject.link =""
            
            fileobject.save()
            _multi = request.POST.get('multiaccess', False)
            if _multi:
                fileobject.redirects = 9999
            fileobject.link = "https://zurustorage.blob.core.windows.net/media/" + fileobject.fileObject.name
            fileobject.save()

            # create link for this file

            link = Link()
            link.to = fileobject.link
            link.is_fileobject = True

            if _user:
                if request.POST['fsuffixinput']:
                    link.suffix, result = createSuffix(request.POST['fsuffixinput'])
                else:
                    result = True
                    link.suffix = createRandomSuffix()
            else:
                link.suffix = createRandomSuffix()
                result = True

            link.is_active = True
            if _multi:
                link.redirects = 9999
            else:
                link.redirects = 1
            datecur = timezone.datetime.now()
            link.expiry = datetime(datecur.year+100, datecur.month, datecur.day)
            fileobject.suffix = link.suffix
            fileobject.save()
            if _user:
                link.owner = request.user
                user_account = Account.objects.get(username=request.user)
                user_account.linkset.append(link)
                user_account.fileset.append(fileobject)
                user_account.save()
            else:
                link.owner = User.objects.get(username='akshay')
            link.save()


            retlink = "zuru.io/"+link.suffix
            error = "Sorry! That URL is not available."
            if not result:
                return render(request, 'links/home.html', {'retlink2':retlink, 'error':error})
            else:
                return render(request, 'links/home.html', {'retlink2':retlink})
    else:
        return render(request, 'links/home.html')

def transfer(request, link_id):
    link = get_object_or_404(Link, suffix=link_id)
    print("requesting transfer ", link_id)
    go = link.to
    # TODO: make this a background task
    if link.redirects == 1:
        link_owner = Account.objects.get(username=link.owner)
        link_owner_linkset = link_owner.linkset
        link_owner_fileset = link_owner.fileset
        for i in range(0, len(link_owner_linkset)):
            if link_owner_linkset[i].suffix == link_id:
                print("deleting owner link")
                del link_owner_linkset[i]
                break
        if link.is_fileobject:
            for i in range(0, len(link_owner_fileset)):
                if link_owner_fileset[i].suffix == link_id:
                    print("deleting owner file")
                    del link_owner_fileset[i]
                    fileobject = get_object_or_404(FileObject, suffix=link_id)
                    fileobject.delete()
                    break
        link.delete()
        link_owner.save()

    return redirect(go)

def dashboard(request):
    if request.user.is_authenticated:
        user_account = Account.objects.get(username=request.user)
        links = user_account.linkset
        files = user_account.fileset
        for f in files:
            if f.redirects > 1:
                f.redirects = True
            else:
                f.redirects = False

            f_suf = f.suffix
            for i in range(0, len(links)):
                l = links[i]
                if l.suffix == f_suf:
                    print("removing ", f_suf)
                    f.link = l.suffix
                    del links[i]
                    break
        for link in links:
            if link.redirects == 1:
                link.redirects = True
            else:
                link.redirects = False

        for link in links:
            print(link.suffix)
        return render(request, 'links/dashboard.html', {'linkset':links, 'fileset':files})
    else:
        return redirect('login')