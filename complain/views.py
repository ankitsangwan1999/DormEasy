from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView,DetailView,CreateView
from noticeapp.models import Mess_Management_Committee,Wardens
from . import forms
from .models import Complaint,Complainers
from . import forms as complain_forms
'''
FOR SENDING MAIL
'''
from django.core.mail import send_mail,EmailMessage
from django.conf import settings 
from django.template.loader import render_to_string

# Create your views here.
class MyComplains(LoginRequiredMixin,ListView):
	model = Complaint
	template_name = 'complain/my_complains.html'
	context_object_name = 'complains'
	ordering = ['-date_added']
	paginate_by = 1
	def get_context_data(self,**kwargs):
		 context = super(MyComplains,self).get_context_data(**kwargs)
		 context['status_choices']=Complaint._meta.get_field('status').choices
		 context['complains']=Complaint.objects.all().filter(first_complainer=self.request.user)
		 return context
class AllComplains(ListView):
	model = Complaint # MODEL WHICH THIS CLASS GONNA USE           view_type e.g. detail,list
	# template_name attribute tells which template to render
	template_name = 'complain/all_complains.html'# template name form by default for class based views: <app>/<model>_<view_type>.html
	context_object_name = 'complains' # THIS ATTRIBUTE IS FOR GIVING NAME TO THE CONTEXT SO THAT WE 
	# DONT NEED TO CHANGE THE posts VARIABLE USED WITHIN OUR TEMPLATE. 
	ordering = ['-date_added']
	paginate_by = 5
	# form = UserRegistrationForm() #NOT REQUIRED AS FIELDS ARE WRITTEN IN HTML ITSELF
	# model = Categories
	# template_name = 'blogapp/side_nav.html'
	# context_object_name = 'categories'
	def get_context_data(self,**kwargs):
		 context = super(AllComplains,self).get_context_data(**kwargs) # or context = super().get_context_data(**kwargs)
		 # context['posts'] = Post.objects.all()
		 # context['categories'] =  Categories.objects.all()
		 # context['comments'] = Comment.objects.all()
		 context['status_choices']=Complaint._meta.get_field('status').choices
		 # context['form'] = self.form#NOT REQUIRED AS FIELDS ARE WRITTEN IN HTML ITSELF
		 return context

@login_required
def new_complain(request):
	if request.method == 'POST':
		# print(request.POST)
		form = forms.AddComplainForm(request.POST)
		if form.is_valid():
			formed_form = form.save(commit=False)
			formed_form.first_complainer = request.user
			formed_form.related_hostel = request.user.profile.hostel_alloted
			# formed_form.save()
			formed_form.save()
			# print(form.cleaned_data)
			complain = Complaint.objects.all().last()
			complainer = Complainers.objects.create(
						user_id  = request.user,
						complaint_id = complain
						)
			complainer.save()
			subject = "New Complain From a Student."
			from_email = settings.EMAIL_HOST_USER
			to_list = []
			to_list.append(form.cleaned_data['concerned_authority'])
			# print(to_list)
			curr_id = Complaint.objects.all().last().id
			context = {
        		'fullname': request.user.first_name + " " + request.user.last_name,
        		'email':request.user.email,
        		'hostel': request.user.profile.hostel_alloted,
        		'title': formed_form.title,
        		'curr_id':str(curr_id)
    		}
			html_message = render_to_string("complain/html_content.html",context)
			msg = EmailMessage(subject,html_message,from_email,to_list)
			msg.content_subtype = "html"
			try:
				msg.send(fail_silently=True)
			except BadHeaderError:
				return HttpResponse('Mail Not Sent Successfully. Possible Causes:- Invalid header found/Connection Issue.')			
			# respond var is 1 when mail sent is successful and 0 when it is not
			messages.success(request,'{}'.format("In regard to your Complain an Email has been sent to the concerned concerned_authority. You will get a resonse shortly."))
			return redirect("complain-detail",curr_id)
		else:
			if form.errors:
				for field in form:
					for error in field.errors:
						return HttpResponse(error)
	else:
		form = forms.AddComplainForm()
		context = {	
					'MMCs':Mess_Management_Committee.objects.all().filter(hostel=request.user.profile.hostel_alloted),
					'Ws':Wardens.objects.all().filter(hostel = request.user.profile.hostel_alloted),
					# 'WFs':Wardens._meta.get_fields(),
					'form':form	
		}
		return render(request,"complain/new_complain.html",context)

