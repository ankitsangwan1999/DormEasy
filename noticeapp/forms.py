from django import forms
from .models import Notices,Hostels
from multiselectfield import MultiSelectField


class AddNoticeForm(forms.ModelForm):
	
	class Meta:
		model = Notices
		fields = ['title','label','description','notice_file','val_time','concerned_hostels','issuing_authority']
		# val_time = forms.DateField(input_formats=['yyyy-mm-dd'])
		concerned_hostels=forms.ModelChoiceField(
								queryset=Hostels.objects.all(),
								to_field_name="hostel_name")
		widgets = {'title':forms.TextInput(
									attrs={'id': "id_title", 'type':"text",
										   'class': "validate",
									       'requred': True}),
				'label':forms.TextInput(attrs={'id':"id_label",
											'type':"text",'class':"validate",
											'required':True}),
				'description':forms.Textarea(attrs={'type':"textarea",'id':"id_content"}),
				'notice_file':forms.FileInput(),				
				'val_time':forms.DateInput(attrs={'class':"datepicker"}),
			}




