from django import forms
from multiselectfield import MultiSelectField
from .models import Complaint,Comment

class AddComplainForm(forms.ModelForm):
	
	class Meta:
		model = Complaint
		fields = ['title','complaint','concerned_authority','status']
		widgets = {'title':forms.TextInput(
									attrs={'id':"id_title" ,'type':"text" ,
									'class':"validate",
									'requred':True}),
				'complaint':forms.Textarea(attrs={'type':"textarea",'id':"id_content"}),
				'concerned_authority':forms.TextInput(attrs={'id':"id_concerned_authority" ,'type':"text" ,
									'class':"validate",
									'requred':True})
		}

class AddComment(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']


