from django.shortcuts import render,redirect,HttpResponse
# from django.http import HttpResponse,
# from django.template import RequestContext
from . models import Notices,Hostels,Hostel_Management_Committee,General_Authority,ChiefWardens,Wardens
from users.models import Profile
from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,DetailView
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
def home(request):
	# return HttpResponse("Hello World")
	notices=[]
	for notice in Notices.objects.all():
		notices.insert(0,notice)

	context = { 	'allnotices':1,
					'notices':notices,
					'concerned_hostels':Hostels.objects.all(),
					'sem_choices' : Profile._meta.get_field('sem').choices,
					'gender_choices' : Profile._meta.get_field('gender').choices,
	}
	return render(request,'noticeapp/index.html',context)
@login_required
def notice_board(request):
	notices=[]
	for notice in Notices.objects.all():
		# print(notice.title)
		if request.user.profile.hostel_alloted in notice.concerned_hostels.all():
			notices.insert(0,notice)
	# notices.sort(key=notice.date_posted,reverse=True)

	context = {
				'notices':notices
	}
	return render(request,"noticeapp/index.html",context)
	# return HttpResponse(notices)




class NoticeCreateView(LoginRequiredMixin,CreateView):
	#Search For notices_form.html file in Temlates Directory
	form_class = forms.AddNoticeForm
	model = Notices
	def get_context_data(self,**kwargs):
		context = super(NoticeCreateView,self).get_context_data(**kwargs)
		context['concerned_hostels'] = Hostels.objects.all()
		context['CWs']=ChiefWardens.objects.all()
		context['HMCs']=Hostel_Management_Committee.objects.all()
		context['GAs']=General_Authority.objects.all()
		context['Ws']=Wardens.objects.all()
		return context
	# def get(self,request,**kwargs):
	# 	form = forms.AddNoticeForm()
	# 	return render(request,'noticeapp/notices_form.html',{'form':form})
	def post(self,request,**kwargs):
		# print(request.POST)
		# for hostel in request.POST.getlist('concerned_hostels'):
		# 	print(hostel)

		#creating a form instance with Post Data 
		form = forms.AddNoticeForm(request.POST,request.FILES)
		# 'concerned_hostels'Hostels.objects.all()
		if form.is_valid():
			
			formed_form = form.save(commit=False)
			formed_form.save()
			raw_concerned_hostels = request.POST.getlist('concerned_hostels')
			for raw_hostel in raw_concerned_hostels:
				# if raw_hostel in raw_concerned_hostels
				formed_form.concerned_hostels.add(raw_hostel)
			formed_form.issuing_authority=request.POST['issuing_authority']
			formed_form.save()
			# 	print(name)
			# f.concerned_hostels.add(tuple(request.POST.getlist('concerned_hostels[]')))
			messages.success(self.request,'Notice Added Successfully.')
			# return super().form_valid(form)
			return redirect('homepage')
		else:
			if form.errors:
				for field in form:
					for error in field.errors:
						messages.success(request,'{}'.format(error))
			return redirect('homepage')


	# def form_valid(self,form):
	# 	# form.instance.author=self.request.user 
	# 	messages.success(self.request,'Notice Added Successfully.')
	# 	return super().form_valid(form)

class NoticeDetailView(LoginRequiredMixin,DetailView):
	def get(self,request):
		notice = Notices.objects.all().last()
		return render(request,'noticeapp/notices_detail.html',{'notice':notice})

def Contact(request):
	return render(request,"noticeapp/mnnit_contact_details.html")