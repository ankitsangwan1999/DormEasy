"""dormEasy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from noticeapp import views as noticeapp_views
from users import views as users_views
from complain import views as complain_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',noticeapp_views.home,name='homepage'),
    path('notice_board/',noticeapp_views.notice_board,name='specific-notice-board'),
    path('AddNotice/',noticeapp_views.NoticeCreateView.as_view(),name="addnotice"),
    path('notice1/',noticeapp_views.NoticeDetailView.as_view(),name="notice-detail"),
    # path('AddNotice',views.Notice),
    path('log_in/',users_views.login_view,name="users-login"),
    path('new_profile/',users_views.create_profile,name="users-new-profile"),
    path('register/',users_views.register,name="users-register"),
    path('log_out/',users_views.logout_view,name = "users-logout"),
    path('profile/',users_views.profile,name="users-profile"),
    path('new-complain/',complain_views.new_complain,name="new_complain"),
    path('all-complains/',complain_views.AllComplains.as_view(),name="all_complains"),
    path('my-complains/',complain_views.MyComplains.as_view(),name="my_complains"),
    path('all-complains/<int:pk>',complain_views.ComplainDetailView.as_view(),name="complain-detail"),
    path('all-complains/<int:pk>/comment/',complain_views.CommentView,name="post-comment"),
    path("comps-on-me/",complain_views.CompsOnMe,name="complains_on_me"),
    path("resolved-comps/",complain_views.ResolvedComplains,name="reviews_on_me"),
    path("give-fb-on-res/",complain_views.GiveFbRes,name="give_feedback"),

    path("dislike/",complain_views.DislikeComplains,name="dislike"),

    path("contact_info",noticeapp_views.Contact,name="mnnit_contact_details"),

    path('password-reset',users_views.PasswordResetUView.as_view(template_name='users/password_reset.html'),name="password_reset"),
    path('password_reset_done',users_views.PasswordResetUView.as_view(template_name="users/password_reset_done.html"),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
            users_views.PasswordResetConfirmUView.as_view(template_name='users/password_reset_confirm.html'),
            name='password_reset_confirm'),
    path('password-reset-complete/',
            users_views.PasswordResetCompleteUView.as_view(template_name='users/password_reset_complete.html'),
            name='password_reset_complete'),
    ###
    path('ckeditor/',include('ckeditor_uploader.urls')), # to make the file uploads from the ckeditor's RichTextUploadingField to work
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)