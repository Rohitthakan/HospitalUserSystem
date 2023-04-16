from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from users.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from users.models import Picture, Blog, Appointment
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import redirect
import datetime
from datetime import datetime, timedelta


# Create your views here.
def index(request):
    return render(request, 'index.html')

def blogpost(request, pk):
    blogs = get_object_or_404(Blog, pk=pk)
    return render(request, 'blogpost.html', {'blogs': blogs})


def dash(request):
    if request.user.is_authenticated:
        doctors = User.objects.filter(userprofileinfo__type='Doctor')
        documents = Picture.objects.filter(user=request.user)
        if request.user.userprofileinfo.type == 'Doctor':
            # if 'PUBLISH_POST' in request.POST:
            #     sno = request.POST.get('sno')
            #     blog = Blog.objects.filter(sno=sno)
            #     blog.draft = False
            #     blog.save()
            category = request.POST.get('category')
            if category:
                blogs = Blog.objects.filter(category=category, user=request.user)
            else:
                blogs = Blog.objects.filter(user=request.user)
        else:
            category = request.POST.get('category')
            if category:
                blogs = Blog.objects.filter(category=category, draft=False)                
            else:
                blogs = Blog.objects.filter(draft=False)
        return render(request, 'dash.html', {'documents': documents, 'blogs': blogs, 'doctors': doctors})  
    else:
        return render(request, 'dash.html')  



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('dash'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Someone with username: {} and password: {} tried to login and failed".format(username,password))
            return HttpResponse("Invalid login Crediantials!")
    else:
        return render(request,"login.html")
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('dash'))


def signup(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            document = request.FILES.get("document")
            picture = Picture.objects.create(user=user, document=document)

            registered = True

            return HttpResponseRedirect(reverse('login'))
        else:
            print(user_form.errors,profile_form.errors)
            

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'signup.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})



def blog(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        image = request.FILES.get("image")
        category = request.POST.get("category")
        summary = request.POST.get("summary")
        content = request.POST.get("content")
        user = request.user
        
        if 'SAVE_DRAFT' in request.POST:
            ins = Blog(user=user, title=title, image=image, category=category, summary=summary, content=content, draft=True)
        else:
            ins = Blog(user=user, title=title, image=image, category=category, summary=summary, content=content)
        ins.save()
    return render(request, 'blog.html')


@login_required
def create_appointment(request, pk):
    if request.user.userprofileinfo.type != 'Patient':
        return redirect('dash')

    doctor = get_object_or_404(User, pk=pk)
    print(doctor)

    if request.method == 'POST':
        speciality = request.POST.get('speciality')
        date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        start_time = datetime.strptime(request.POST.get('start_time'), '%H:%M').time()
        end_time = (datetime.combine(date, start_time) + timedelta(minutes=45)).time() 
        existing_appointments = Appointment.objects.filter(doctor=doctor, date=date, start_time__lt=end_time, end_time__gt=start_time)
        if existing_appointments.exists():
            context = {'doctor': doctor, 'alert_message': 'The selected time slot is not available. Please choose a different time.'}
            return render(request, 'appointment.html', context)
        appointment = Appointment(patient=request.user, doctor=doctor, speciality=speciality, date=date, start_time=start_time)
        appointment.save()
        return HttpResponseRedirect(reverse('appointments_list'))

    return render(request, 'appointment.html', {'doctor': doctor})

def appointments_list(request):
    appointments = Appointment.objects.filter(patient=request.user)
    appointment = Appointment.objects.filter(doctor=request.user)
    context = {
        'appointments': appointments,
        'appointment' : appointment
    }
    return render(request, 'appointments_list.html', context)

def appointment_details(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    context = {
        'appointment': appointment,
    }
    return render(request, 'appointment_details.html', context)
