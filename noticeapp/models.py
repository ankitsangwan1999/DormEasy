from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
class Hostels(models.Model):
	Hostel_Type = (
			('B','Boys'),('G','Girls')
	)
	hostel_name = models.CharField(max_length=100,unique=True)# max_length is mandatory for CharField
	Type = models.CharField(max_length=1,choices=Hostel_Type)
	class Meta:
		ordering= ['id']
	def __str__(self):
		return "{}".format(self.hostel_name)

class Notices(models.Model):
	title = models.CharField(max_length=50,unique=True)
	label = models.CharField(max_length=50,unique=True)
	description = RichTextUploadingField(max_length=150)
	notice_file = models.FileField(upload_to='Notices')
	date_posted = models.DateTimeField(default = timezone.now)
	val_time = models.DateField(blank=True,null=True)
	concerned_hostels = models.ManyToManyField(Hostels)
	issuing_authority = models.CharField(max_length=60)
	class meta:
		ordering=['-date_posted']
	def __str__(self):
		return "{}".format(self.title)
	def save(self,*args,**kwargs):
		self.label = slugify(self.label)
		super(Notices,self).save(*args,**kwargs)
	def get_absolute_url(self):
		#returning to Home Page
		return reverse('homepage')
class ChiefWardens(models.Model):
	hostel_type_choices=(
				('1','Boys'),
				('2','Girls')
	)
	Name = models.CharField(max_length=50)
	email = models.CharField(max_length=60)
	contact = models.CharField(max_length=15)
	hostel_type = models.CharField(max_length=1,choices=hostel_type_choices)
	def __str__(self):
		return "{}".format(self.Name)
class Wardens(models.Model):
	Name = models.CharField(max_length=50)
	email = models.CharField(max_length=60)
	contact = models.CharField(max_length=15)
	hostel = models.ForeignKey(Hostels,on_delete=models.CASCADE)
	def __str__(self):
		return "{}".format(self.Name)
class Hostel_Management_Committee(models.Model):
	hostel = models.OneToOneField(Hostels,on_delete=models.CASCADE)
	chief_warden_email = models.ForeignKey(ChiefWardens,on_delete=models.CASCADE)
	warden_email = models.CharField(max_length=50)
	care_taker_email = models.CharField(max_length=50)
	hostel_president_email = models.CharField(max_length=50,blank=True)
	hostel_manager_email = models.CharField(max_length=50,blank=True)
	hostel_secretary_email = models.CharField(max_length=50,blank=True)
class Mess_Management_Committee(models.Model):
	hostel = models.OneToOneField(Hostels,on_delete=models.CASCADE)
	mess_secretary_email = models.CharField(max_length=50)
	mess_manager_email =  models.CharField(max_length=50)


class General_Authority(models.Model):
	Name = models.CharField(max_length=60)
	contact_person = models.CharField(max_length=50)
	designations = models.CharField(max_length=60)
	contact_email = models.CharField(max_length=60)

