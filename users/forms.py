from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeFormfrom django.contrib.auth.models import User 
# from .models import CustomUser
from django.contrib.auth.models import User
from .models import Profile
from noticeapp.models import Hostels

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email']

class ProfileUpdateForm(forms.ModelForm):
	

	sem = forms.CharField()
	#Model Choice Field is apt for updating a Foreign key
	# here to_field_name is optional without which it will try to assing the pk value to
	# the hostel_alloted attribute of Profile Model hence wrong. So assigning it ensures
	# which attribute of the Hostel Model is used to assign the value.
	hostel_alloted = forms.ModelChoiceField(queryset=Hostels.objects.all(),to_field_name="hostel_name")
	class Meta:
		model = Profile
		fields = ['sem','hostel_alloted']












### OLD STUFF
# class CustomUserCreationForm(UserCreationForm):
# 	class Meta:
# 		model = CustomUser
# 		fields = ('username','email')

# class CustomUserChangeForm(UserChangeForm):
# 	class Meta:
# 		model = CustomUser
# 		fields = ('username','email')
# 		