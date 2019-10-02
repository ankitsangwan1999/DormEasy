from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from noticeapp.models import Hostels
from django.contrib.auth.models import User
# Create your models here.
from ckeditor_uploader.fields import RichTextUploadingField
class Complaint(models.Model):
	status_choices = (
		('0',"Pending"),
		('1',"Acknowledged"),
		('2',"Resolved")
	)
	title = models.CharField(max_length=150)
	complaint = RichTextUploadingField(max_length=500)
	first_complainer = models.ForeignKey(User,on_delete=models.CASCADE)
	status = models.CharField(max_length=1,choices=status_choices)
	concerned_authority = models.CharField(max_length=60)
	number = models.PositiveIntegerField(default=1)
	related_hostel = models.ForeignKey(Hostels,on_delete=models.CASCADE)
	date_added = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return "{}".format(self.title)

class Complainers(models.Model):
	user_id = models.ForeignKey(User,on_delete=models.CASCADE)
	complaint_id = models.ForeignKey(Complaint,on_delete=models.CASCADE)

class Comment(models.Model):
	comment = models.TextField()
	# reply = 
	user =  models.ForeignKey(User,on_delete=models.CASCADE)
	complaint = models.ForeignKey(Complaint,on_delete=models.CASCADE)
	date_created = models.DateTimeField(default = timezone.now)
	is_review = models.BooleanField(default = False)
	class Meta:
		ordering = ['-date_created']
	def __str__(self):
		return "Comment on ::{}:: {}::".format(self.complaint.title,self.comment)
