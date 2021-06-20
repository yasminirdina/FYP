# from django.db.models import Q
from django.shortcuts import render
from .models import University, Bridge, Course, Jobs
import dashboard.models

def is_valid_queryparam(param):
    return param != '' and param is not None

def search(request, user_type, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    username = userRecord.username
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
    dashboardNav = "Carian Maklumat"

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

    # elif is_valid_queryparam(search_contains_query):
    #     uni = uni.filter(uni__icontains=search_contains_query)
    
    # if is_valid_queryparam(search_contains_query):
    #     Jobs = Jobs.filter(jobs__icontains=search_contains_query)

    context = {
        'dashboardNav': dashboardNav,
        # 'response': response, 
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
        'suggestion': urlSuggestion,
        'allCourse':course,
        'allUni':uni,
        'allJobs':jobs,
        'allBridge':courseuni,
    } 
    return render(request, 'search/search.html', context) 
    

def searchAdmin(request, admin_id):
    # urlTest = 'dashboard:index-nonadmin'
    # urlBlog = 'blog:index-nonadmin'
    # urlQuiz = 'quiz:index-student'
    # urlSearch = 'dashboard:index-nonadmin'
    # urlDashboard = 'dashboard:index-nonadmin'
    # urlLogout = 'dashboard:logout-confirm'
    # dashboardNav = 'Papan Pemuka Pelajar'
    # user_type = 'pelajar'
    context = {
         'admin_id':admin_id
    }
    return render(request, 'search/searchAdmin.html', context) 

