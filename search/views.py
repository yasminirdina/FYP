from django.db.models import Q
import dashboard.models
from django.shortcuts import render, redirect
from .models import University, Bridge, Course, Jobs
from .forms import DataForm
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
def search(request, user_type, user_id):

    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    username = currentUserRecord.username
    urlTest = 'dashboard:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    urlProfile = ''
    urlBookmark = ''
    urlReport = ''
    urlChat = ''
    urlSuggestion = ''
    if user_type == "pelajar" and 'S' in user_id:
        # dashboardNav = " Pelajar"
        urlProfile = 'dashboard:profile-settings-nonadmin' #same view for any nonadmin user (display setting)
        urlBookmark = 'dashboard:bookmarks' #same view for any nonadmin user (display bookmark list)
        urlReport = 'dashboard:reports-student' #so far i think report have diff view for every nonadmin type (student view and download, parent view childrens', homeroom teacher can filter, view, dl)
        urlChat = 'dashboard:chat-student' #tbc same view or not, if yes, omit 'student' use same url pattern for all nonadmin
        urlSuggestion = 'dashboard:suggestions-nonadmin' #same view for any nonadmin user (display suggestion list)
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
            'profile': urlProfile,
            'bookmark': urlBookmark, 
            'report': urlReport, 
            'chat': urlChat, 
            'suggestion': urlSuggestion
        } 
        return render(request,'search/user/search.html', context)
    elif user_type == "penjaga" and 'P' in user_id:
        urlProfile = 'dashboard:profile-settings-nonadmin'
        urlBookmark = 'dashboard:bookmarks'
        urlReport = 'dashboard:reports-parent'
        urlChat = 'dashboard:chat-parent'
        urlSuggestion = 'dashboard:suggestions-nonadmin'
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
            'profile': urlProfile,
            'bookmark': urlBookmark, 
            'report': urlReport, 
            'chat': urlChat, 
            'suggestion': urlSuggestion
        } 
        return render(request, 'search/user/search.html', context)
    elif user_type == "guru" and 'T' in user_id:
        urlProfile = 'dashboard:profile-settings-nonadmin'
        urlBookmark = 'dashboard:bookmarks'
        urlReport = 'dashboard:reports-teacher'
        urlChat = 'dashboard:chat-teacher'
        urlSuggestion = 'dashboard:suggestions-nonadmin'
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
            'profile': urlProfile,
            'bookmark': urlBookmark, 
            'report': urlReport, 
            'chat': urlChat, 
            'suggestion': urlSuggestion
        } 
        return render(request, 'search/user/search.html', context)
    else: #no match between user type and user ID huruf part (cth: 'pelajar' and 'A1') OR english user types OR typo
        title = ''
        dashboardNav = ''
        if user_type == 'pelajar':
            title = "Future Cruise: Papan Pemuka Pelajar"
            dashboardNav = "Papan Pemuka Pelajar"
            response = "Halaman ini hanya boleh diakses oleh pelajar."
        elif user_type == 'penjaga':
            title = "Future Cruise: Papan Pemuka Penjaga"
            dashboardNav = "Papan Pemuka Penjaga"
            response = "Halaman ini hanya boleh diakses oleh ibu bapa atau penjaga."
        elif user_type == 'guru':
            title = "Future Cruise: Papan Pemuka Guru"
            dashboardNav = "Papan Pemuka Guru"
            response = "Halaman ini hanya boleh diakses oleh guru."
        else: #user type in english/invalid e.g. student, parent, teacher, typos
            title = "Future Cruise: Papan Pemuka Pengguna"
            dashboardNav = "Papan Pemuka Pengguna"
            response = "Halaman ini tidak wujud." 
        #pass url navbar nonadmin to error template
        context = {
            'title': title, 
            'dashboardNav': dashboardNav, 
            'response': response, 
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
        return render(request, 'dashboard\dashboardIndexNonAdminError.html', context)

def searchAll(request, user_type, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    username = currentUserRecord.username
    urlTest = 'dashboard:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    urlProfile = 'dashboard:profile-settings-nonadmin'
    urlBookmark = ''
    urlReport = ''
    urlChat = ''
    urlSuggestion = ''
    urlLogout = 'dashboard:logout-confirm'
    
    course = Course.objects.all()
    uni = University.objects.all()
    jobs = Jobs.objects.all()
    courseuni = Bridge.objects.all()
    uni_contains = request.GET.get('uni_contains')
    course_contains = request.GET.get('course_contains')
    jobs_contains = request.GET.get('jobs_contains')
    uniorcourse_contains = request.GET.get('uniorcourse_contains')
    # uni_filter = request.GET.get('uni_filter')
    # course_filter = request.GET.get('course_filter')
    # jobs_filter = request.GET.get('jobs_filter')

    if is_valid_queryparam(uni_contains):
        uni = uni.filter(uni__icontains=uni_contains)
    if is_valid_queryparam(course_contains):
        course = course.filter(course__icontains=course_contains)
    # if is_valid_queryparam(jobs_contains):
    #     jobs = jobs.filter(jobs__icontains=jobs_contains)
        
    context = {
        'user_id': user_id,
        'user_type': user_type,
        'username' : username,
        'dashboardNav' : userid(user_id), 
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
    return render(request, 'search/user/searchAll.html', context)

def searchUni(request, user_type, user_id):
    
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    username = currentUserRecord.username
    urlTest = 'dashboard:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    urlProfile = 'dashboard:profile-settings-nonadmin'
    urlBookmark = ''
    urlReport = ''
    urlChat = ''
    urlSuggestion = ''
    urlLogout = 'dashboard:logout-confirm'
    
    course = Course.objects.all()
    uni = University.objects.all()
    jobs = Jobs.objects.all()
    courseuni = Bridge.objects.all()
    uni_contains = request.GET.get('uni_contains')
    course_contains = request.GET.get('course_contains')
    uniorcourse_contains = request.GET.get('uniorcourse_contains')
    uni_filter = request.GET.get('uni_filter')
    course_filter = request.GET.get('course_filter')
    jobs_filter = request.GET.get('jobs_filter')

    if is_valid_queryparam(uni_contains):
        uni = uni.filter(uni__icontains=uni_contains)
    if is_valid_queryparam(course_contains):
        course = course.filter(course__icontains=course_contains)

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = "Papan Pemuka Pelajar"
    elif user_type == 'penjaga':
        dashboardNav = "Papan Pemuka Penjaga"
    elif user_type == 'guru':
        dashboardNav = "Papan Pemuka Guru"
    else: #user type in english/invalid e.g. student, parent, teacher, typos
        dashboardNav = "Papan Pemuka Pengguna"

    context = {
        'user_id': user_id,
        'user_type': user_type,
        'username' : username,
        'dashboardNav' : dashboardNav, 
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
    return render(request, 'search/user/searchUni.html', context)

def searchCourse(request, user_type, user_id):
    
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    username = currentUserRecord.username
    urlTest = 'dashboard:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    urlProfile = 'dashboard:profile-settings-nonadmin'
    urlBookmark = ''
    urlReport = ''
    urlChat = ''
    urlSuggestion = ''
    urlLogout = 'dashboard:logout-confirm'
    
    course = Course.objects.all()
    uni = University.objects.all()
    jobs = Jobs.objects.all()
    courseuni = Bridge.objects.all()
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

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = "Papan Pemuka Pelajar"
    elif user_type == 'penjaga':
        dashboardNav = "Papan Pemuka Penjaga"
    elif user_type == 'guru':
        dashboardNav = "Papan Pemuka Guru"
    else: #user type in english/invalid e.g. student, parent, teacher, typos
        dashboardNav = "Papan Pemuka Pengguna"

    context = {
        'user_id': user_id,
        'user_type': user_type,
        'username' : username,
        'dashboardNav' : dashboardNav, 
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
    return render(request, 'search/user/searchCourse.html', context)

def searchJobs(request, user_type, user_id):
    
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    username = currentUserRecord.username
    urlTest = 'dashboard:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    urlProfile = 'dashboard:profile-settings-nonadmin'
    urlBookmark = ''
    urlReport = ''
    urlChat = ''
    urlSuggestion = ''
    urlLogout = 'dashboard:logout-confirm'
    
    course = Course.objects.all()
    uni = University.objects.all()
    jobs = Jobs.objects.all()
    courseuni = Bridge.objects.all()
    uni_contains = request.GET.get('uni_contains')
    course_contains = request.GET.get('course_contains')
    jobs_contains = request.GET.get('jobs_contains')
    uniorcourse_contains = request.GET.get('uniorcourse_contains')
    uni_filter = request.GET.get('uni_filter')
    course_filter = request.GET.get('course_filter')
    jobs_filter = request.GET.get('jobs_filter')

    if is_valid_queryparam(jobs_contains):
        jobs = jobs.filter(jobs__icontains=jobs_contains)
    if is_valid_queryparam(course_contains):
        course = course.filter(course__icontains=course_contains)

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = "Papan Pemuka Pelajar"
    elif user_type == 'penjaga':
        dashboardNav = "Papan Pemuka Penjaga"
    elif user_type == 'guru':
        dashboardNav = "Papan Pemuka Guru"
    else: #user type in english/invalid e.g. student, parent, teacher, typos
        dashboardNav = "Papan Pemuka Pengguna"

    context = {
        'user_id': user_id,
        'user_type': user_type,
        'username' : username,
        'dashboardNav' : dashboardNav, 
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
    return render(request, 'search/user/searchJobs.html', context)

#admin
def searchAdmin(request, user_id):
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

        course = Course.objects.all()
        uni = University.objects.all()
        jobs = Jobs.objects.all()
        courseuni = Bridge.objects.all()
        uni_contains = request.GET.get('uni_contains')
        course_contains = request.GET.get('course_contains')
        uniorcourse_contains = request.GET.get('uniorcourse_contains')
        uni_filter = request.GET.get('uni_filter')
        course_filter = request.GET.get('course_filter')
        jobs_filter = request.GET.get('jobs_filter')

        if is_valid_queryparam(uni_contains):
            uni = uni.filter(uni__icontains=uni_contains)
        if is_valid_queryparam(course_contains):
            course = course.filter(course__icontains=course_contains)
        # elif is_valid_queryparam(uniorcourse_contains):
        #     courseuni = courseuni.filter(Q(university__icontains=uniorcourse_contains) | Q(course__icontains=uniorcourse_contains)).distinct()

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

        course = Course.objects.all()
        uni = University.objects.all()
        jobs = Jobs.objects.all()
        courseuni = Bridge.objects.all()
        search_contains_query = request.GET.get('search_contains')
        uni_filter = request.GET.get('uni_filter')
        course_filter = request.GET.get('course_filter')
        jobs_filter = request.GET.get('jobs_filter')

        if search_contains_query != '' and search_contains_query is not None:
            course = course.filter(course__icontains=search_contains_query)

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

        course = Course.objects.all()
        uni = University.objects.all()
        jobs = Jobs.objects.all()
        courseuni = Bridge.objects.all()
        search_contains_query = request.GET.get('search_contains')
        uni_filter = request.GET.get('uni_filter')
        course_filter = request.GET.get('course_filter')
        jobs_filter = request.GET.get('jobs_filter')

        if search_contains_query != '' and search_contains_query is not None:
            course = course.filter(course__icontains=search_contains_query)

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

        course = Course.objects.all()
        uni = University.objects.all()
        jobs = Jobs.objects.all()
        courseuni = Bridge.objects.all()
        search_contains_query = request.GET.get('search_contains')
        uni_filter = request.GET.get('uni_filter')
        course_filter = request.GET.get('course_filter')
        jobs_filter = request.GET.get('jobs_filter')

        if search_contains_query != '' and search_contains_query is not None:
            course = course.filter(course__icontains=search_contains_query)

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
        
        data = Bridge.objects.get(id=pk)
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
        
        data = Bridge.objects.get(id=pk)
        if request.method == "POST":
            data.delete()
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
