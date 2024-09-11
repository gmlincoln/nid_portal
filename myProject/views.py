from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from myApp.models import *

@login_required
def homePage(req):
    
    user = req.user
    
    return render(req, 'myAdmin/index.html', {'user':user})



def registerPage(req):
    
    if req.method == 'POST':
        
        first_name = req.POST.get('firstname')
        last_name = req.POST.get('lastname')
        username = req.POST.get('username')
        email = req.POST.get('email')
        profile_pic = req.FILES.get('profile_pic')
        user_type = req.POST.get('user-type')
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm-password')
        
        if password == confirm_password:
            register = Custom_User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            profile_pic = profile_pic,
            user_type = user_type,
            password = confirm_password
            )
            register.save() 
            return redirect('loginPage')
        else:
            return HttpResponse('Sorry! Password not match!!!')
    
    return render(req, 'common/register.html')




def loginPage(req):
    
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        
        user = authenticate(req, username = username, password = password)

        if user:
            login(req,user)
            return redirect('homePage')
        else:
            return HttpResponse('Sorry! Username or Password is Wrong!!!')
    
    return render(req, 'common/login.html')


def logoutPage(req):
    
    logout(req)
    
    return redirect('loginPage')

@login_required
def addNID(req):
    
    users = Custom_User.objects.all()
    
    if req.method == 'POST':
        myid = req.POST.get('user-name')
        nid_number = req.POST.get('nid-number')
        date_of_issue = req.POST.get('date-of-issue')
        place_of_issue = req.POST.get('place-of-issue')
        
        user = Custom_User.objects.get(id=myid)
        
        newCitizen = NID_Model(
            user = user,
            nid_number = nid_number,
            date_of_issue = date_of_issue,
            place_of_issue = place_of_issue
        )
        
        newCitizen.save()
        return redirect('citizenList')     
        
    return render(req,'myAdmin/add-nid.html', {'users':users})


@login_required
def citizenList(req):
    
    users = NID_Model.objects.all()
    
    return render(req,'myAdmin/citizen-list.html', {'users':users})

@login_required
def singleNid(req,id):
    
    users = NID_Model.objects.get(id=id)
    
    return render(req,'myAdmin/nid-single-view.html', {'users':users})

@login_required
def removeCitizen(req, id):
    
    data = NID_Model.objects.filter(id=id)
    
    data.delete()
    
    return redirect('citizenList')

@login_required
def updateNID(req,id):
    
    
    data = NID_Model.objects.get(id=id)
    user = data.user
    
    if req.method == 'POST':
        user.first_name = req.POST.get('firstname')
        user.last_name = req.POST.get('lastname')
        user.username = req.POST.get('username')
        user.email = req.POST.get('email')
        
        
        if req.FILES.get('profile_pic'):
            user.profile_pic = req.FILES.get('profile_pic')
        
        user.save()

        data.nid_number = req.POST.get('nid-number')
        data.date_of_issue = req.POST.get('date-of-issue')
        data.place_of_issue = req.POST.get('place-of-issue')
        
        data.save()

        return redirect('citizenList')
        
    
    return render(req,'myAdmin/update-nid.html', {'data':data})