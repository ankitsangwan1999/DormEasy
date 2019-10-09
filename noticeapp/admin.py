from django.contrib import admin
from . import models
class HostelsAdmin(admin.ModelAdmin):
	model = models.Hostels
	list_display = ['id','hostel_name','Type']
	# Below Code Works when any one of the fields is a foreign key
	# def get_name(self,obj):
	# 	return obj.Hostels.Type
	# get_name.short_description = 'Type'#Renames column head
class NoticesAdmin(admin.ModelAdmin):
	model = models.Notices
	list_display = ['title','label','issuing_authority','date_posted','val_time']
	# Below Code Works when any one of the fields is a foreign key
	# def description(self,obj):
		# return obj.Hostels.Type
	# get_name.short_description = 'Type'#Renames column head
class HMCAdmin(admin.ModelAdmin):
	model= models.Hostel_Management_Committee
	list_display = ['hostel','chief_warden_email','warden_email','care_taker_email','hostel_president_email']
class MMCAdmin(admin.ModelAdmin):
	model = models.Mess_Management_Committee
	list_display = ['hostel','mess_secretary_email','mess_manager_email']
class CWAdmin(admin.ModelAdmin):
	model= models.ChiefWardens
	list_display = ['id','Name','email','contact','hostel_type']
class WAdmin(admin.ModelAdmin):
	model= models.Wardens
	list_display = ['Name','email','contact','hostel']	
class GAAdmin(admin.ModelAdmin):
	model = models.General_Authority
	list_display = ['id','Name','contact_person','designations','contact_email']

# Register your models here.
admin.site.register(models.Hostels,HostelsAdmin)
admin.site.register(models.Notices,NoticesAdmin)
admin.site.register(models.Hostel_Management_Committee,HMCAdmin)
admin.site.register(models.Mess_Management_Committee,MMCAdmin)
admin.site.register(models.ChiefWardens,CWAdmin)
admin.site.register(models.Wardens,WAdmin)
admin.site.register(models.General_Authority,GAAdmin)
