from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    number = models.IntegerField()
    description = models.TextField()
    location = models.CharField(max_length=255)
    website = models.URLField(max_length=255)

    def __str__(self):
        return self.name


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    skills = models.TextField(null=True)
    education = models.TextField(null=True)
    experience = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('edit_resume', args=[str(self.id)])

    def get_url(self):
        return reverse('resume_detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.PositiveIntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='jobs')
    is_remote = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job_detail', args=[str(self.id)])


class JobApplication(models.Model):
    APPLICATION_STATUS = [('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='Pending')

    def __str__(self):
        return f'{self.user.username} - {self.job.title}'