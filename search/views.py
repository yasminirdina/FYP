from django.db.models import Q
import dashboard.models
import search.models
from .forms import DataForm
from django.shortcuts import render, redirect
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
        uni = uni.filter(uni__icontains=uni_contains)
    if is_valid_queryparam(course_contains):
        course = course.filter(course__icontains=course_contains)
    if is_valid_queryparam(job_contains):
        job = job.filter(job__icontains=job_contains)
        
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

    # if is_valid_queryparam(uni_contains):
    #     uni = uni.filter(uni__icontains=uni_contains)
    # if is_valid_queryparam(course_contains):
    #     course = course.filter(course__icontains=course_contains)

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
        # 'allUni':uni,
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
        'allBridge':courseuni,
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
        # 'allJobs': job,
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

        course = search.models.Course.objects.all()
        uni = search.models.University.objects.all()
        jobs = search.models.Jobs.objects.all()
        courseuni = search.models.UniCourseBridge.objects.all()
        uni_contains = request.GET.get('uni_contains')
        course_contains = request.GET.get('course_contains')
        jobs_contains = request.GET.get('jobs_contains')
        uniorcourse_contains = request.GET.get('uniorcourse_contains')
        uni_filter = request.GET.get('uni_filter')
        course_filter = request.GET.get('course_filter')
        jobs_filter = request.GET.get('jobs_filter')
        
        if is_valid_queryparam(uni_contains):
            uni = uni.filter(uni__icontains=uni_contains)
        if is_valid_queryparam(course_contains):
            course = course.filter(course__icontains=course_contains)
        if is_valid_queryparam(jobs_contains):
            jobs = jobs.filter(jobs__icontains=jobs_contains)

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
            'allJobs':jobs,
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

        course = search.models.Course.objects.all()
        uni = search.models.University.objects.all()
        courseuni = search.models.UniCourseBridge.objects.all()
        uni_contains = request.GET.get('uni_contains')
        course_contains = request.GET.get('course_contains')
        uniorcourse_contains = request.GET.get('uniorcourse_contains')
        uni_filter = request.GET.get('uni_filter')
        course_filter = request.GET.get('course_filter')

        if is_valid_queryparam(uni_contains):
            uni = uni.filter(uni__icontains=uni_contains)
        if is_valid_queryparam(course_contains):
            course = course.filter(course__icontains=course_contains)

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
            'allUni':uni,
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

        course = search.models.Course.objects.all()
        uni = search.models.University.objects.all()
        courseuni = search.models.UniCourseBridge.objects.all()
        uni_contains = request.GET.get('uni_contains')
        course_contains = request.GET.get('course_contains')
        uniorcourse_contains = request.GET.get('uniorcourse_contains')
        # uni_filter = request.GET.get('uni_filter')
        # course_filter = request.GET.get('course_filter')
        # jobs_filter = request.GET.get('jobs_filter')

        if is_valid_queryparam(course_contains):
            course = course.filter(course__icontains=course_contains)
        if is_valid_queryparam(uni_contains):
            uni = uni.filter(uni__icontains=uni_contains)

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
            'allUni':uni,
            'allBridge':courseuni,
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

        course = search.models.Course.objects.all()
        job = search.models.Jobs.objects.all()
        coursejob = search.models.JobCourseBridge.objects.all()
        course_contains = request.GET.get('course_contains')
        job_contains = request.GET.get('job_contains')
        joborcourse_contains = request.GET.get('joborcourse_contains')
        # course_filter = request.GET.get('course_filter')
        # job_filter = request.GET.get('job_filter')

        if is_valid_queryparam(job_contains):
            job = job.filter(job__icontains=job_contains)
        if is_valid_queryparam(course_contains):
            course = course.filter(course__icontains=course_contains)

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
            'allJobs':job,
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

#create,update,delete for admin
def createData(request, user_id):
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
        form = DataForm()

        if request.method == "POST":
            # print(request.POST)
            form = DataForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('search:all-admin', user_id=user_id)

        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'form' : form,
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/dataForm.html', context)

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

def updateData(request, user_id, pk):
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
        
        data = search.models.UniCourseBridge.objects.get(id=pk)
        form = DataForm(instance=data)
        if request.method == "POST":
            # print(request.POST)
            form = DataForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                return redirect('search:all-admin', user_id=user_id)

        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'form' : form,
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/dataForm.html', context)

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

def deleteData(request, user_id, pk):
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
        
        data = search.models.UniCourseBridge.objects.get(id=pk)
        if request.method == "POST":
            # data.delete()
            # return redirect(reverse('search:index-admin'))
            return redirect('search:all-admin', user_id=user_id)
            
        context = {
                'user_id': user_id, 
                'test': urlTest, 
                'blog': urlBlog, 
                'quiz': urlQuiz,
                'search': urlSearch, 
                'dashboard': urlDashboard, 
                'logout': urlLogout,
                'data' : data.course.id,
                # 'allCourse' : course,
                # 'allUni':uni,
                # 'allJobs':jobs,
                # 'allBridge':courseuni,
                }
        return render(request, 'search/admin/deleteData.html', context)

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
