from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *

from .forms import StudentForm, CreateUserForm

from .filters import StudentFilter

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def home(request):

	students = Student.objects.all()

	total_students = students.count()

	total_courses = Student.objects.values('programme').distinct().count()

	context = {'total_students' : total_students, 'total_courses': total_courses}


	return render(request, 'students/dashboard.html', context )

@login_required(login_url='login')
def student_data(request):

	students = Student.objects.all()

	myFilter = StudentFilter(request.GET, queryset=students)

	students = myFilter.qs




	context = {'students' : students, 'myFilter' : myFilter}

	return render(request, 'students/students.html', context)

@login_required(login_url='login')
def create_Student (request):

	form = StudentForm
	if request.method == 'POST':
		# print('printing POST', request.POST)
		form = StudentForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')


	context = {'form' : form}

	return render(request, 'students/student_form.html', context)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:

		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)
			if user is not  None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Incorrect Username or Password')


		context = {}
		return render(request, 'students/login.html', context )

def logoutUser(request):

	logout(request)

	return redirect('login')



def registerPage(request):

	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()

		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account created for ' + user)
				return redirect('login')



		context = {'form':form}
		return render(request, 'students/register.html', context )
