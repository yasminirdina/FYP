import dashboard.models
from django.shortcuts import render, redirect
from django.urls import reverse


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

def testMain(request, user_type, user_id):

    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
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
    #if student
    if user_type == 'pelajar' and 'S' in user_id:
        context = {
            'dashboardNav': userid(user_id), 
            'user_id': user_id, 
            'user_type': user_type, 
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
        return render(request, 'pTest\pTstudentMain.html', context)
    #parent and teacher
    else:
        context = {
            'dashboardNav': userid(user_id), 
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
        return render(request, 'pTest\pTestNonStudent.html', context)

def testStart(request, user_type, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
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
    #if student
    if user_type == 'pelajar' and 'S' in user_id:
        context = {
            'dashboardNav': userid(user_id), 
            'user_id': user_id,
            'user_type': user_type,  
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
        return render(request, 'pTest\studentTest.html', context)
    #parent and teacher
    else:
        context = {
            'dashboardNav': userid(user_id), 
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
        return render(request, 'pTest\pTestNonStudent.html', context)

def testAdmin(request, user_type, user_id):
    context = {
        'dashboardNav': user_id,
        'user_type' : user_type, 
        'user_id': user_id, 
    }
    return render(request, 'pTest\pTestAdmin.html', context)
