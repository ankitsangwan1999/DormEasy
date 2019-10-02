from django.contrib import admin
from . import models
# Register your models here.
class ComplaintAdmin(admin.ModelAdmin):
	list_display = ['title','first_complainer','status','concerned_authority','related_hostel','number','date_added']

class ComplainersAdmin(admin.ModelAdmin):
	list_display = ['user_id','complaint_id']
class CommentAdmin(admin.ModelAdmin):
	list_display = ['user','comment','complaint','date_created','is_review']
admin.site.register(models.Complaint,ComplaintAdmin)
admin.site.register(models.Complainers,ComplainersAdmin)
admin.site.register(models.Comment,CommentAdmin)
