from django.contrib import admin
from .models import Profile,Reg_Students
from django.contrib.auth.admin import UserAdmin
##
from import_export.admin import ImportExportModelAdmin  
##
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['first_name','last_name','email','regno','sem','gender','hostel_alloted']
    def first_name(self,instance):
        return instance.user.first_name
    def last_name(self,instance):
        return instance.user.last_name
    def email(self,instance):
        return instance.user.email

class Reg_StudentsAdmin(ImportExportModelAdmin):
   list_display = ['Regno','Fullname','Sem','Gender'] 



admin.site.register(Profile,ProfileAdmin)
admin.site.register(Reg_Students,Reg_StudentsAdmin)















'''
In Try of Custom User Mode But Authentication with regno is not a good idea.
'''

# Register your models here.
##################################################################
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin
# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import CustomUser




# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['fullname','regno','username','email','sem','gender'
#     				,'hostel_alloted','isOnline']
#     fieldsets = (
# 		(None, {'fields': ('regno','email','password','hostel_alloted')}),
# 		('Personal Info',{'fields':('fullname','sem','dob','gender','category')}),
# 		('Permissions', {'fields': ('isOnline','is_superuser', 'is_staff', 'is_active',)}),
# 	)




# admin.site.register(CustomUser, CustomUserAdmin)
##################################################################