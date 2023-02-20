from django.contrib import admin
from .models import Resume, Company, Job, JobApplication, Category
# Register your models here.
admin.site.register(Resume)

admin.site.register(Category)
admin.site.register(JobApplication)


class CompanyCategory(admin.ModelAdmin):
    list_display = ('name', 'number', 'location', 'description')
    search_fields = ('name', 'description', 'location')


class AdminJobCategory(admin.ModelAdmin):
    list_display = ('title', 'location', 'salary', 'is_remote', 'published_at')
    list_filter = ('is_remote', 'published_at')
    search_fields = ('title', 'description', 'location')
    filter_horizontal = ('categories',)


admin.site.register(Job, AdminJobCategory)
admin.site.register(Company, CompanyCategory)