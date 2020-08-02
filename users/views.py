from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate,views
from django.contrib.auth.decorators import login_required
from .models import Reg_Students,Profile
from users.models import Hostels
from django.contrib import messages
import re
from .forms import UserUpdateForm,ProfileUpdateForm
# Create your views here.

def register(request):
	if request.method == 'POST':
		username = request.POST['username']
		password1 = request.POST['password1'] 
		password2 = request.POST['password2']
		email  = request.POST['email']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		regno = int(request.POST['regno'])
		sem_ind = request.POST.get('sem')
		gender_ind = request.POST.get('gender')
		hostel_alloted = request.POST.get('hostel_alloted')## to remove multivaluedictionary error
		reg_students =  Reg_Students.objects.all() # College registered Students
		reg_students_regno = [] #regno of College Registered Students
		reg_users = User.objects.all() #signed up users
		reg_username = [] #username of signed up users
		reg_email = [] #email of signed up users
		reg_users_profile = Profile.objects.all() # profile of signed up users to validate duplicate regno
		reg_regno = [] #regno of signed up students
		for user in reg_users:
			reg_username.append(user.username)
			reg_email.append(user.email)
		for entry in reg_students:
			reg_students_regno.append(int(entry.Regno))
		for regnumber in reg_users_profile:
			reg_regno.append(int(regnumber.regno))
		# print(reg_regno)
		if password1 != password2:
			messages.error(request,"Password Didn't Match.")
			return redirect(request.GET.get('next','homepage'))
		if username in reg_username:
			messages.error(request,"Username taken.")
			return redirect(request.GET.get('next','homepage'))
		# print(reg_email)
		if email in reg_email:
			messages.error(request,"Email already registered.")
			return redirect(request.GET.get('next','homepage'))
		# print(regno)
		# print(reg_students_regno)
		# print(regno)
		# print(regno in reg_regno)
		if regno not in reg_students_regno:
			messages.error(request,"Invalid Registration no.")
			return redirect(request.GET.get('next','homepage'))
		elif regno in reg_regno:
			messages.error(request,"This Registration No. has already Signed Up.")
			return redirect(request.GET.get('next','homepage'))
		if len(password1)<8 or len(password1)>15:
			messages.error(request,"Password should contain 1-15 Characters")
			return redirect(request.GET.get('next','homepage'))
		def has_num_and_alph(s):
			return bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])',s))
		if has_num_and_alph(password1) is False:
			messages.error(request,"Password should contain atleast 1 Number and 1 Alphabet")
			return redirect(request.GET.get('next','homepage'))
			
	# Registration request is valid.
		# print(Profile._meta.get_field('sem').choices[int(sem_ind)-1][1])
		user = User.objects.create_user(
			username = username,
			email = email,
			password = password1,
			first_name = first_name,
			last_name  = last_name
		)
		if user:
			user.save()
		else:
			messages.error(request,"Error occured in Registration")
			return redirect(request.GET.get('next','homepage'))
	# updating profile
		#updating the regstered user query set
		reg_users = User.objects.all()	
		if user in reg_users: 
			profile = Profile(
				user = user,
				regno = regno,
				sem = Profile._meta.get_field('sem').choices[int(sem_ind)-1][0],
				gender = Profile._meta.get_field('gender').choices[int(gender_ind)][0],
				hostel_alloted = Hostels.objects.all().filter(hostel_name=hostel_alloted).first()	
			)
			profile.save()
			messages.error(request,"Registered Successfully.Log in to continue with Website.")
			return redirect(request.GET.get('next','homepage'))
		else:
			messages.error(request,"Error occured in Registration")
			return redirect(request.GET.get('next','homepage'))
	else:
		concerned_hostels = Hostels.objects.all()
		context = { 'concerned_hostels':Hostels.objects.all(),
					'sem_choices' : Profile._meta.get_field('sem').choices,
					'gender_choices' : Profile._meta.get_field('gender').choices,
		}
		# print(context.get('sem_choices'))
		return redirect('homepage')

def logout_view(request):
	messages.success(request,"Logged Out Succesfully")
	logout(request)
	return redirect('homepage')