class ComplainDetailView(LoginRequiredMixin,DetailView):

	def get(self,request,pk):
		complain = Complaint.objects.all().filter(id=pk).first()
		status_choices=Complaint._meta.get_field('status').choices
		# comments = Comment.objects.all()       'comments':comments
		return render(request,'complain/complain_detail.html',{'complain':complain,'status_choices':status_choices})
	def post(self,request,pk):
		new_status = int(request.POST['status'])
		complain = Complaint.objects.all().filter(id=pk).first()
		complain.status = new_status
		complain.save()
		first_complainer = complain.first_complainer.email
		subject = "Complaint Resolved!"
		from_email = settings.EMAIL_HOST_USER
		to_list = []
		to_list.append(first_complainer)
		# print(type(new_status))
		if new_status == 2:
			print("Email sent")
			curr_id = complain.id
			context = {
	    		'title': complain.title,
	    		'curr_id':str(curr_id)
			}
			html_message = render_to_string("complain/html_content_resolved.html",context)
			msg = EmailMessage(subject,html_message,from_email,to_list)
			msg.content_subtype = "html"
			try:

				msg.send(fail_silently=True)

			except BadHeaderError:
				return HttpResponse('Mail Not Sent Successfully. Possible Causes:- Invalid header found/Connection Issue.')			
			# respond var is 1 when mail sent is successful and 0 when it is not
			messages.success(request,'{}'.format("Status of the Complain has been updated and Review Email Sent."))
		# status_choices=Complaint._meta.get_field('status').choices
		# return render(request,'complain/all_complains.html',{'status_choices':status_choices})
		return redirect("complains_on_me")

@login_required
def CommentView(request,pk):
	if request.method == 'POST':
		# print(request.POST)

		complain = Complaint.objects.all().filter(id=pk).first()
		form = complain_forms.AddComment(request.POST)
		submit_val = int(request.POST['submit'])
		
		if submit_val == 2:
			form.instance.is_review = True
		form.instance.user = request.user
		form.instance.complaint = complain
		next = request.POST.get('next','/')
		# print(next) # we get like /newhome/?page=4
		rediurl = next+"#"+ str(complain.id)
		if form.is_valid():
			form.save()
			messages.success(request,f'Commeted Successfully!')
			# return HttpResponse("Commeted Successfully!")	
			# return HttpResponse("Commeted Successfully!")
			return redirect(rediurl) 
		else:
			messages.success(request,f'Comments can\'t be blank.')
			return redirect(next)


@staff_member_required
def CompsOnMe(request):
	complains = Complaint.objects.all().filter(concerned_authority = request.user.email)
	context = {
		'count': complains.count(),
		'comps_on_me' : complains,
		'status_choices' : Complaint._meta.get_field('status').choices
	}
	return render(request,"complain/complains_on_me.html",context)

@staff_member_required
def ResolvedComplains(request):
	# print(request.user.email)
	complains = Complaint.objects.all().filter(status=2).filter(concerned_authority = request.user.email)
	context = {
		'count': complains.count(),
		'res_comps' : complains,
		'status_choices' : Complaint._meta.get_field('status').choices
	}
	return render(request,"complain/resolved_complains.html",context)


@login_required
def GiveFbRes(request):
	complains = Complaint.objects.all().filter(status=2).filter(first_complainer=request.user)
	context={
		'count': complains.count(),
		'res_comps' : complains,
		'status_choices' : Complaint._meta.get_field('status').choices
	}
	return render(request,"complain/give_fb_on_res.html",context)




@login_required
def DislikeComplains(request):
	complain_id = int(request.GET.get('complain_id'))
	# print(complain_id)
	complainers = Complainers.objects.all().filter(user_id = request.user.id).filter(complaint_id=complain_id).count()
	print(complainers)
	complain = Complaint.objects.all().filter(id = complain_id ).first()
	if complainers == 0 and request.user.username != complain.first_complainer.username:
			complain.number = complain.number + 1
			complain.save()
			obj = Complainers.objects.create(
					user_id = request.user,
					complaint_id = complain  
				)
			obj.save()

	context = {
			'newnumber' : complain.number,
			
	}
	return JsonResponse(context)