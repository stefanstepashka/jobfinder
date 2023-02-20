from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, JobApplication, Company, Resume
# Create your views here.
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import ResumeForm, JobApplicationForm, CompanyRegistrationForm
from django.contrib import messages
from django.core import cache

def main(request):
    return render(request, 'main.html')


def job(request):
    search_job = request.GET.get('search_job', '')
    salary_min = request.GET.get('salary_min', '')
    salary_max = request.GET.get('salary_max', '')
    job_type = request.GET.get('job_type', '')

    jobs = Job.objects.all().select_related('company').only(
        'title', 'description', 'salary', 'company__name')

    if job_type:
        if job_type == 'remote':
            jobs = jobs.filter(is_remote=True)
        else:
            jobs = jobs.filter(is_remote=False)

    if salary_min or salary_max:
        if salary_min:
            try:
                salary_min = int(salary_min)
                jobs = jobs.filter(salary__gte=salary_min)
            except ValueError:
                pass

        if salary_max:
            try:
                salary_max = int(salary_max)
                jobs = jobs.filter(salary__lte=salary_max)
            except ValueError:
                pass

    if search_job:
        jobs = jobs.filter(title__icontains=search_job)

    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs.html', context={
        'jobs': page_obj, 'search_job': search_job,
        'salary_min': salary_min, 'salary_max': salary_max, 'job_type': job_type})


def job_detail(request, id):
    jobs = get_object_or_404(Job, id=id)
    user = request.user
    resume = user.resume_set.first()

    already_applied = JobApplication.objects.filter(job=jobs, user=user).exists()
    num_applications = JobApplication.objects.filter(job=jobs).count()
    return render(request, 'job_detail.html', context={
        'jobs': jobs,
        'already_applied': already_applied,
        'num_applications': num_applications,
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('main')


def resumes(request):
    resume = Resume.objects.all()
    query = request.GET.get('query')
    if query:
        resume = resume.filter(Q(title__icontains=query))

    return render(request, 'resumes.html', context={'resume': resume})


@login_required
def user_profile(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'user_profile.html', context={'resumes':resumes})


@login_required
def all_resumes(request):

    resumes = Resume.objects.filter(user=request.user).only('title')


    return render(request, 'all_resumes.html', {'resumes': resumes})


@login_required
def create_resume(request):
    if request.method == 'POST':
        resumeform = ResumeForm(request.POST)
        if resumeform.is_valid():
            if resumeform.is_valid():
                resume = resumeform.save(commit=False)
                resume.user = request.user
                resume.save()
                resumeform.save_m2m()
                return redirect('user_profile')
    else:
        resumeform = ResumeForm(request.POST)
    return render(request, 'create_resume.html', {'resumeform': resumeform})


@login_required
def edit_resume(request, id):
    resume = get_object_or_404(Resume, id=id)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('all_resumes')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'edit_resume.html', {'resume': resume, 'form': form})


@login_required
def apply_to_job(request, id):
    job = get_object_or_404(Job, id=id)
    user = request.user
    resume = user.resume_set.first()
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.user = user
            job_application.job = job
            job_application.save()
            return redirect('job_detail', id=id)
    else:
        form = JobApplicationForm(user=request.user)

    return render(request, 'job_detail.html', context={'form': form, 'jobs': job})


def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    return render(request, 'resume_detail.html', context={'resume': resume})


def company(request):
    company = Company.objects.all()
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('main')
    else:
        form = CompanyRegistrationForm(request.POST)

    return render(request, 'company_signin.html', context={'company': company, 'company_form': form})