def login_view(request):
	username = request.POST['username']
	password = request.POST['password']
	regno = int(request.POST['regno']) # regno is a string
	remember_me = request.POST.get('remember_me')
	# print(username,password)
	# print(remember_me)
	user = authenticate(request,username=username,password=password)
	if user is not None:
		# print(Profile.objects.all().filter(user=user).first().regno)
		response = redirect(request.GET.get('next','homepage'))
		profile = Profile.objects.all().filter(user=user).first()
		if profile:
			if Profile.objects.all().filter(user=user).first().regno == regno:
				login(request,user)
				messages.error(request,"Login Succesfully.")
				if remember_me is None:
					if 'cook_user' and 'cook_pass' and 'cook_regno' in request.COOKIES:
						response.delete_cookie('cook_user')
						response.delete_cookie('cook_pass')
						response.delete_cookie('cook_regno')	
					return response
				else:
					if 'cook_user' and 'cook_pass' and 'cook_regno' not in request.COOKIES:
						response.set_cookie('cook_user',username,max_age=86400,path='/')
						response.set_cookie('cook_pass',password,max_age=86400,path='/')
						response.set_cookie('cook_regno',regno,max_age=86400,path='/')	
					return response
			else:
				messages.error(request,"Registration no. not correct.")
				return response
		# else:
			#Not working for now coz we don't come to this view on soicial-login
			#instead go to create_userprofile view
			# user.delete()
			# messages.error(request,"This Account is not Registered Yet.")
			# return response

		
	else:
		messages.error(request,"Invalid Credentials")
		return redirect(request.GET.get('next','homepage'))

@login_required
def profile(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		username = request.POST['username']
		hostel_alloted = request.POST.get('hostel_alloted')
		sem = request.POST.get('sem')
		users = User.objects.all()	
		emails = []
		usernames = []
		print(request.POST)
		for user in users:
			emails.append(user.email)
			usernames.append(user.username)

		if (username != request.user.username) and (username in usernames):
			messages.error(request,"Username already Exist.")
			return redirect(request.path_info)
		if email != request.user.email and email in emails:
			messages.error(request,"Email already Exists.")
			return redirect(request.path_info)
		u_form = UserUpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
		# print(request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request,f'Profile Info Updated Succesfully')
			return redirect(request.path_info)
		else:
			messages.success(request,f'Somethong Went Wrong.')
			return redirect(request.path_info)

	context={
		# 'regno':Profile.objects.all().filter(user=request.user).first().regno,
		'concerned_hostels': Hostels.objects.all(),
		'sem_choices' : Profile._meta.get_field('sem').choices,
		'gender_choices' : Profile._meta.get_field('gender').choices
	}
	return render(request,"users/profile.html",context)




@login_required
def create_profile(request):
	if request.method == 'POST':
		regno = int(request.POST['regno'])
		sem_ind = request.POST.get('sem')
		gender_ind = request.POST.get('gender')
		hostel_alloted = request.POST.get('hostel_alloted')## to remove multivaluedictionary error
		reg_students =  Reg_Students.objects.all() # College registered Students
		reg_students_regno = [] #regno of College Registered Students
		reg_users_profile = Profile.objects.all()
		reg_regno = [] #regno of signed up students
		for entry in reg_students:
			reg_students_regno.append(int(entry.Regno))
		for regnumber in reg_users_profile:
			reg_regno.append(int(regnumber.regno))
		

		if regno not in reg_students_regno:
			messages.error(request,"Invalid Registration no.")
			return redirect(request.path_info)
		elif regno in reg_regno:
			messages.error(request,"This Registration No. has already Signed Up.")
			return redirect(request.path_info)
		# updating profile
		#updating the regstered user query set
		reg_users = User.objects.all()	
		if request.user in reg_users: 
			profile = Profile(
				user = request.user,
				regno = regno,
				sem = Profile._meta.get_field('sem').choices[int(sem_ind)-1][0],
				gender = Profile._meta.get_field('gender').choices[int(gender_ind)][0],
				hostel_alloted = Hostels.objects.all().filter(hostel_name=hostel_alloted).first()	
			)
			profile.save()
			messages.error(request,"Successfully Created the Profile.")
			return redirect(request.GET.get('next','homepage'))
		else:
			messages.error(request,"Error occured in Creating Profile.")
			return redirect(request.GET.get('next','homepage'))

	else:
		profile = Profile.objects.all().filter(user=request.user)
		if profile:
			# messages(request,"Profile Already Created for you.")
			# return HttpResponse("Profile Already Created for you.")
			return redirect(request.GET.get('next','homepage'))
		else:
			context = { 'concerned_hostels':Hostels.objects.all(),
						'sem_choices' : Profile._meta.get_field('sem').choices,
						'gender_choices' : Profile._meta.get_field('gender').choices,
			}
			return render(request,"users/new_profile.html",context)

class PasswordResetUView(views.PasswordResetView):
	pass
class PasswordResetDoneUView(views.PasswordResetDoneView):
	pass
class PasswordResetConfirmUView(views.PasswordResetConfirmView):
	pass
class PasswordResetCompleteUView(views.PasswordResetCompleteView):
	pass