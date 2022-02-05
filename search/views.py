from django.db.models import Q
import dashboard.models
import search.models
from .forms import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

def is_valid_queryparam(param):
    return param != '' and param is not None

def userid(user_id):
    if 'S' in user_id:
        dashboardNav = " Pelajar"
    elif 'P' in user_id:
        dashboardNav = " Penjaga"
    elif 'T' in user_id:
        dashboardNav = " Guru"
    else: #user type in english/invalid e.g. student, parent, teacher, typos
        dashboardNav = " Pengguna"
    return dashboardNav

#user
def searchMain(request, user_type, user_id):

    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')
    
    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    
    context = { 
        'dashboardNav': userid(user_id),  
        'user_type': user_type, 
        'user_id': user_id, 
        'username': username,
        'test': urlTest, 
        'blog': urlBlog, 
        'quiz': urlQuiz, 
        'search': urlSearch, 
        'dashboard':urlDashboard,
        'logout': urlLogout 
    } 
    return render(request,'search/user/search.html', context)

def searchAll(request, user_type, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')
    
    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    
    course = search.models.Course.objects.all()
    uni = search.models.University.objects.all()
    job = search.models.Jobs.objects.all()
    courseuni = search.models.UniCourseBridge.objects.all()
    uni_contains = request.GET.get('uni_contains')
    course_contains = request.GET.get('course_contains')
    job_contains = request.GET.get('job_contains')
    uniorcourse_contains = request.GET.get('uniorcourse_contains')
    uni_filter = request.GET.get('uni_filter')
    course_filter = request.GET.get('course_filter')
    jobs_filter = request.GET.get('jobs_filter')

    if is_valid_queryparam(uni_contains):
        if is_valid_queryparam(course_contains):
            if is_valid_queryparam(job_contains):
                uni = uni.filter(uni__icontains=uni_contains)
                course = course.filter(course__icontains=course_contains)
                job = job.filter(job__icontains=job_contains)
            else:
                uni = uni.filter(uni__icontains=uni_contains)
                course = course.filter(course__icontains=course_contains)
                job = ""
        else:
            uni = uni.filter(uni__icontains=uni_contains)
            course = ""
            job = ""

    elif is_valid_queryparam(course_contains):
        if is_valid_queryparam(job_contains):
            uni = ""
            course = course.filter(course__icontains=course_contains)
            job = job.filter(job__icontains=job_contains)
        else:
            course = course.filter(course__icontains=course_contains)
            uni = ""
            job = ""
        
    elif is_valid_queryparam(job_contains):
        job = job.filter(job__icontains=job_contains)
        course = ""
        uni = ""    
        
    context = { 
        'dashboardNav': userid(user_id),  
        'user_type': user_type, 
        'user_id': user_id, 
        'username': username,
        'test': urlTest, 
        'blog': urlBlog, 
        'quiz': urlQuiz, 
        'search': urlSearch, 
        'dashboard':urlDashboard,
        'logout': urlLogout, 
        'allCourse' : course,
        'allUni':uni,
        'allJobs':job,
        'allBridge':courseuni,
        }
    return render(request, 'search/user/searchAll.html', context)

def searchUni(request, user_type, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')
    
    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    
    course = search.models.Course.objects.all()
    uni = search.models.University.objects.all()
    courseuni = search.models.UniCourseBridge.objects.all()
    uni_contains = request.GET.get('uni_contains')
    course_contains = request.GET.get('course_contains')
    uniorcourse_contains = request.GET.get('uniorcourse_contains')
    uni_filter = request.GET.get('uni_filter')
    course_filter = request.GET.get('course_filter')

    uniList=[]
    for j in uni:
        uniList.append(j)
    
    if is_valid_queryparam(uni_contains):
        uni2 = list(uni.filter(uni__icontains=uni_contains))
        uniList=[]
        for j in uni2:
            uniList.append(j)

    elif is_valid_queryparam(course_contains):
        course = course.filter(course__icontains=course_contains)
        uniList=[]
        for x in course:
            courseUni = courseuni.filter(course_id=x.id)
            for y in courseUni:
                uni3 = list(uni.filter(id=y.uni_id))
                for j in uni3:
                    uniList.append(j)

    context = { 
        'dashboardNav': userid(user_id),  
        'user_type': user_type, 
        'user_id': user_id, 
        'username': username,
        'test': urlTest, 
        'blog': urlBlog, 
        'quiz': urlQuiz, 
        'search': urlSearch, 
        'dashboard':urlDashboard,
        'logout': urlLogout, 
        'allCourse' : course,
        'allUni':uniList,
        'allBridge':courseuni,
    } 
    return render(request,'search/user/searchUni.html', context)

def searchCourse(request, user_type, user_id): 
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')
    
    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    
    course = search.models.Course.objects.all()
    uni = search.models.University.objects.all()
    courseuni = search.models.UniCourseBridge.objects.all()
    uni_contains = request.GET.get('uni_contains')
    course_contains = request.GET.get('course_contains')
    uniorcourse_contains = request.GET.get('uniorcourse_contains')
    # uni_filter = request.GET.get('uni_filter')
    # course_filter = request.GET.get('course_filter')
    # jobs_filter = request.GET.get('jobs_filter')

    courseList=[]
    for j in course:
        courseList.append(j)
    # print(jobList)
    
    if is_valid_queryparam(course_contains):
        course2 = list(course.filter(course__icontains=course_contains))
        courseList=[]
        for j in course2:
            courseList.append(j)
        # print(jobList)

    elif is_valid_queryparam(uni_contains):
        uni = uni.filter(uni__icontains=uni_contains)
        courseList=[]
        for x in uni:
            courseUni = courseuni.filter(uni_id=x.id)
            for y in courseUni:
                course3 = list(course.filter(id=y.course_id))
                for j in course3:
                    courseList.append(j)
                    # print(courseList)
        # print(jobList)

    context = { 
        'dashboardNav': userid(user_id),  
        'user_type': user_type, 
        'user_id': user_id, 
        'username': username,
        'test': urlTest, 
        'blog': urlBlog, 
        'quiz': urlQuiz, 
        'search': urlSearch, 
        'dashboard':urlDashboard,
        'logout': urlLogout, 
        # 'allCourse' : course,
        'allCourse' : courseList,
        'allUni': uni,
        'allBridge':courseuni
        }
    return render(request, 'search/user/searchCourse.html', context)

def searchJobs(request, user_type, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')
    
    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    
    course = search.models.Course.objects.all()
    job = search.models.Jobs.objects.all()
    coursejob = search.models.JobCourseBridge.objects.all()
    course_contains = request.GET.get('course_contains')
    job_contains = request.GET.get('job_contains')
    joborcourse_contains = request.GET.get('joborcourse_contains')
    # course_filter = request.GET.get('course_filter')
    # job_filter = request.GET.get('job_filter')

    jobList=[]
    for j in job:
        jobList.append(j)
    # print(jobList)
    
    if is_valid_queryparam(job_contains):
        job2 = list(job.filter(job__icontains=job_contains))
        jobList=[]
        for j in job2:
            jobList.append(j)
        # print(jobList)

    elif is_valid_queryparam(course_contains):
        course = course.filter(course__icontains=course_contains)
        jobList=[]
        for x in course:
            courseJob = coursejob.filter(course_id=x.id)
            for y in courseJob:
                job3 = list(job.filter(id=y.job_id))
                for j in job3:
                    jobList.append(j)
                    print(jobList)
        # print(jobList)

    context = { 
        'dashboardNav': userid(user_id),  
        'user_type': user_type, 
        'user_id': user_id, 
        'username': username,
        'test': urlTest, 
        'blog': urlBlog, 
        'quiz': urlQuiz, 
        'search': urlSearch, 
        'dashboard':urlDashboard,
        'logout': urlLogout, 
        'allCourse' : course,
        'allJobs': jobList,
        'allBridge':coursejob,
        }
    return render(request, 'search/user/searchJobs.html', context)

def coursePage(request, user_type, user_id, course_id): 
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')
    
    currentCourse = search.models.Course.objects.get(id=course_id)
    uni = search.models.University.objects.all()
    job = search.models.Jobs.objects.all()
    uniCourseBridge = search.models.UniCourseBridge.objects.filter(course_id=course_id)
    jobCourseBridge = search.models.JobCourseBridge.objects.filter(course_id=course_id)

    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    
    context = { 
        'dashboardNav': userid(user_id),  
        'user_type': user_type, 
        'user_id': user_id,
        'course_id': course_id, 
        'username': username,
        'test': urlTest, 
        'blog': urlBlog, 
        'quiz': urlQuiz, 
        'search': urlSearch, 
        'dashboard':urlDashboard,
        'logout': urlLogout,
        'currentCourse': currentCourse,
        'uni': uni,
        'job': job,
        'uniCourseBridge': uniCourseBridge,
        'jobCourseBridge': jobCourseBridge
        }
    return render(request, 'search/user/page/coursePage.html', context)

def uniPage(request, user_type, user_id, uni_id): 
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')
    
    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    
    currentUni = search.models.University.objects.get(id=uni_id)
    course = search.models.Course.objects.all()
    uniCourseBridge = search.models.UniCourseBridge.objects.filter(university_id=uni_id)

    context = { 
        'dashboardNav': userid(user_id),  
        'user_type': user_type, 
        'user_id': user_id,
        'uni_id': uni_id, 
        'username': username,
        'test': urlTest, 
        'blog': urlBlog, 
        'quiz': urlQuiz, 
        'search': urlSearch, 
        'dashboard':urlDashboard,
        'logout': urlLogout,
        'currentUni': currentUni,
        'course': course,
        'bridge': uniCourseBridge
        }
    return render(request, 'search/user/page/uniPage.html', context)

def jobPage(request, user_type, user_id, job_id): 
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')
    
    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    
    currentJob = search.models.Jobs.objects.get(id=job_id)
    course = search.models.Course.objects.all()
    jobCourseBridge = search.models.JobCourseBridge.objects.filter(job_id=job_id)

    context = { 
        'dashboardNav': userid(user_id),  
        'user_type': user_type, 
        'user_id': user_id,
        'job_id': job_id, 
        'username': username,
        'test': urlTest, 
        'blog': urlBlog, 
        'quiz': urlQuiz, 
        'search': urlSearch, 
        'dashboard':urlDashboard,
        'logout': urlLogout,
        'currentJob': currentJob,
        'course': course,
        'jobCourseBridge': jobCourseBridge
        }
    return render(request, 'search/user/page/jobPage.html', context)

#admin
def searchMainAdmin(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        context = {
            'user_id': user_id, 
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz,
            'search': urlSearch, 
            'dashboard': urlDashboard, 
            'logout': urlLogout,
            }
        return render(request, 'search/admin/searchAdmin.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def allAdmin(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'

        course = search.models.Course.objects.all()
        uni = search.models.University.objects.all()
        job = search.models.Jobs.objects.all()
        courseuni = search.models.UniCourseBridge.objects.all()
        uni_contains = request.GET.get('uni_contains')
        course_contains = request.GET.get('course_contains')
        job_contains = request.GET.get('job_contains')
        uniorcourse_contains = request.GET.get('uniorcourse_contains')
        uni_filter = request.GET.get('uni_filter')
        course_filter = request.GET.get('course_filter')
        jobs_filter = request.GET.get('jobs_filter')

        if is_valid_queryparam(uni_contains):
            if is_valid_queryparam(course_contains):
                if is_valid_queryparam(job_contains):
                    uni = uni.filter(uni__icontains=uni_contains)
                    course = course.filter(course__icontains=course_contains)
                    job = job.filter(job__icontains=job_contains)
                else:
                    uni = uni.filter(uni__icontains=uni_contains)
                    course = course.filter(course__icontains=course_contains)
                    job = ""
            else:
                uni = uni.filter(uni__icontains=uni_contains)
                course = ""
                job = ""

        elif is_valid_queryparam(course_contains):
            if is_valid_queryparam(job_contains):
                uni = ""
                course = course.filter(course__icontains=course_contains)
                job = job.filter(job__icontains=job_contains)
            else:
                course = course.filter(course__icontains=course_contains)
                uni = ""
                job = ""
            
        elif is_valid_queryparam(job_contains):
            job = job.filter(job__icontains=job_contains)
            course = ""
            uni = ""    

        context = {
            'user_id': user_id, 
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz,
            'search': urlSearch, 
            'dashboard': urlDashboard, 
            'logout': urlLogout,
            'allCourse' : course,
            'allUni':uni,
            'allJobs':job,
            'allBridge':courseuni,
        }
        return render(request, 'search/admin/allAdmin.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def uniAdmin(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'

        course = search.models.Course.objects.all()
        uni = search.models.University.objects.all()
        courseuni = search.models.UniCourseBridge.objects.all()
        uni_contains = request.GET.get('uni_contains')
        course_contains = request.GET.get('course_contains')
        uniorcourse_contains = request.GET.get('uniorcourse_contains')
        uni_filter = request.GET.get('uni_filter')
        course_filter = request.GET.get('course_filter')

        uniList=[]
        for j in uni:
            uniList.append(j)
        
        if is_valid_queryparam(uni_contains):
            uni2 = list(uni.filter(uni__icontains=uni_contains))
            uniList=[]
            for j in uni2:
                uniList.append(j)

        elif is_valid_queryparam(course_contains):
            course = course.filter(course__icontains=course_contains)
            uniList=[]
            for x in course:
                courseUni = courseuni.filter(course_id=x.id)
                for y in courseUni:
                    uni3 = list(uni.filter(id=y.uni_id))
                    for j in uni3:
                        uniList.append(j)

        context = { 
            'dashboardNav': userid(user_id),  
            'user_id': user_id, 
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz, 
            'search': urlSearch, 
            'dashboard':urlDashboard,
            'logout': urlLogout, 
            'allCourse' : course,
            'allUni':uniList,
            'allBridge':courseuni,
        }
        return render(request, 'search/admin/uniAdmin.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def courseAdmin(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'

        course = search.models.Course.objects.all()
        uni = search.models.University.objects.all()
        courseuni = search.models.UniCourseBridge.objects.all()
        uni_contains = request.GET.get('uni_contains')
        course_contains = request.GET.get('course_contains')
        uniorcourse_contains = request.GET.get('uniorcourse_contains')
        # uni_filter = request.GET.get('uni_filter')
        # course_filter = request.GET.get('course_filter')
        # jobs_filter = request.GET.get('jobs_filter')

        courseList=[]
        for j in course:
            courseList.append(j)
        
        if is_valid_queryparam(course_contains):
            course2 = list(course.filter(course__icontains=course_contains))
            courseList=[]
            for j in course2:
                courseList.append(j)

        elif is_valid_queryparam(uni_contains):
            uni = uni.filter(uni__icontains=uni_contains)
            courseList=[]
            for x in uni:
                courseUni = courseuni.filter(uni_id=x.id)
                for y in courseUni:
                    course3 = list(course.filter(id=y.course_id))
                    for j in course3:
                        courseList.append(j)

        context = { 
            'dashboardNav': userid(user_id),  
            'user_id': user_id, 
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz, 
            'search': urlSearch, 
            'dashboard':urlDashboard,
            'logout': urlLogout, 
            'allCourse' : courseList,
            'allUni': uni,
            'allBridge':courseuni
        }
        return render(request, 'search/admin/courseAdmin.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def jobsAdmin(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'

        course = search.models.Course.objects.all()
        job = search.models.Jobs.objects.all()
        coursejob = search.models.JobCourseBridge.objects.all()
        course_contains = request.GET.get('course_contains')
        job_contains = request.GET.get('job_contains')
        joborcourse_contains = request.GET.get('joborcourse_contains')
        # course_filter = request.GET.get('course_filter')
        # job_filter = request.GET.get('job_filter')

        jobList=[]
        for j in job:
            jobList.append(j)
        
        if is_valid_queryparam(job_contains):
            job2 = list(job.filter(job__icontains=job_contains))
            jobList=[]
            for j in job2:
                jobList.append(j)

        elif is_valid_queryparam(course_contains):
            course = course.filter(course__icontains=course_contains)
            jobList=[]
            for x in course:
                courseJob = coursejob.filter(course_id=x.id)
                for y in courseJob:
                    job3 = list(job.filter(id=y.job_id))
                    for j in job3:
                        jobList.append(j)
                        print(jobList)

        context = { 
            'dashboardNav': userid(user_id), 
            'user_id': user_id, 
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz, 
            'search': urlSearch, 
            'dashboard':urlDashboard,
            'logout': urlLogout, 
            'allCourse' : course,
            'allJobs': jobList,
            'allBridge':coursejob,
        }
        return render(request, 'search/admin/jobsAdmin.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def courseAdminPage(request, user_id, course_id): 
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'

        currentCourse = search.models.Course.objects.get(id=course_id)
        uni = search.models.University.objects.all()
        job = search.models.Jobs.objects.all()
        uniCourseBridge = search.models.UniCourseBridge.objects.filter(course_id=course_id)
        jobCourseBridge = search.models.JobCourseBridge.objects.filter(course_id=course_id)

        context = { 
            'dashboardNav': userid(user_id),  
            'user_id': user_id,
            'course_id': course_id, 
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz, 
            'search': urlSearch, 
            'dashboard':urlDashboard,
            'logout': urlLogout,
            'currentCourse': currentCourse,
            'uni': uni,
            'job': job,
            'uniCourseBridge': uniCourseBridge,
            'jobCourseBridge': jobCourseBridge
            }
        return render(request, 'search/admin/page/courseAdminPage.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def uniAdminPage(request, user_id, uni_id): 
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'

        currentUni = search.models.University.objects.get(id=uni_id)
        course = search.models.Course.objects.all()
        uniCourseBridge = search.models.UniCourseBridge.objects.filter(university_id=uni_id)

        context = { 
            'dashboardNav': userid(user_id),  
            'user_id': user_id,
            'uni_id': uni_id, 
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz, 
            'search': urlSearch, 
            'dashboard':urlDashboard,
            'logout': urlLogout,
            'currentUni': currentUni,
            'course': course,
            'bridge': uniCourseBridge
            }
        return render(request, 'search/admin/page/uniAdminPage.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def jobAdminPage(request, user_id, job_id): 
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'

        currentJob = search.models.Jobs.objects.get(id=job_id)
        course = search.models.Course.objects.all()
        jobCourseBridge = search.models.JobCourseBridge.objects.filter(job_id=job_id)

        context = { 
            'dashboardNav': userid(user_id),  
            'user_id': user_id,
            'job_id': job_id, 
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz, 
            'search': urlSearch, 
            'dashboard':urlDashboard,
            'logout': urlLogout,
            'currentJob': currentJob,
            'course': course,
            'jobCourseBridge': jobCourseBridge
            }
        return render(request, 'search/admin/page/jobAdminPage.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

#create,update,delete for admin
def createData(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'

        # admin go to the page(initial) without submitting it
        # submitted = False
        
        formUni = createUniversity
        formCourse = createCourse
        formJob = createJob
        formUniCourse = uniCourseCreate 
        formJobCourse = jobCourseCreate
       
        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'formUni': formUni,
                'formCourse':  formCourse,
                'formJob': formJob,
                'formUniCourse': formUniCourse,
                'formJobCourse': formJobCourse
                # 'submitted': submitted,
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/create/createForm.html', context)

def createUniData(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        
        # admin go to the page(initial) without submitting it
        submitted = False
        if request.method == "POST":
            # admin submit the form, it(page) submits to itself, the data is saved in db 
            # then redirect it back to itself(HttpResponse), send the subit status to page
            
            # for create uni
            formUni = createUniversity(request.POST)
            formUniCourse = uniCourseCreate(request.POST)
            if formUni.is_valid():
                if formUniCourse.is_valid():
                    formUni.save()
                    uni = search.models.University.objects.get(uni=formUni.cleaned_data["uni"])
                    new_uniCourse = search.models.UniCourseBridge.objects.create(
                        university_id = uni.id,
                        course = formUniCourse.cleaned_data["course"]
                    ) 
                    new_uniCourse.save()
                    # formUniCourse.save()
                    return HttpResponseRedirect('/carian-maklumat/admin/A1/cipta-rekod-baru/universiti?submitted=True')
           
        else:
            # 1. if they didn't submit, send again form
            # 2. if GET, check if form submitted or not then change to true
            formUni = createUniversity
            formUniCourse = uniCourseCreate
            if 'submitted' in request.GET:
                submitted = True

        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'formUni': formUni,
                'formUniCourse':  formUniCourse,
                'submitted': submitted
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/create/createUniForm.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def createCourseData(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        
        # admin go to the page(initial) without submitting it
        submitted = False
        if request.method == "POST":
            # admin submit the form, it(page) submits to itself, the data is saved in db 
            # then redirect it back to itself(HttpResponse), send the subit status to page

            # for create course
            formCourse = createCourse(request.POST)
            if formCourse.is_valid():
                formCourse.save()
                return HttpResponseRedirect('/carian-maklumat/admin/A1/cipta-rekod-baru/kursus?submitted=True')
           
        else:
            # 1. if they didn't submit, send again form
            # 2. if GET, check if form submitted or not then change to tru
            formCourse = createCourse
            if 'submitted' in request.GET:
                submitted = True

        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'formCourse': formCourse,
                'submitted': submitted
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/create/createCourseForm.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def createJobData(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        
        # admin go to the page(initial) without submitting it
        submitted = False
        if request.method == "POST":
            # admin submit the form, it(page) submits to itself, the data is saved in db 
            # then redirect it back to itself(HttpResponse), send the subit status to page

            # for create job
            formJob = createJob(request.POST)
            formJobCourse = jobCourseCreate(request.POST)
            if formJob.is_valid():
                if formJobCourse.is_valid():
                    formJob.save()
                    job = search.models.Jobs.objects.get(job=formJob.cleaned_data["job"])
                    new_jobCourse = search.models.JobCourseBridge.objects.create(
                        job_id = job.id,
                        course = formJobCourse.cleaned_data["course"]
                    ) 
                    new_jobCourse.save()
                    return HttpResponseRedirect('/carian-maklumat/admin/A1/cipta-rekod-baru/kerjaya?submitted=True')

        else:
            # 1. if they didn't submit, send again form
            # 2. if GET, check if form submitted or not then change to true
            formJob = createJob
            formJobCourse = jobCourseCreate
            if 'submitted' in request.GET:
                submitted = True

        print(submitted)
        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'formJob': formJob,
                'formJobCourse': formJobCourse,
                'submitted': submitted
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/create/createJobForm.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def updateUniData(request, user_id, uni_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'search:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        
        uni = search.models.University.objects.get(id=uni_id)
        uniForm = createUniversity(request.POST or None, instance=uni)
        if request.method == "POST":
            if uniForm.is_valid():
                uniForm.save()
                return redirect('search:all-admin', user_id=user_id)

        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'uni': uni,
                'uniForm': uniForm
                # 'form' : form,
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/update/updateUni.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def updateCourseData(request, user_id, course_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'search:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        
        course = search.models.Course.objects.get(id=course_id)
        courseForm = createCourse(request.POST or None, instance=course)
        if request.method == "POST":
            if courseForm.is_valid():
                courseForm.save()
                return redirect('search:all-admin', user_id=user_id)

        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'course': course,
                'courseForm': courseForm
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/update/updateCourse.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def updateJobData(request, user_id, job_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'

        job = search.models.Jobs.objects.get(id=job_id)
        formJob = createJob(request.POST or None, instance=job)
        if request.method == "POST":
            if formJob.is_valid():
                formJob.save()
                return redirect('search:all-admin', user_id=user_id)

        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'job': job,
                'formJob': formJob,
                # 'form' : form,
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/update/updateJob.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def deleteUniData(request, user_id, uni_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'search:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm' 
        
        uni = search.models.Course.objects.get(id=uni_id)
        uni.delete()

        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'uni' : uni,
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/searchAdmin.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def deleteCourseData(request, user_id, course_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'search:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        
        course = search.models.Course.objects.get(id=course_id)
        course.delete()

        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'course': course
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/searchAdmin.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)

def deleteJobData(request, user_id, job_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'

    if user_id == 'A1':
        urlTest = 'search:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        
        job = search.models.Jobs.objects.get(id=job_id)
        job.delete()

        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'job': job
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/searchAdmin.html', context)

    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        context = {
            'response': response,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout
            }
        return render(request, 'dashboard\searchAdminError.html', context)