from django.db import models
from django.contrib.auth.models import User
from noticeapp.models import Hostels


class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE) # here user becomes = email of
	regno = models.PositiveIntegerField()
# Imp: In our database 1st value of each choice tuple is stored and hence while  
# assigning values to them we should assign accordingly.
# i.e. 1 is stored if we choose 1st so, while assigning we should assign 1 only
# not 1st.
	Sem_Choices=(
			('1','1st'),('2','2nd'),('3','3rd'),('4','4th'),
			('5','5th'),('6','6th'),('7','7th'),('8','8th')
		)
	Gender_Choices = (
        ('0', 'Male'),
        ('1', 'Female')
    )
	sem = models.CharField(max_length=1,choices=Sem_Choices)
	gender = models.CharField(max_length=1,choices=Gender_Choices)
	hostel_alloted = models.ForeignKey(Hostels,null=True,on_delete=models.SET_NULL)
	# isOnline = models.BooleanField(default=False)

	def __str__(self):
		return "{} {}".format(self.user,"Profile")

class Reg_Students(models.Model):
	Fullname = models.CharField(null=True,max_length=50)
	Regno = models.CharField(max_length=10)
	Sem = models.CharField(max_length=1)
	Gender = models.CharField(max_length=1)

	def __str__(self):
		return "{}".format(self.Regno)




