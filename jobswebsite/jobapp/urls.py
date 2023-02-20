from django.contrib import admin
from django.urls import path, include
from .views import main, job, job_detail, user_login, \
    user_signup, user_logout, user_profile,create_resume, all_resumes, edit_resume, apply_to_job, resumes, resume_detail, company
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page



urlpatterns = [
    path('', main, name='main'),
    path('jobs/', cache_page(30)(job), name='job'),
    path('jobs/<int:id>', job_detail, name='job_detail'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('createresume/', create_resume, name='create_resume'),
    path('all_resumes/', all_resumes, name='all_resumes'),
    path('edit_resume/<int:id>', edit_resume, name='edit_resume'),
    path('apply_to_job/<int:id>', apply_to_job, name='apply_to_job'),
    path('resumes', resumes, name='resumes'),
    path('resumes/<int:resume_id>', resume_detail, name='resume_detail'),
    path('company', company, name='company')
]
