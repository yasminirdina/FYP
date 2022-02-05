from datetime import datetime
from tkinter import NONE
from django import http
from django.db.models.expressions import F
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .forms import AddSuggestionForm, ChangePasswordForm, AddClassForm, EditProfileStudentForm, EditProfileParentForm, EditProfileTeacherForm
import dashboard.models, blog.models, quiz.models
import string, re
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.db.models import Sum, Q
from collections import Counter
from operator import itemgetter
import numpy as np

# Create your views here.
def adminNotif(request, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    user_type= "admin"

    urlClassSettings = 'dashboard:class-settings'
    urlSuggestions = 'dashboard:suggestions-admin'
    # urlChat = 'dashboard:chat-admin'
    urlChat = 'dashboard:chat'

    if user_id == 'A1': #betul ni admin, render dashboard index admin
        allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
        unreadNotifCnt = allNotif.filter(isOpen=False).count()

        if request.method == 'POST':
            if request.is_ajax():
                if request.POST['requestType'] == 'updateNotifStatus':
                    # print("hi POST ajax updateNotifStatus") # Test
                    notifID = request.POST['notifID']

                    # print("notifID is number?: " + str(isinstance(notifID, int))) #Test
                    # print("classToDelete: " + notifID) #Test

                    justReadNotif = allNotif.get(id=notifID)
                    justReadNotif.isOpen = True
                    justReadNotif.save()

                    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
                    unreadNotifCnt = allNotif.filter(isOpen=False).count()

                    context = {
                        'doneUpdateNotifStatus': "Yes",
                        'unreadNotifCnt': unreadNotifCnt
                    }
                    
                    return JsonResponse(context)
                # elif request.POST['requestType'] == 'markAllRead':
                #     allUnreadNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id, isOpen=False)

                #     if allUnreadNotif:
                #         for unread in allUnreadNotif:
                #             unread.isOpen = True
                #             unread.save()
                    
                #     allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
                #     unreadNotifCnt = allNotif.filter(isOpen=False).count()
                #     print("unreadNotifCnt: " + str(unreadNotifCnt))

                #     context = {
                #         'user_id': user_id,
                #         'user_type': user_type,
                #         'allNotif': allNotif,
                #         'unreadNotifCnt': unreadNotifCnt
                #     }

                #     return render(request, 'dashboard/adminNotifContent.html', context)
        else:
            context = {
                'user_id': user_id,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard': urlDashboard,
                'logout': urlLogout,
                'user_type': user_type,
                'settings': urlClassSettings,
                'suggestions': urlSuggestions,
                'chat': urlChat,
                'allNotif': allNotif,
                'unreadNotifCnt': unreadNotifCnt
            }
            return render(request, 'dashboard/adminNotif.html', context)
    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        #pass url navbar admin to error template
        context = {
            'response': response,
            'user_type': user_type,
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard': urlDashboard,
            'logout': urlLogout,
            'settings': urlClassSettings,
            'suggestions': urlSuggestions,
            'chat': urlChat
        }
        return render(request, 'dashboard/adminIndexError.html', context)

def adminClassSettings(request, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    user_type= "admin"

    urlClassSettings = 'dashboard:class-settings'
    urlSuggestions = 'dashboard:suggestions-admin'
    # urlChat = 'dashboard:chat-admin'
    urlChat = 'dashboard:chat'

    allClass = dashboard.models.HomeroomTeacherClass.objects.exclude(className='NA').order_by('className')
    
    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    if request.method == 'POST':
        # print("hi POST")
        if request.is_ajax():
            if request.POST['requestType'] == 'deleteClass':
                # print("hi POST ajax deleteClass") # Test
                classToDelete = request.POST['className']

                # print("classToDelete: " + classToDelete) #Test

                allTeacherClassList = list(dashboard.models.Teacher.objects.exclude(homeroomClass='NA').values_list('homeroomClass', flat=True))

                if classToDelete in allTeacherClassList:
                    currentHomeroomTeacher = dashboard.models.Teacher.objects.get(homeroomClass=classToDelete)
                    currentHomeroomTeacher.role = "NA"
                    currentHomeroomTeacher.homeroomClass = "NA"
                    currentHomeroomTeacher.save()

                dashboard.models.ClassList.objects.get(name=classToDelete).delete()
                dashboard.models.HomeroomTeacherClass.objects.get(className=classToDelete).delete()

                context = {
                    'doneDeleteClass': "Yes"
                }
                
                return JsonResponse(context)
        else:
            form = AddClassForm(request.POST)
            if form.is_valid():
                filledList = form.cleaned_data
                newClass = filledList['classname']

                allClassList = list(allClass.values_list('className', flat=True))

                # print("newClassCap: " + newClass.upper()) #Test

                if newClass.upper() not in allClassList:
                    dashboard.models.HomeroomTeacherClass.objects.create(className=newClass.upper(), lastDateEdited=datetime.now().date())
                    dashboard.models.ClassList.objects.create(name=newClass.upper())
                    form = AddClassForm()
        
                    context = {
                        'user_id': user_id,
                        'test': urlTest,
                        'blog': urlBlog,
                        'quiz': urlQuiz,
                        'search': urlSearch,
                        'dashboard':urlDashboard,
                        'logout': urlLogout,
                        'user_type': user_type,
                        'settings': urlClassSettings,
                        'suggestions': urlSuggestions,
                        'chat': urlChat,
                        'allClass': allClass,
                        'form': form,
                        'allNotif': allNotif,
                        'unreadNotifCnt': unreadNotifCnt
                    }
                else:
                    context = {
                        'user_id': user_id,
                        'test': urlTest,
                        'blog': urlBlog,
                        'quiz': urlQuiz,
                        'search': urlSearch,
                        'dashboard':urlDashboard,
                        'logout': urlLogout,
                        'user_type': user_type,
                        'settings': urlClassSettings,
                        'suggestions': urlSuggestions,
                        'chat': urlChat,
                        'allClass': allClass,
                        'form': form,
                        'error': "Nama kelas yang dimasukkan telah wujud. Sila masukkan nama kelas yang lain.",
                        'allNotif': allNotif,
                        'unreadNotifCnt': unreadNotifCnt
                    }
                
                return render(request, 'dashboard/adminClassSettings.html', context)
    else:
        form = AddClassForm()
        
        context = {
            'user_id': user_id,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout,
            'user_type': user_type,
            'settings': urlClassSettings,
            'suggestions': urlSuggestions,
            'chat': urlChat,
            'allClass': allClass,
            'form': form,
            'allNotif': allNotif,
            'unreadNotifCnt': unreadNotifCnt
        }

        return render(request, 'dashboard/adminClassSettings.html', context)

def adminSuggestions(request, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    user_type= "admin"

    urlClassSettings = 'dashboard:class-settings'
    urlSuggestions = 'dashboard:suggestions-admin'
    # urlChat = 'dashboard:chat-admin'
    urlChat = 'dashboard:chat'

    statusList = ['Dihantar', 'Sedang Diproses', 'Ditutup']
    allSuggestions = dashboard.models.Suggestion.objects.all().order_by('-dateIssued', '-timeIssued', 'title')
    allCategory = dashboard.models.SuggestionType.objects.all().order_by('name')

    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    if request.method == 'POST':
        # print("hi POST")
        if request.is_ajax():
            if request.POST['requestType'] == 'updateStatus':
                # print("hi POST ajax updateStatus") # Test
                newStatus = request.POST['newStatus']
                suggestionID = request.POST['suggestionID']

                # print("newStatus: " + newStatus) #Test
                # print("suggestionID: " + str(suggestionID)) #Test

                currentSuggestion = dashboard.models.Suggestion.objects.get(id=suggestionID)
                currentSuggestion.status = newStatus
                currentSuggestion.dateUpdated = datetime.now().date()
                currentSuggestion.timeUpdated = datetime.now().time()
                currentSuggestion.save()

                #create notification (Type id 5 - Status change (for non-admin ONLY))
                dashboard.models.Notification.objects.create(senderID_id='A1', recipientID_id=currentSuggestion.creatorID_id, suggestionID_id=currentSuggestion.id, suggestionStatus=currentSuggestion.status, typeID_id=5)

                context = {
                    'doneUpdateStatus': "Yes"
                }

                return JsonResponse(context)
    else:      
        if request.is_ajax():
            cat_selected = request.GET.get('cat_selected', None)

            if cat_selected != 'Semua':
                for category in allCategory:
                    if category.name == cat_selected:
                        allSuggestions = allSuggestions.filter(typeID_id=category.id)
            
            context = {
                'statusList': statusList,
                'allSuggestions': allSuggestions,
                'allCategory': allCategory
            }

            return render(request, 'dashboard/adminSuggestionsContent.html', context)
        else:
            context = {
                'user_id': user_id,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard': urlDashboard,
                'logout': urlLogout,
                'user_type': user_type,
                'settings': urlClassSettings,
                'suggestions': urlSuggestions,
                'chat': urlChat,
                'statusList': statusList,
                'allSuggestions': allSuggestions,
                'allCategory': allCategory,
                'allNotif': allNotif,
                'unreadNotifCnt': unreadNotifCnt
            }

            return render(request, 'dashboard/adminSuggestions.html', context)

""" def adminChat(request, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    user_type= "admin"

    urlClassSettings = 'dashboard:class-settings'
    urlSuggestions = 'dashboard:suggestions-admin'
    # urlChat = 'dashboard:chat-admin'
    urlChat = 'dashboard:chat'

    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    context = {
        'user_id': user_id,
        'test': urlTest,
        'blog': urlBlog,
        'quiz': urlQuiz,
        'search': urlSearch,
        'dashboard': urlDashboard,
        'logout': urlLogout,
        'user_type': user_type,
        'settings': urlClassSettings,
        'suggestions': urlSuggestions,
        'chat': urlChat,
        'allNotif': allNotif,
        'unreadNotifCnt': unreadNotifCnt
    }

    return render(request, 'dashboard/adminChat.html', context) """

def nonAdminNotif(request, user_type, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    username = userRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'

    urlProfile = 'dashboard:profile-settings'
    urlBookmark = 'dashboard:bookmark'
    urlReport = 'dashboard:report'
    # urlChat = 'dashboard:chat-nonadmin'
    urlChat = 'dashboard:chat'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = " Pelajar"
        allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
        unreadNotifCnt = allNotif.filter(isOpen=False).count()

        if request.method == 'POST':
            if request.is_ajax():
                if request.POST['requestType'] == 'updateNotifStatus':
                    # print("hi POST ajax updateNotifStatus") # Test
                    notifID = request.POST['notifID']

                    # print("notifID is number?: " + str(isinstance(notifID, int))) #Test
                    # print("notifToDelete: " + notifID) #Test

                    justReadNotif = allNotif.get(id=notifID)
                    justReadNotif.isOpen = True
                    justReadNotif.save()

                    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
                    unreadNotifCnt = allNotif.filter(isOpen=False).count()

                    context = {
                        'doneUpdateNotifStatus': "Yes",
                        'unreadNotifCnt': unreadNotifCnt
                    }
                    
                    return JsonResponse(context)
        else:
            context = {
                'dashboardNav': dashboardNav,
                'user_type': user_type,
                'user_id': user_id,
                'username': username,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard':urlDashboard,
                'logout': urlLogout,
                'settings': urlProfile,
                'bookmark': urlBookmark,
                'report': urlReport,
                'chat': urlChat,
                'suggestions': urlSuggestion,
                'allNotif': allNotif,
                'unreadNotifCnt': unreadNotifCnt
            } 
            return render(request, 'dashboard/nonAdminNotif.html', context)
    elif user_type == "penjaga" and 'P' in user_id:
        dashboardNav = " Penjaga"
        allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
        unreadNotifCnt = allNotif.filter(isOpen=False).count()

        if request.method == 'POST':
            if request.is_ajax():
                if request.POST['requestType'] == 'updateNotifStatus':
                    # print("hi POST ajax updateNotifStatus") # Test
                    notifID = request.POST['notifID']

                    # print("notifID is number?: " + str(isinstance(notifID, int))) #Test
                    # print("notifToDelete: " + notifID) #Test

                    justReadNotif = allNotif.get(id=notifID)
                    justReadNotif.isOpen = True
                    justReadNotif.save()

                    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
                    unreadNotifCnt = allNotif.filter(isOpen=False).count()

                    context = {
                        'doneUpdateNotifStatus': "Yes",
                        'unreadNotifCnt': unreadNotifCnt
                    }
                    
                    return JsonResponse(context)
        else:
            context = {
                'dashboardNav': dashboardNav,
                'user_type': user_type,
                'user_id': user_id,
                'username': username,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard':urlDashboard,
                'logout': urlLogout,
                'settings': urlProfile,
                'bookmark': urlBookmark,
                'report': urlReport,
                'chat': urlChat,
                'suggestions': urlSuggestion,
                'allNotif': allNotif,
                'unreadNotifCnt': unreadNotifCnt
            } 
            return render(request, 'dashboard/nonAdminNotif.html', context)
    elif user_type == "guru" and 'T' in user_id:
        dashboardNav = " Guru"
        allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
        unreadNotifCnt = allNotif.filter(isOpen=False).count()

        if request.method == 'POST':
            if request.is_ajax():
                if request.POST['requestType'] == 'updateNotifStatus':
                    # print("hi POST ajax updateNotifStatus") # Test
                    notifID = request.POST['notifID']

                    # print("notifID is number?: " + str(isinstance(notifID, int))) #Test
                    # print("notifToDelete: " + notifID) #Test

                    justReadNotif = allNotif.get(id=notifID)
                    justReadNotif.isOpen = True
                    justReadNotif.save()

                    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
                    unreadNotifCnt = allNotif.filter(isOpen=False).count()

                    context = {
                        'doneUpdateNotifStatus': "Yes",
                        'unreadNotifCnt': unreadNotifCnt
                    }
                    
                    return JsonResponse(context)
        else:
            context = {
                'dashboardNav': dashboardNav,
                'user_type': user_type,
                'user_id': user_id,
                'username': username,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard':urlDashboard,
                'logout': urlLogout,
                'settings': urlProfile,
                'bookmark': urlBookmark,
                'report': urlReport,
                'chat': urlChat,
                'suggestions': urlSuggestion,
                'allNotif': allNotif,
                'unreadNotifCnt': unreadNotifCnt
            } 
            return render(request, 'dashboard/nonAdminNotif.html', context)
    else: #no match between user type and user ID huruf part (cth: 'pelajar' and 'A1') OR english user types OR typo
        if user_type == 'pelajar':
            dashboardNav = " Pelajar"
            response = "Halaman ini hanya boleh diakses oleh pelajar."
        elif user_type == 'penjaga':
            dashboardNav = " Penjaga"
            response = "Halaman ini hanya boleh diakses oleh ibu bapa atau penjaga."
        elif user_type == 'guru':
            dashboardNav = " Guru"
            response = "Halaman ini hanya boleh diakses oleh guru."
        else: #user type in english/invalid e.g. student, parent, teacher, typos
            dashboardNav = " Pengguna"
            response = "Halaman ini tidak wujud." 

        #pass url navbar nonadmin to error template
        context = {
            'response': response,
            'dashboardNav': dashboardNav,
            'user_type': user_type,
            'user_id': user_id,
            'username': username,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout,
            'settings': urlProfile,
            'bookmark': urlBookmark,
            'report': urlReport,
            'chat': urlChat,
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminIndexError.html', context)

def showProfileNonAdmin(request, user_type, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    username = userRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'

    urlProfile = 'dashboard:profile-settings'
    urlBookmark = 'dashboard:bookmark'
    urlReport = 'dashboard:report'
    # urlChat = 'dashboard:chat-nonadmin'
    urlChat = 'dashboard:chat'
    urlSuggestion = 'dashboard:suggestions-nonadmin'
    
    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    if user_type == 'pelajar' and 'S' in user_id:
        title = " Tetapan Akaun Pelajar"
        dashboardNav = " Pelajar"
        studentDetail = dashboard.models.Student.objects.get(ID=user_id)
        subtitle = "Biodata Pelajar"

        context = {
            'title': title,
            'dashboardNav': dashboardNav,
            'userDetail': studentDetail,
            'subtitle': subtitle,
            'user_type': user_type,
            'user_id': user_id,
            'username': username,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout,
            'settings': urlProfile,
            'bookmark': urlBookmark,
            'report': urlReport,
            'chat': urlChat,
            'suggestions': urlSuggestion,
            'allNotif': allNotif,
            'unreadNotifCnt': unreadNotifCnt
        }

        return render(request, 'dashboard\showProfile.html', context)
    elif user_type == 'penjaga' and 'P' in user_id:
        title = " Tetapan Akaun Penjaga"
        dashboardNav = " Penjaga"
        parentDetail = dashboard.models.Parent.objects.get(ID=user_id)
        studentDetailQuery = dashboard.models.Student.objects.filter(parentID=parentDetail).order_by('name')
        subtitle = "Biodata Penjaga"

        context = {
            'title': title,
            'dashboardNav': dashboardNav,
            'userDetail': parentDetail,
            'studentDetail': studentDetailQuery,
            'studentDetailCount': studentDetailQuery.count(),
            'subtitle': subtitle,
            'user_type': user_type,
            'user_id': user_id,
            'username': username,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout,
            'settings': urlProfile,
            'bookmark': urlBookmark,
            'report': urlReport,
            'chat': urlChat,
            'suggestions': urlSuggestion,
            'allNotif': allNotif,
            'unreadNotifCnt': unreadNotifCnt
        }

        return render(request, 'dashboard\showProfile.html', context)
    elif user_type == 'guru' and 'T' in user_id:
        title = " Tetapan Akaun Guru"
        dashboardNav = " Guru"
        subtitle = "Biodata Guru"
        teacherDetail = dashboard.models.Teacher.objects.get(ID=user_id)

        if teacherDetail.role == "Guru Kelas":
            if teacherDetail.homeroomClass != 'NA':
                homeroomDetail = dashboard.models.HomeroomTeacherClass.objects.get(teacherID=teacherDetail)
                studentDetailQuery = dashboard.models.Student.objects.filter(studentClass=homeroomDetail.className)

                context = {
                    'title': title,
                    'dashboardNav': dashboardNav,
                    'userDetail': teacherDetail,
                    'studentDetail': studentDetailQuery,
                    'studentDetailCount': studentDetailQuery.count(),
                    'subtitle': subtitle,
                    'user_type': user_type,
                    'user_id': user_id,
                    'username': username,
                    'test': urlTest,
                    'blog': urlBlog,
                    'quiz': urlQuiz,
                    'search': urlSearch,
                    'dashboard':urlDashboard,
                    'logout': urlLogout,
                    'settings': urlProfile,
                    'bookmark': urlBookmark,
                    'report': urlReport,
                    'chat': urlChat,
                    'suggestions': urlSuggestion,
                    'allNotif': allNotif,
                    'unreadNotifCnt': unreadNotifCnt
                }
            else:
                context = {
                    'title': title,
                    'dashboardNav': dashboardNav,
                    'userDetail': teacherDetail,
                    'subtitle': subtitle,
                    'user_type': user_type,
                    'user_id': user_id,
                    'username': username,
                    'test': urlTest,
                    'blog': urlBlog,
                    'quiz': urlQuiz,
                    'search': urlSearch,
                    'dashboard':urlDashboard,
                    'logout': urlLogout,
                    'settings': urlProfile,
                    'bookmark': urlBookmark,
                    'report': urlReport,
                    'chat': urlChat,
                    'suggestions': urlSuggestion,
                    'allNotif': allNotif,
                    'unreadNotifCnt': unreadNotifCnt
                }
        else:
            context = {
                'title': title,
                'dashboardNav': dashboardNav,
                'userDetail': teacherDetail,
                'subtitle': subtitle,
                'user_type': user_type,
                'user_id': user_id,
                'username': username,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard':urlDashboard,
                'logout': urlLogout,
                'settings': urlProfile,
                'bookmark': urlBookmark,
                'report': urlReport,
                'chat': urlChat,
                'suggestions': urlSuggestion,
                'allNotif': allNotif,
                'unreadNotifCnt': unreadNotifCnt
            }

        return render(request, 'dashboard\showProfile.html', context)

#showProfile.changePassword
def changePassword(request, user_type, user_id):
    #for any user type
    #if filled current pass sama dgn the one in their user type table record
        #baru proceed reset password
        #save in database
        #back to show profile for that usertype and userid
    #else (current pass tak match)
        #error current pass not match
        #load empty form balik
    
    filledList = {}
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    username = currentUserDetail.username
    #urls for navbar
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    subtitle = "Tukar Kata Laluan" #h2 tag

    urlProfile = 'dashboard:profile-settings'
    urlBookmark = 'dashboard:bookmark'
    urlReport = 'dashboard:report'
    # urlChat = 'dashboard:chat-nonadmin'
    urlChat = 'dashboard:chat'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    if user_type == 'pelajar' and 'S' in user_id:
        currentUserTypeDetail = dashboard.models.Student.objects.get(ID=user_id)
        title = " Tetapan Akaun Pelajar"
        dashboardNav = " Pelajar"
    elif user_type == 'penjaga' and 'P' in user_id:
        currentUserTypeDetail = dashboard.models.Parent.objects.get(ID=user_id)
        title = " Tetapan Akaun Penjaga"
        dashboardNav = " Penjaga"
    elif user_type == 'guru' and 'T' in user_id:
        currentUserTypeDetail = dashboard.models.Teacher.objects.get(ID=user_id)
        title = " Tetapan Akaun Guru"
        dashboardNav = " Guru"

    def errorMessageDisplay(request, form, errorMessage):
        #redirect to refreshed form with error message on top
        context = {
            'title': title,
            'dashboardNav': dashboardNav,
            'username': username,
            'user_id': user_id,
            'user_type': user_type, 
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard': urlDashboard,
            'logout': urlLogout,
            'settings': urlProfile,
            'bookmark': urlBookmark,
            'report': urlReport,
            'chat': urlChat,
            'suggestions': urlSuggestion,
            'subtitle': subtitle,
            'errorMessage': errorMessage,
            'form': form,
            'allNotif': allNotif,
            'unreadNotifCnt': unreadNotifCnt
        }
        return render(request, 'dashboard/changePassword.html', context)

    def checkChar(firstPass):
        cntUpper = 0
        cntLower = 0
        cntSpecial = 0
        cntNumber = 0
        for char in firstPass:
            if char in string.punctuation:
                cntSpecial += 1
            elif char.isupper():
                cntUpper += 1
            elif char.islower():
                cntLower += 1
            elif char.isnumeric():
                cntNumber +=1

        if cntUpper > 0  and cntLower and cntSpecial > 0 and cntNumber > 0:
            return True
        else:
            return False

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            filledList = form.cleaned_data
            #if filled current password is the same as that user's record in Student/Parent/Teacher table
            # print("filledpassraw: " + filledList['currentPass']) #Test
            # print("filledpasshash: " + make_password(filledList['currentPass'])) #Test
            # print("currentpassraw: " + currentUserTypeDetail.password) #Test
            # print("currentpasshash: " + make_password(currentUserTypeDetail.password)) #Test
            if check_password(filledList['currentPass'], currentUserTypeDetail.password) == True:
                #if first and second entered password is the same
                if filledList['newPass'] == filledList['newPassConfirm']:
                    #if entered password length is 10
                    if len(filledList['newPass']) == 10:
                        #if has at least 1 upper, lower, special and number characters
                        if checkChar(filledList['newPass']) == True:
                            #update password in that usertype's table record for the entered email
                            currentUserTypeDetail.password = make_password(filledList['newPassConfirm'])
                            currentUserTypeDetail.save()   
                            
                            #render successUpdate.html - with context for navbar, title, subtitle,
                            #successmsg, variable for views url in template
                            successMessage = "Kata laluan berjaya dikemaskini!"
                            
                            context = {
                                'title': title,
                                'dashboardNav': dashboardNav,
                                'username': username,
                                'user_id': user_id,
                                'user_type': user_type,
                                'test': urlTest,
                                'blog': urlBlog,
                                'quiz': urlQuiz,
                                'search': urlSearch,
                                'dashboard': urlDashboard,
                                'logout': urlLogout,
                                'settings': urlProfile,
                                'bookmark': urlBookmark,
                                'report': urlReport,
                                'chat': urlChat,
                                'suggestions': urlSuggestion,
                                'subtitle': subtitle,
                                'successMessage': successMessage,
                                'allNotif': allNotif,
                                'unreadNotifCnt': unreadNotifCnt
                            }
                            return render(request, 'dashboard/successUpdate.html', context)
                        #if either has no upper/lower/special/number characters
                        else:
                            errorMessage = "Kata laluan baharu anda mestilah mengandungi huruf besar, huruf kecil, angka dan aksara khas."
                            return errorMessageDisplay(request, form, errorMessage)
                    #if entered password length is not 10
                    else: 
                        errorMessage = "Kata laluan baharu anda terlalu pendek."
                        return errorMessageDisplay(request, form, errorMessage)
                #if first and second entered password do not match
                else:          
                    #display error passwords do not match
                    errorMessage = "Sila pastikan kedua-dua kata laluan baharu adalah sama."
                    return errorMessageDisplay(request, form, errorMessage)
            #if filled current password does not match the user's record in her/his usertype's table
            else:
                #display error current password not match
                errorMessage = "Kata laluan semasa tidak tepat."
                form = ChangePasswordForm()
                return errorMessageDisplay(request, form, errorMessage)
    else: 
        form = ChangePasswordForm()

    context = {
        'title': title,
        'dashboardNav': dashboardNav, 
        'username': username,
        'user_id': user_id,
        'user_type': user_type,
        'test': urlTest,
        'blog': urlBlog,
        'quiz': urlQuiz,
        'search': urlSearch,
        'dashboard':urlDashboard,
        'logout': urlLogout,
        'settings': urlProfile,
        'bookmark': urlBookmark,
        'report': urlReport,
        'chat': urlChat,
        'suggestions': urlSuggestion,
        'subtitle': subtitle,
        'form': form,
        'allNotif': allNotif,
        'unreadNotifCnt': unreadNotifCnt
    }
    return render(request, 'dashboard/changePassword.html', context)

#showProfile.editProfile
def editProfile(request, user_type, user_id):
    filledList = {}
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    username = currentUserDetail.username
    #urls for navbar
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    subtitle = "Kemaskini Profil" #h2 tag

    urlProfile = 'dashboard:profile-settings'
    urlBookmark = 'dashboard:bookmark'
    urlReport = 'dashboard:report'
    # urlChat = 'dashboard:chat-nonadmin'
    urlChat = 'dashboard:chat'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    if request.method == 'POST':
        #if student
        if user_type == 'pelajar' and 'S' in user_id:
            title = " Tetapan Akaun Pelajar"
            dashboardNav = " Pelajar"
            currentUserTypeDetail = dashboard.models.Student.objects.get(ID=user_id)  
            ParentOfStudentRecord = dashboard.models.Parent.objects.get(ID=currentUserTypeDetail.parentID.ID)
            name = currentUserTypeDetail.name
            year = currentUserTypeDetail.year
            studentClass = currentUserTypeDetail.studentClass
            interest = currentUserTypeDetail.interest
            parentID = ParentOfStudentRecord
            form = EditProfileStudentForm(request.POST, initial={'name': name, 'year': year, 'studentClass': studentClass,
            'interest': interest, 'parentID': parentID})
            if form.is_valid():
                filledList = form.cleaned_data
                #if filled name tak sama from current DB record (= dia tukar)
                if filledList['name'] != currentUserTypeDetail.name:
                    currentUserTypeDetail.name = filledList['name']
                    currentUserTypeDetail.save()
                #if dia tukar year
                if filledList['year'] != currentUserTypeDetail.year:
                    currentUserTypeDetail.year = filledList['year']
                    currentUserTypeDetail.save()                
                #if dia tukar kelas
                if filledList['studentClass'] != currentUserTypeDetail.studentClass.className:
                    currentUserTypeDetail.studentClass = filledList['studentClass']
                    currentUserTypeDetail.save()
                #if dia tukar interest
                if filledList['interest'] != currentUserTypeDetail.interest:
                    currentUserTypeDetail.interest = filledList['interest']
                    currentUserTypeDetail.save()
                #if dia tukar parent name
                if filledList['parentID'] != currentUserTypeDetail.parentID:
                    currentUserTypeDetail.parentID = filledList['parentID']
                    currentUserTypeDetail.save()

                #render successUpdate.html - with context for navbar, title, subtitle,
                #successmsg, variable for views url in template
                successMessage = "Profil berjaya dikemaskini!"
                context = {
                    'title': title,
                    'dashboardNav': dashboardNav,
                    'username': username,
                    'user_id': user_id,
                    'user_type': user_type,
                    'test': urlTest,
                    'blog': urlBlog,
                    'quiz': urlQuiz,
                    'search': urlSearch,
                    'dashboard':urlDashboard,
                    'logout': urlLogout,
                    'settings': urlProfile,
                    'bookmark': urlBookmark,
                    'report': urlReport,
                    'chat': urlChat,
                    'suggestions': urlSuggestion,
                    'subtitle': subtitle,
                    'successMessage': successMessage,
                    'allNotif': allNotif,
                    'unreadNotifCnt': unreadNotifCnt
                }
                return render(request, 'dashboard/successUpdate.html', context)
        #if parent
        elif user_type == 'penjaga' and 'P' in user_id:
            title = " Tetapan Akaun Penjaga"
            dashboardNav = " Penjaga"
            currentUserTypeDetail = dashboard.models.Parent.objects.get(ID=user_id)
            name = currentUserTypeDetail.name
            salutation = currentUserTypeDetail.salutation
            age = currentUserTypeDetail.age
            job = currentUserTypeDetail.job
            relation = currentUserTypeDetail.relation
            form = EditProfileParentForm(request.POST, initial={'name': name, 'salutation': salutation, 'age': age,
            'job': job, 'relation': relation})
            if form.is_valid():
                filledList = form.cleaned_data
                #if filled name tak sama from current DB record (= dia tukar)
                if filledList['name'] != currentUserTypeDetail.name:
                    currentUserTypeDetail.name = filledList['name']
                    currentUserTypeDetail.save()
                #if dia tukar salutation
                if filledList['salutation'] != currentUserTypeDetail.salutation:
                    currentUserTypeDetail.salutation = filledList['salutation']
                    currentUserTypeDetail.save()
                #if dia tukar age
                if filledList['age'] != currentUserTypeDetail.age:
                    currentUserTypeDetail.age = filledList['age']
                    currentUserTypeDetail.save()
                #if dia tukar job
                if filledList['job'] != currentUserTypeDetail.job:
                    currentUserTypeDetail.job = filledList['job']
                    currentUserTypeDetail.save()
                #if dia tukar relation
                if filledList['relation'] != currentUserTypeDetail.relation:
                    currentUserTypeDetail.relation = filledList['relation']
                    currentUserTypeDetail.save()

                #render successUpdate.html - with context for navbar, title, subtitle,
                #successmsg, variable for views url in template
                successMessage = "Profil berjaya dikemaskini!"
                context = {
                    'title': title,
                    'dashboardNav': dashboardNav,
                    'username': username,
                    'user_id': user_id,
                    'user_type': user_type,
                    'test': urlTest,
                    'blog': urlBlog,
                    'quiz': urlQuiz,
                    'search': urlSearch,
                    'dashboard':urlDashboard,
                    'logout': urlLogout,
                    'settings': urlProfile,
                    'bookmark': urlBookmark,
                    'report': urlReport,
                    'chat': urlChat,
                    'suggestions': urlSuggestion,
                    'subtitle': subtitle,
                    'successMessage': successMessage,
                    'allNotif': allNotif,
                    'unreadNotifCnt': unreadNotifCnt
                }
                return render(request, 'dashboard/successUpdate.html', context)
        #if teacher
        elif user_type == 'guru' and 'T' in user_id:
            title = " Tetapan Akaun Guru"
            dashboardNav = " Guru"
            currentUserTypeDetail = dashboard.models.Teacher.objects.get(ID=user_id)
            name = currentUserTypeDetail.name
            salutation = currentUserTypeDetail.salutation
            role = currentUserTypeDetail.role
            year = currentUserTypeDetail.year
            homeroomClass = currentUserTypeDetail.homeroomClass
            form = EditProfileTeacherForm(request.POST, initial={'name': name, 'salutation': salutation, 'role': role, 'year': year, 'homeroomClass': homeroomClass})
            if form.is_valid():
                filledList = form.cleaned_data
                #if filled name tak sama from current DB record (= dia tukar)
                if filledList['name'] != currentUserTypeDetail.name:
                    currentUserTypeDetail.name = filledList['name']
                    currentUserTypeDetail.save()
                #if dia tukar salutation
                if filledList['salutation'] != currentUserTypeDetail.salutation:
                    currentUserTypeDetail.salutation = filledList['salutation']
                    currentUserTypeDetail.save()
                
                #save prev role to a variable
                prevUserRole = currentUserTypeDetail.role
                #if dia tukar role
                if filledList['role'] != currentUserTypeDetail.role:
                    currentUserTypeDetail.role = filledList['role']
                    currentUserTypeDetail.save()
                    #---PASS---
                    #if prev role = guru kelas --> new role = bukan guru kelas
                    if prevUserRole == 'Guru Kelas' and currentUserTypeDetail.role != 'Guru Kelas':
                        #change current user id dlm teacherID in HTC to "NA" (drop assignation teacher tu as guru kelas to class x) + SAVE
                        #change homeroomClass in Teacher table for this user_id to "NA" + SAVE
                        #return successpage
                        HTCTeacherIDlist = list(dashboard.models.HomeroomTeacherClass.objects.values_list('teacherID', flat=True))
                        #if current teacherID takde dlm HTC teacherID skip if ni (sbb when tukar role GK --> non GK, previously mmg tkde homeroomClass so
                        #tkde jugak teacherID dia dlm HTC)
                        if user_id in HTCTeacherIDlist:
                            currentHTCforUserDetail = dashboard.models.HomeroomTeacherClass.objects.get(teacherID=currentUserTypeDetail)
                            NATeacherUserDetail = dashboard.models.User.objects.get(ID='NA')
                            NATeacherDetail = dashboard.models.Teacher.objects.get(ID=NATeacherUserDetail)
                            currentHTCforUserDetail.teacherID = NATeacherDetail
                            currentHTCforUserDetail.lastDateEdited = datetime.now().date()
                            currentHTCforUserDetail.save()
                        currentUserTypeDetail.homeroomClass = 'NA'
                        currentUserTypeDetail.year = filledList['year'] #tak kisah tukar year tak sebab nak keluar dah lepas if ni
                        currentUserTypeDetail.save()
                        
                        successMessage = "Profil berjaya dikemaskini!"
                        context = {
                            'title': title,
                            'dashboardNav': dashboardNav,
                            'username': username,
                            'user_id': user_id,
                            'user_type': user_type,
                            'test': urlTest,
                            'blog': urlBlog,
                            'quiz': urlQuiz,
                            'search': urlSearch,
                            'dashboard':urlDashboard,
                            'logout': urlLogout,
                            'settings': urlProfile,
                            'bookmark': urlBookmark,
                            'report': urlReport,
                            'chat': urlChat,
                            'suggestions': urlSuggestion,
                            'subtitle': subtitle,
                            'successMessage': successMessage,
                            'allNotif': allNotif,
                            'unreadNotifCnt': unreadNotifCnt
                        }
                        return render(request, 'dashboard/successUpdate.html', context)
                #if new/unchanged role = Guru Kelas #MEMANG GURU KELAS or NEW GURU KELAS
                if currentUserTypeDetail.role == 'Guru Kelas':
                    #if filled class dah tukar (dont save yet)
                    if currentUserTypeDetail.homeroomClass != filledList['homeroomClass']:
                        #get currentHTC for the new class
                        currentHTCforClassDetail = dashboard.models.HomeroomTeacherClass.objects.get(className=filledList['homeroomClass'])
                        NATeacherUserDetail = dashboard.models.User.objects.get(ID='NA')
                        NATeacherDetail = dashboard.models.Teacher.objects.get(ID=NATeacherUserDetail)
                        #---PASS---(mmg GK)
                        #if changed filled class ada existing guru kelas (bukan "NA") in HTC table
                        if currentHTCforClassDetail.teacherID != NATeacherDetail:
                            #save prev teacherID and record from Teacher table to a var
                            prevHTCTeacherID = currentHTCforClassDetail.teacherID.ID.ID
                            prevTeacherUserDetail = dashboard.models.User.objects.get(ID=prevHTCTeacherID)
                            prevTeacherDetail = dashboard.models.Teacher.objects.get(ID=prevTeacherUserDetail)
                            #---PASS---(mmg GK & new GK)
                            #if year dlm HTC for that class lain from filled year
                            if currentHTCforClassDetail.year != filledList['year']:
                                #change year in HTC to filled year
                                #change year of prev guru kelas in Teacher table to filled year
                                currentHTCforClassDetail.year = filledList['year']
                                prevTeacherDetail.year = filledList['year']
                            HTCTeacherIDlist = list(dashboard.models.HomeroomTeacherClass.objects.values_list('teacherID', flat=True))
                            ##---PASS---(mmg GK - new GK tak perlu sbb mmg tkde record in HTC) if current teacherID already exist in HTC for other class, tukar teacherID HTC tu to 'NA' & year dia to filled year
                            ##---PASS---(mmg GK & new GK) if not, skip this if
                            if user_id in HTCTeacherIDlist:
                                currentHTCforUserDetail = dashboard.models.HomeroomTeacherClass.objects.get(teacherID=currentUserTypeDetail)
                                currentHTCforUserDetail.teacherID = NATeacherDetail
                                currentHTCforUserDetail.year = filledList['year']
                                currentHTCforUserDetail.lastDateEdited = datetime.now().date()
                                currentHTCforUserDetail.save()
                            #change teacherID in HTC to current user_id and SAVE (apply for both changed year or not)
                            #change role prev guru kelas (in Teacher table) to "NA"
                            #change homeroomClass of prev guru kelas to "NA" and SAVE record prev teacher
                            currentHTCforClassDetail.teacherID = currentUserTypeDetail
                            currentHTCforClassDetail.lastDateEdited = datetime.now().date()
                            currentHTCforClassDetail.save()
                            prevTeacherDetail.role = 'NA'
                            NAHTCDetail = dashboard.models.HomeroomTeacherClass.objects.get(className='NA')
                            prevTeacherDetail.homeroomClass = NAHTCDetail.className
                            prevTeacherDetail.save()
                        #---PASS ALL--- (mmg GK & new GK)    
                        #if change filled class takda existing guru kelas (is "NA") in HTC table
                        elif currentHTCforClassDetail.teacherID == NATeacherDetail:
                            #---PASS--- (mmg GK & new GK)
                            #if year dlm HTC for that class lain from filled year
                            if currentHTCforClassDetail.year != filledList['year']:
                                #change year in HTC to filled year
                                currentHTCforClassDetail.year = filledList['year']
                            HTCTeacherIDlist = list(dashboard.models.HomeroomTeacherClass.objects.values_list('teacherID', flat=True))
                            #---PASS--- (mmg GK - new GK tak perlu sbb mmg tkde prev record dlm HTC) if current teacherID already exist
                            #in other class dlm HTC, tukar teacherID HTC tu to 'NA' & year dia to filled year
                            #---PASS--- (mmg GK & new GK) if not, skip if
                            if user_id in HTCTeacherIDlist:
                                currentHTCforUserDetail = dashboard.models.HomeroomTeacherClass.objects.get(teacherID=currentUserTypeDetail)
                                currentHTCforUserDetail.teacherID = NATeacherDetail
                                currentHTCforUserDetail.year = filledList['year']
                                currentHTCforUserDetail.lastDateEdited = datetime.now().date()
                                currentHTCforUserDetail.save()
                                #response = str(NATeacherDetail) + ",,, " + str(currentHTCforUserDetail)
                                #return HttpResponse(response)
                            #change teacherID in HTC from "NA" to current user_id and SAVE (apply for changed year or not)
                            #currentTeacherUserDetail = dashboard.models.User.objects.get(ID=user_id)
                            #currentTeacherDetail = dashboard.models.Teacher.objects.get(ID=currentTeacherUserDetail)
                            currentHTCforClassDetail.teacherID = currentUserTypeDetail
                            currentHTCforClassDetail.lastDateEdited = datetime.now().date()
                            currentHTCforClassDetail.save()
                        #change current teacher.class and year in Teacher table to filled
                        #SAVE record current user_id in Teacher table
                        #currentTeacherUserDetail = dashboard.models.User.objects.get(ID=user_id)
                        #currentTeacherDetail = dashboard.models.Teacher.objects.get(ID=currentTeacherUserDetail)
                        currentUserTypeDetail.homeroomClass = filledList['homeroomClass']
                        currentUserTypeDetail.year = filledList['year']
                        currentUserTypeDetail.save()
                    #if tak tukar kelas (applicable for both memang guru kelas and new (sebab new GK might forgot))
                    elif currentUserTypeDetail.homeroomClass == filledList['homeroomClass']:
                        #---PASS--- until successpage
                        #if tukar tahun & memang GK
                        if (currentUserTypeDetail.year != filledList['year']) and (prevUserRole == currentUserTypeDetail.role):
                            #change year in Teacher gak + SAVE
                            HTCTeacherIDlist = list(dashboard.models.HomeroomTeacherClass.objects.values_list('teacherID', flat=True))
                            #if current teacher ni dah ada record id dalam HTC (sebab dia dah set class), tukar year dlm HTC sekali + SAVE,
                            #kalau tak skip if ni
                            if user_id in HTCTeacherIDlist:
                                currentHTCforUserDetail = dashboard.models.HomeroomTeacherClass.objects.get(teacherID=currentUserTypeDetail)
                                currentHTCforUserDetail.year = filledList['year']
                                currentHTCforUserDetail.lastDateEdited = datetime.now().date()
                                currentHTCforUserDetail.save()
                            currentUserTypeDetail.year = filledList['year']
                            currentUserTypeDetail.save()
                        #---PASS--- until successpage    
                        #if tukar tahun & new GK
                        elif (currentUserTypeDetail.year != filledList['year']) and (prevUserRole != 'Guru Kelas') and (currentUserTypeDetail.role == 'Guru Kelas'):
                            #change year in Teacher gak + SAVE
                            currentUserTypeDetail.year = filledList['year']
                            currentUserTypeDetail.save()
                    #---PASS--- for tukar role to GK ONLY, not class and year

                    #render successUpdate.html - with context for navbar, title, subtitle,
                    #successmsg, variable for views url in template
                    successMessage = "Profil berjaya dikemaskini!"
                    context = {
                        'title': title,
                        'dashboardNav': dashboardNav,
                        'username': username,
                        'user_id': user_id,
                        'user_type': user_type,
                        'test': urlTest,
                        'blog': urlBlog,
                        'quiz': urlQuiz,
                        'search': urlSearch,
                        'dashboard':urlDashboard,
                        'logout': urlLogout,
                        'settings': urlProfile,
                        'bookmark': urlBookmark,
                        'report': urlReport,
                        'chat': urlChat,
                        'suggestions': urlSuggestion,
                        'subtitle': subtitle,
                        'successMessage': successMessage,
                        'allNotif': allNotif,
                        'unreadNotifCnt': unreadNotifCnt
                    }
                    return render(request, 'dashboard/successUpdate.html', context)

                #---PASS---
                #if tukar year & yang memang bukan guru kelas - sebab yg GK --> non GK dah save kt atas
                if (currentUserTypeDetail.year != filledList['year']) and (currentUserTypeDetail.role != 'Guru Kelas'):
                    #save mcm biasa in Teacher
                    currentUserTypeDetail.year = filledList['year']
                    currentUserTypeDetail.save()
                
                #---PASS---
                #if tukar class & yang role memang bukan GK (tersilap) - sebab yg GK --> non GK dah save kt atas
                if (currentUserTypeDetail.homeroomClass != filledList['homeroomClass']) and (currentUserTypeDetail.role != 'Guru Kelas'):
                    #errormessage Kelas hanya boleh ditukar oleh Guru Kelas sahaja.
                    #refresh current form     
                    name = currentUserTypeDetail.name
                    salutation = currentUserTypeDetail.salutation
                    role = currentUserTypeDetail.role
                    year = currentUserTypeDetail.year
                    homeroomClass = currentUserTypeDetail.homeroomClass
                    form = EditProfileTeacherForm(initial={'name': name, 'salutation': salutation, 'role': role,
                    'year': year, 'homeroomClass': homeroomClass})
                    errorMessage = "Kelas hanya boleh ditukar oleh Guru Kelas sahaja."

                    context = {
                        'title': title,
                        'dashboardNav': dashboardNav,
                        'username': username,
                        'user_id': user_id,
                        'user_type': user_type,
                        'test': urlTest,
                        'blog': urlBlog,
                        'quiz': urlQuiz,
                        'search': urlSearch,
                        'dashboard': urlDashboard,
                        'logout': urlLogout,
                        'settings': urlProfile,
                        'bookmark': urlBookmark,
                        'report': urlReport,
                        'chat': urlChat,
                        'suggestions': urlSuggestion,
                        'subtitle': subtitle,
                        'errorMessage': errorMessage,
                        'form': form,
                        'allNotif': allNotif,
                        'unreadNotifCnt': unreadNotifCnt
                    }

                    return render(request, 'dashboard/editProfile.html', context)

                #render successUpdate.html - with context for navbar, title, subtitle,
                #successmsg, variable for views url in template
                successMessage = "Profil berjaya dikemaskini!"
                
                context = {
                    'title': title,
                    'dashboardNav': dashboardNav,
                    'username': username,
                    'user_id': user_id,
                    'user_type': user_type,
                    'test': urlTest,
                    'blog': urlBlog,
                    'quiz': urlQuiz,
                    'search': urlSearch,
                    'dashboard':urlDashboard,
                    'logout': urlLogout,
                    'settings': urlProfile,
                    'bookmark': urlBookmark,
                    'report': urlReport,
                    'chat': urlChat,
                    'suggestions': urlSuggestion,
                    'subtitle': subtitle,
                    'successMessage': successMessage,
                    'allNotif': allNotif,
                    'unreadNotifCnt': unreadNotifCnt
                }
                return render(request, 'dashboard/successUpdate.html', context)
    else:
        if user_type == 'pelajar' and 'S' in user_id:
            title = " Tetapan Akaun Pelajar"
            dashboardNav = " Pelajar"
            currentUserTypeDetail = dashboard.models.Student.objects.get(ID=user_id)   
            ParentOfStudentRecord = dashboard.models.Parent.objects.get(ID=currentUserTypeDetail.parentID.ID)
            parentID = ParentOfStudentRecord
            name = currentUserTypeDetail.name
            year = currentUserTypeDetail.year
            studentClass = currentUserTypeDetail.studentClass.className
            interest = currentUserTypeDetail.interest
            form = EditProfileStudentForm(initial={'name': name, 'year': year, 'studentClass': studentClass,
            'interest': interest, 'parentID': parentID})
        elif user_type == 'penjaga' and 'P' in user_id:
            title = " Tetapan Akaun Penjaga"
            dashboardNav = " Penjaga"
            currentUserTypeDetail = dashboard.models.Parent.objects.get(ID=user_id)
            name = currentUserTypeDetail.name
            salutation = currentUserTypeDetail.salutation
            age = currentUserTypeDetail.age
            job = currentUserTypeDetail.job
            relation = currentUserTypeDetail.relation
            form = EditProfileParentForm(initial={'name': name, 'salutation': salutation, 'age': age,
            'job': job, 'relation': relation})
        elif user_type == 'guru' and 'T' in user_id:
            title = " Tetapan Akaun Guru"
            dashboardNav = " Guru"
            currentUserTypeDetail = dashboard.models.Teacher.objects.get(ID=user_id)
            name = currentUserTypeDetail.name
            salutation = currentUserTypeDetail.salutation
            role = currentUserTypeDetail.role
            year = currentUserTypeDetail.year
            homeroomClass = currentUserTypeDetail.homeroomClass
            form = EditProfileTeacherForm(initial={'name': name, 'salutation': salutation, 'role': role,
            'year': year, 'homeroomClass': homeroomClass})

    context = {
        'title': title,
        'dashboardNav': dashboardNav,
        'username': username,
        'user_id': user_id,
        'user_type': user_type,
        'test': urlTest,
        'blog': urlBlog,
        'quiz': urlQuiz,
        'search': urlSearch,
        'dashboard': urlDashboard,
        'logout': urlLogout,
        'settings': urlProfile,
        'bookmark': urlBookmark,
        'report': urlReport,
        'chat': urlChat,
        'suggestions': urlSuggestion,
        'subtitle': subtitle,
        'form': form,
        'allNotif': allNotif,
        'unreadNotifCnt': unreadNotifCnt
    }

    return render(request, 'dashboard/editProfile.html', context)

def nonAdminBookmark(request, user_type, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    username = userRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'

    urlProfile = 'dashboard:profile-settings'
    urlBookmark = 'dashboard:bookmark'
    urlReport = 'dashboard:report'
    # urlChat = 'dashboard:chat-nonadmin'
    urlChat = 'dashboard:chat'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    allPostBookmarks = blog.models.BlogPostBookmark.objects.filter(userID_id=user_id).order_by('-dateTimeAdded')
    #[KIV] get allInfoBookmarks for current user_id

    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    if request.method == 'POST':
        # print("hi POST")
        if request.is_ajax():
            if request.POST['requestType'] == 'deleteBookmark':
                # print("hi POST ajax deleteBookmark") # Test
                bookmarkType = request.POST['bookmarkType']
                bookmarkID = int(request.POST['bookmarkID'])

                # print("bookmarkType: " + bookmarkType) #Test
                # print("bookmarkID: " + str(bookmarkID)) #Test

                context = {}

                if bookmarkType == 'post':
                    # print("bookmarkType is post") #Test
                    blog.models.BlogPostBookmark.objects.get(id=bookmarkID).delete()
                    allPostBookmarks = blog.models.BlogPostBookmark.objects.filter(userID_id=user_id).order_by('-dateTimeAdded')
                    # print("allPostBookmarks: " + str(allPostBookmarks)) #Test

                    context = {
                        'allPostBookmarks': allPostBookmarks
                    }
                    return render(request, 'dashboard/nonAdminBookmarkContent1.html', context)
                #[KIV] EDIT WITH AIN's PART
                #elif bookmarkType == 'info':
                    #delete info bookmark record of the selected id
                    #update allInfoBookmarks for current user_id
                    #return render(request, 'dashboard/nonAdminBookmarkContent2.html', context)
    else:      
        if request.is_ajax():
            if request.GET.get('requestType') == 'findPostTitle' or request.GET.get('requestType') == 'sortPostDate':
                search_post = request.GET.get('search_post', None)
                sort_order = request.GET.get('sort_order', None)
            
                if search_post is not None:
                    allPostIDsinUserBookmark = list(allPostBookmarks.values_list('blogPostID_id', flat=True))
                    # print("allPostIDsinUserBookmark: " + str(allPostIDsinUserBookmark)) #Test
                    allBookmarkedPosts = blog.models.BlogPost.objects.filter(id__in=allPostIDsinUserBookmark)
                    # print("allBookmarkedPosts: " + str(allBookmarkedPosts)) #Test
                    filteredPosts = allBookmarkedPosts.filter(title__icontains=search_post)
                    # print("filteredPosts: " + str(filteredPosts)) #Test
                    filteredPostIDs = list(filteredPosts.values_list('id', flat=True))
                    # print("filteredPostIDs: " + str(filteredPostIDs)) #Test
                    allPostBookmarks = allPostBookmarks.filter(blogPostID_id__in=filteredPostIDs)
                    # print("allPostBookmarks: " + str(allPostBookmarks)) #Test

                if sort_order == 'Terkini':
                    allPostBookmarks = allPostBookmarks.order_by('-dateTimeAdded')
                elif sort_order == 'Paling Lama':
                    allPostBookmarks = allPostBookmarks.order_by('dateTimeAdded')
                
                # print("allPostBookmarks: " + str(allPostBookmarks)) #Test
                    
                context = {
                    'user_type': user_type,
                    'user_id': user_id,
                    'allPostBookmarks': allPostBookmarks
                }

                return render(request, 'dashboard/nonAdminBookmarkContent1.html', context)
            #[KIV] sortInfoCategory/sortInfoDate
            #else if request.GET.get('requestType') == 'sortInfoCategory' or request.GET.get('requestType') == 'sortInfoDate':
                #do the same for info filtering
                #return render(request, 'dashboard/nonAdminBookmarkContent2.html', context)
        else:
            if user_type == "pelajar" and 'S' in user_id:
                dashboardNav = " Pelajar"
            elif user_type == "penjaga" and 'P' in user_id:
                dashboardNav = " Penjaga"
            elif user_type == "guru" and 'T' in user_id:
                dashboardNav = " Guru"
                
            context = {
                'dashboardNav': dashboardNav,
                'user_type': user_type,
                'user_id': user_id,
                'username': username,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard':urlDashboard,
                'logout': urlLogout,
                'settings': urlProfile,
                'bookmark': urlBookmark,
                'report': urlReport,
                'chat': urlChat,
                'suggestions': urlSuggestion,
                'allPostBookmarks': allPostBookmarks,
                'allNotif': allNotif,
                'unreadNotifCnt': unreadNotifCnt
            } 
            return render(request, 'dashboard/nonAdminBookmark.html', context)

def nonAdminReport(request, user_type, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    username = userRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'

    urlProfile = 'dashboard:profile-settings'
    urlBookmark = 'dashboard:bookmark'
    urlReport = 'dashboard:report'
    # urlChat = 'dashboard:chat-nonadmin'
    urlChat = 'dashboard:chat'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = " Pelajar"

        # div-career-student
        currentPlayerAllFieldRecords = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, isFinish=True)
        fieldIDList = list(currentPlayerAllFieldRecords.order_by('fieldID_id').values_list("fieldID_id", flat=True).distinct("fieldID_id"))
        criteria_score_list = []
        criteria_hint_list = []
        criteria_time_list = []
        final_field_criteria_dict = {}

        for i in range(len(fieldIDList)):
            currentIterFieldRecords = currentPlayerAllFieldRecords.filter(fieldID_id=fieldIDList[i])
            currentFieldSessionCount = currentIterFieldRecords.count()

            #for criteria_score_list
            fullScoreEasyDict = currentIterFieldRecords.aggregate(Sum('countEasy'))
            fullScoreEasy = fullScoreEasyDict['countEasy__sum']*6
            fullScoreMediumDict = currentIterFieldRecords.aggregate(Sum('countMedium'))
            fullScoreMedium = fullScoreMediumDict['countMedium__sum']*8
            fullScoreHardDict = currentIterFieldRecords.aggregate(Sum('countHard'))
            fullScoreHard = fullScoreHardDict['countHard__sum']*10
            totalFullScore = fullScoreEasy + fullScoreMedium + fullScoreHard

            #deducted hint already because took from currentPointsEarned
            earnedScoreDict = currentIterFieldRecords.aggregate(Sum('currentPointsEarned'))
            earnedScore = earnedScoreDict['currentPointsEarned__sum']

            if totalFullScore > 0:
                criteria_score_list.append(round((earnedScore/totalFullScore)*45, 2))
            else:
                criteria_score_list.append(0)

            #for criteria_hint_list
            fullHintCount = 30*currentFieldSessionCount
            usedHintCountDict = currentIterFieldRecords.aggregate(Sum('hintsUsedCount'))
            usedHintCount = usedHintCountDict['hintsUsedCount__sum']

            criteria_hint_list.append(round(((fullHintCount-usedHintCount)/fullHintCount)*30, 2))

            #for criteria_time_list (in seconds)
            fullTimeEasy = fullScoreEasyDict['countEasy__sum']*10
            fullTimeMedium = fullScoreMediumDict['countMedium__sum']*20
            fullTimeHard = fullScoreHardDict['countHard__sum']*30
            totalFullTime = fullTimeEasy + fullTimeMedium + fullTimeHard

            timeList = list(currentIterFieldRecords.values_list('timeTaken', flat=True))
            totalTimeTaken = timedelta(seconds=sum(td.total_seconds() for td in timeList)).total_seconds()

            #rasanya no totalFullTime should be 0? Sebab mesti time akan running at least 1s. But this one happened sebab
            #while debugging something dulu it didnt manage to track time but now should be ok
            if totalFullTime > 0:
                criteria_time_list.append(round(((totalFullTime-totalTimeTaken)/totalFullTime)*25, 2))
            else:
                criteria_time_list.append(0)

            final_field_criteria_dict[fieldIDList[i]] = criteria_score_list[i] + criteria_hint_list[i] + criteria_time_list[i]
        
        k = Counter(final_field_criteria_dict)
    
        # Finding 3 highest values
        three_highest_fields = k.most_common(3) #returns list = [(fieldID_1, perc_1), (fieldID_2, perc_2), (fieldID_3, perc_3)]
        three_highest_fieldIDs = list(field[0] for field in three_highest_fields)
        three_highest_fieldPerc = list(field[1] for field in three_highest_fields)
        three_highest_fieldImage = []
        three_highest_fieldName = []

        #append image URL into imageURLList following the order of gameFields
        for fieldID in three_highest_fieldIDs:
            for field in quiz.models.GameField.objects.all():
                if fieldID == field.id:
                    three_highest_fieldName.append(field.name)
                    for image in quiz.models.ImageField.objects.all():
                        if field.imageURL_id == image.id:
                            three_highest_fieldImage.append(image.imageURL)
                            break
                    break

        context = {
            'dashboardNav': dashboardNav,
            'user_type': user_type,
            'user_id': user_id,
            'username': username,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout,
            'settings': urlProfile,
            'bookmark': urlBookmark,
            'report': urlReport,
            'chat': urlChat,
            'suggestions': urlSuggestion,
            'allNotif': allNotif,
            'unreadNotifCnt': unreadNotifCnt,
            'three_highest_fieldName': three_highest_fieldName,
            'three_highest_fieldImage': three_highest_fieldImage,
            'recCnt': len(three_highest_fieldName)
        } 
        return render(request, 'dashboard/nonAdminReport.html', context)
    elif user_type == "penjaga" and 'P' in user_id:
        dashboardNav = " Penjaga"

        parentStudents = dashboard.models.Student.objects.filter(parentID_id=user_id).order_by('name')
        parentStudentsCnt = parentStudents.count()
        print("parentStudentsCnt: " + str(parentStudentsCnt))

        filtered_student = parentStudents.first()
        print("filtered_student: " + str(filtered_student))

        if parentStudentsCnt > 0:
            currentPlayerAllFieldRecords = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=filtered_student.ID_id, isFinish=True)
            fieldIDList = list(currentPlayerAllFieldRecords.order_by('fieldID_id').values_list("fieldID_id", flat=True).distinct("fieldID_id"))
            criteria_score_list = []
            criteria_hint_list = []
            criteria_time_list = []
            final_field_criteria_dict = {}

            for i in range(len(fieldIDList)):
                currentIterFieldRecords = currentPlayerAllFieldRecords.filter(fieldID_id=fieldIDList[i])
                currentFieldSessionCount = currentIterFieldRecords.count()

                #for criteria_score_list
                fullScoreEasyDict = currentIterFieldRecords.aggregate(Sum('countEasy'))
                fullScoreEasy = fullScoreEasyDict['countEasy__sum']*6
                fullScoreMediumDict = currentIterFieldRecords.aggregate(Sum('countMedium'))
                fullScoreMedium = fullScoreMediumDict['countMedium__sum']*8
                fullScoreHardDict = currentIterFieldRecords.aggregate(Sum('countHard'))
                fullScoreHard = fullScoreHardDict['countHard__sum']*10
                totalFullScore = fullScoreEasy + fullScoreMedium + fullScoreHard

                #deducted hint already because took from currentPointsEarned
                earnedScoreDict = currentIterFieldRecords.aggregate(Sum('currentPointsEarned'))
                earnedScore = earnedScoreDict['currentPointsEarned__sum']

                if totalFullScore > 0:
                    criteria_score_list.append(round((earnedScore/totalFullScore)*45, 2))
                else:
                    criteria_score_list.append(0)

                #for criteria_hint_list
                fullHintCount = 30*currentFieldSessionCount
                usedHintCountDict = currentIterFieldRecords.aggregate(Sum('hintsUsedCount'))
                usedHintCount = usedHintCountDict['hintsUsedCount__sum']

                criteria_hint_list.append(round(((fullHintCount-usedHintCount)/fullHintCount)*30, 2))

                #for criteria_time_list (in seconds)
                fullTimeEasy = fullScoreEasyDict['countEasy__sum']*10
                fullTimeMedium = fullScoreMediumDict['countMedium__sum']*20
                fullTimeHard = fullScoreHardDict['countHard__sum']*30
                totalFullTime = fullTimeEasy + fullTimeMedium + fullTimeHard

                timeList = list(currentIterFieldRecords.values_list('timeTaken', flat=True))
                totalTimeTaken = timedelta(seconds=sum(td.total_seconds() for td in timeList)).total_seconds()

                #rasanya no totalFullTime should be 0? Sebab mesti time akan running at least 1s. But this one happened sebab
                #while debugging something dulu it didnt manage to track time but now should be ok
                if totalFullTime > 0:
                    criteria_time_list.append(round(((totalFullTime-totalTimeTaken)/totalFullTime)*25, 2))
                else:
                    criteria_time_list.append(0)

                final_field_criteria_dict[fieldIDList[i]] = criteria_score_list[i] + criteria_hint_list[i] + criteria_time_list[i]
            
            k = Counter(final_field_criteria_dict)
        
            # Finding 3 highest values
            three_highest_fields = k.most_common(3) #returns list = [(fieldID_1, perc_1), (fieldID_2, perc_2), (fieldID_3, perc_3)]
            three_highest_fieldIDs = list(field[0] for field in three_highest_fields)
            three_highest_fieldPerc = list(field[1] for field in three_highest_fields)
            three_highest_fieldImage = []
            three_highest_fieldName = []

            #append image URL into imageURLList following the order of gameFields
            for fieldID in three_highest_fieldIDs:
                for field in quiz.models.GameField.objects.all():
                    if fieldID == field.id:
                        three_highest_fieldName.append(field.name)
                        for image in quiz.models.ImageField.objects.all():
                            if field.imageURL_id == image.id:
                                three_highest_fieldImage.append(image.imageURL)
                                break
                        break
        else:
            three_highest_fieldImage = []
            three_highest_fieldName = []

        # div-career-parent
        if request.is_ajax():
            if request.GET.get('requestType') == 'filterStudentName':
                print("filterStudentName")
                filteredStudentID = request.GET.get('filteredStudentID', None)
            
                if filteredStudentID is not None:
                    filtered_student = parentStudents.get(ID_id=filteredStudentID)
                    print("filtered_student: " + str(filtered_student)) #Test

                currentPlayerAllFieldRecords = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=filtered_student.ID_id, isFinish=True)
                fieldIDList = list(currentPlayerAllFieldRecords.order_by('fieldID_id').values_list("fieldID_id", flat=True).distinct("fieldID_id"))
                criteria_score_list = []
                criteria_hint_list = []
                criteria_time_list = []
                final_field_criteria_dict = {}

                for i in range(len(fieldIDList)):
                    currentIterFieldRecords = currentPlayerAllFieldRecords.filter(fieldID_id=fieldIDList[i])
                    currentFieldSessionCount = currentIterFieldRecords.count()

                    #for criteria_score_list
                    fullScoreEasyDict = currentIterFieldRecords.aggregate(Sum('countEasy'))
                    fullScoreEasy = fullScoreEasyDict['countEasy__sum']*6
                    fullScoreMediumDict = currentIterFieldRecords.aggregate(Sum('countMedium'))
                    fullScoreMedium = fullScoreMediumDict['countMedium__sum']*8
                    fullScoreHardDict = currentIterFieldRecords.aggregate(Sum('countHard'))
                    fullScoreHard = fullScoreHardDict['countHard__sum']*10
                    totalFullScore = fullScoreEasy + fullScoreMedium + fullScoreHard

                    #deducted hint already because took from currentPointsEarned
                    earnedScoreDict = currentIterFieldRecords.aggregate(Sum('currentPointsEarned'))
                    earnedScore = earnedScoreDict['currentPointsEarned__sum']

                    if totalFullScore > 0:
                        criteria_score_list.append(round((earnedScore/totalFullScore)*45, 2))
                    else:
                        criteria_score_list.append(0)

                    #for criteria_hint_list
                    fullHintCount = 30*currentFieldSessionCount
                    usedHintCountDict = currentIterFieldRecords.aggregate(Sum('hintsUsedCount'))
                    usedHintCount = usedHintCountDict['hintsUsedCount__sum']

                    criteria_hint_list.append(round(((fullHintCount-usedHintCount)/fullHintCount)*30, 2))

                    #for criteria_time_list (in seconds)
                    fullTimeEasy = fullScoreEasyDict['countEasy__sum']*10
                    fullTimeMedium = fullScoreMediumDict['countMedium__sum']*20
                    fullTimeHard = fullScoreHardDict['countHard__sum']*30
                    totalFullTime = fullTimeEasy + fullTimeMedium + fullTimeHard

                    timeList = list(currentIterFieldRecords.values_list('timeTaken', flat=True))
                    totalTimeTaken = timedelta(seconds=sum(td.total_seconds() for td in timeList)).total_seconds()

                    #rasanya no totalFullTime should be 0? Sebab mesti time akan running at least 1s. But this one happened sebab
                    #while debugging something dulu it didnt manage to track time but now should be ok
                    if totalFullTime > 0:
                        criteria_time_list.append(round(((totalFullTime-totalTimeTaken)/totalFullTime)*25, 2))
                    else:
                        criteria_time_list.append(0)

                    final_field_criteria_dict[fieldIDList[i]] = criteria_score_list[i] + criteria_hint_list[i] + criteria_time_list[i]
                
                k = Counter(final_field_criteria_dict)
            
                # Finding 3 highest values
                three_highest_fields = k.most_common(3) #returns list = [(fieldID_1, perc_1), (fieldID_2, perc_2), (fieldID_3, perc_3)]
                three_highest_fieldIDs = list(field[0] for field in three_highest_fields)
                three_highest_fieldPerc = list(field[1] for field in three_highest_fields)
                three_highest_fieldImage = []
                three_highest_fieldName = []

                #append image URL into imageURLList following the order of gameFields
                for fieldID in three_highest_fieldIDs:
                    for field in quiz.models.GameField.objects.all():
                        if fieldID == field.id:
                            three_highest_fieldName.append(field.name)
                            for image in quiz.models.ImageField.objects.all():
                                if field.imageURL_id == image.id:
                                    three_highest_fieldImage.append(image.imageURL)
                                    break
                            break
            
                context = {
                    'dashboardNav': dashboardNav,
                    'user_type': user_type,
                    'user_id': user_id,
                    'username': username,
                    'test': urlTest,
                    'blog': urlBlog,
                    'quiz': urlQuiz,
                    'search': urlSearch,
                    'dashboard':urlDashboard,
                    'logout': urlLogout,
                    'settings': urlProfile,
                    'bookmark': urlBookmark,
                    'report': urlReport,
                    'chat': urlChat,
                    'suggestions': urlSuggestion,
                    'allNotif': allNotif,
                    'unreadNotifCnt': unreadNotifCnt,
                    'parentStudents': parentStudents,
                    'parentStudentsCnt': parentStudentsCnt,
                    'filtered_student': filtered_student,
                    'three_highest_fieldName': three_highest_fieldName,
                    'three_highest_fieldImage': three_highest_fieldImage,
                    'recCnt': len(three_highest_fieldName)
                }

                return render(request, 'dashboard/nonAdminReportContentParent.html', context)
        else:
            print("GET")
        
        context = {
            'dashboardNav': dashboardNav,
            'user_type': user_type,
            'user_id': user_id,
            'username': username,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout,
            'settings': urlProfile,
            'bookmark': urlBookmark,
            'report': urlReport,
            'chat': urlChat,
            'suggestions': urlSuggestion,
            'allNotif': allNotif,
            'unreadNotifCnt': unreadNotifCnt,
            'parentStudents': parentStudents,
            'parentStudentsCnt': parentStudentsCnt,
            'filtered_student': filtered_student,
            'three_highest_fieldName': three_highest_fieldName,
            'three_highest_fieldImage': three_highest_fieldImage,
            'recCnt': len(three_highest_fieldName)
        } 

        return render(request, 'dashboard/nonAdminReport.html', context)
    elif user_type == "guru" and 'T' in user_id:
        dashboardNav = " Guru"
        
        #For DIV 1: game-perf
        def get_player_name_score_list(allFieldPlayerSessions):
            playerIDList = list(allFieldPlayerSessions.order_by('fieldPlayerID_id').values_list("fieldPlayerID_id", flat=True).distinct("fieldPlayerID_id"))
            playersCnt = len(playerIDList)
            playerNameScoreList = []

            for playerID in playerIDList:
                # print("playerID: " + str(playerID))

                currentPlayerSessions = allFieldPlayerSessions.filter(fieldPlayerID_id=playerID)
                currentPlayerScoreDict = currentPlayerSessions.aggregate(Sum('currentPointsEarned'))
                currentPlayerRecord = quiz.models.Player.objects.get(ID_id=playerID)
                playerNameScoreList.append((currentPlayerRecord.ID.name, currentPlayerScoreDict['currentPointsEarned__sum']))

                # print("playerScoreList: " + str(playerNameScoreList))

            playerNameScoreList = sorted(playerNameScoreList, key=lambda x: x[1], reverse=True)
            # print("sorted playerNameScoreList: " + str(playerNameScoreList))

            return playerNameScoreList, playersCnt

        def get_chart_data(allFieldPlayerSessions):
            totalScoreAllFieldList = list(allFieldPlayerSessions.values_list('currentPointsEarned', flat=True))
            fieldIDList = list(allFieldPlayerSessions.order_by('fieldID_id').values_list("fieldID_id", flat=True).distinct("fieldID_id"))

            #Card 1: Total Players
            results = get_player_name_score_list(allFieldPlayerSessions)
            playerNameScoreList = results[0]
            playersCnt = results[1]
                
            #Card 2: Total No of Plays
            playCount = allFieldPlayerSessions.count()

            #Card 3: Average score per session (all fields)
            totalScoreAllField = 0

            for score in totalScoreAllFieldList:
                totalScoreAllField += score

            if playCount > 0:
                avgSessionScore = int(round(totalScoreAllField/playCount, 0))
            else:
                avgSessionScore = 0

            #Card 4: Average hints used per session (all fields)
            totalHintsUsedDict = allFieldPlayerSessions.aggregate(Sum('hintsUsedCount'))

            if playCount > 0:
                avgHintsUsed = int(round(totalHintsUsedDict['hintsUsedCount__sum']/playCount, 0))
            else:
                avgHintsUsed = 0

            #Card 5: Average time taken per session (all fields)
            timeList = list(allFieldPlayerSessions.values_list('timeTaken', flat=True))
            totalTimeTaken = timedelta(seconds=sum(td.total_seconds() for td in timeList))

            if playCount > 0:
                avgSessionTimeTaken = int(round(totalTimeTaken.total_seconds()/playCount, 0))
            else:
                avgSessionTimeTaken = 0

            minutes = avgSessionTimeTaken // 60
            seconds = avgSessionTimeTaken % 60

            if minutes != 0 and seconds != 0:
                avgSessionTimeTaken = '{} minit {} saat'.format(minutes, seconds)
            elif minutes == 0:
                avgSessionTimeTaken = '{} saat'.format(seconds)
            elif seconds == 0:
                avgSessionTimeTaken = '{} minit'.format(minutes)

            #Card 6: Last Played Time
            if playCount > 0:
                lastPlayedTime = allFieldPlayerSessions.last().dateLastPlayed #Format to string HH:mmPM, DD/MM/YYYY
            else:
                lastPlayedTime = datetime.now()

            #Card 7: (Bar Chart) 5 Most Played Field
            fieldIDList = list(allFieldPlayerSessions.order_by('fieldID_id').values_list("fieldID_id", flat=True).distinct("fieldID_id"))
            allGameFields = quiz.models.GameField.objects.filter(id__in=fieldIDList).order_by('id')

            fieldPlayedCountList = []
            fieldNameList = []
            fieldName_CountDict = {}

            for fieldID in fieldIDList:
                fieldPlayedCountList.append(0)

            for session in allFieldPlayerSessions:
                for i in range(len(fieldIDList)):
                    if session.fieldID_id == fieldIDList[i]:
                        fieldPlayedCountList[i] += 1
                        break

            for i in range(len(fieldIDList)):
                for field in allGameFields:
                    if fieldIDList[i] == field.id:
                        fieldNameList.append(field.name)
                        fieldName_CountDict[field.name] = fieldPlayedCountList[i]
                        break
            
            topFive_fieldName_CountDict = dict(Counter(fieldName_CountDict).most_common(5))

            # Card 8, 9 & 10
            avgSessionScoreByFieldList = []
            avgSessionHintByFieldList = []
            avgSessionTimeTakenByFieldList = []

            for i in range(len(fieldIDList)):
                currentIterFieldRecords = allFieldPlayerSessions.filter(fieldID_id=fieldIDList[i])
                currentFieldSessionCount = currentIterFieldRecords.count()

                totalScoreCurrentFieldDict = currentIterFieldRecords.aggregate(Sum('currentPointsEarned'))
                totalHintCurrentFieldDict = currentIterFieldRecords.aggregate(Sum('hintsUsedCount'))
                timeList = list(currentIterFieldRecords.values_list('timeTaken', flat=True))
                totalTimeTaken = timedelta(seconds=sum(td.total_seconds() for td in timeList))
                avgTimeTaken_unformatted = int(round(totalTimeTaken.total_seconds()/currentFieldSessionCount, 0))

                avgSessionScoreByFieldList.append(int(round(totalScoreCurrentFieldDict['currentPointsEarned__sum']/currentFieldSessionCount, 0)))
                avgSessionHintByFieldList.append(int(round(totalHintCurrentFieldDict['hintsUsedCount__sum']/currentFieldSessionCount, 0)))
                avgSessionTimeTakenByFieldList.append(avgTimeTaken_unformatted)

            fieldName_ScoreDict = {}
            fieldName_HintDict = {}
            fieldName_TimeDict = {}

            for i in range(len(fieldIDList)):
                for field in allGameFields:
                    if fieldIDList[i] == field.id:
                        fieldNameList.append(field.name)
                        fieldName_ScoreDict[field.name] = avgSessionScoreByFieldList[i]
                        fieldName_HintDict[field.name] = avgSessionHintByFieldList[i]
                        fieldName_TimeDict[field.name] = avgSessionTimeTakenByFieldList[i]
                        break
            
            # print("fieldName_ScoreDict: " + str(fieldName_ScoreDict)) #Test

            topFive_fieldName_ScoreDict = dict(Counter(fieldName_ScoreDict).most_common(5))
            # print("topFive_fieldName_ScoreDict: " + str(topFive_fieldName_ScoreDict)) #Test

            topFive_fieldName_HintDict = dict(sorted(fieldName_HintDict.items(), key = itemgetter(1))[:5])
            # print("topFive_fieldName_HintDict: " + str(topFive_fieldName_HintDict)) #Test

            topFive_fieldName_TimeDict = dict(sorted(fieldName_TimeDict.items(), key = itemgetter(1))[:5])
            # print("topFive_fieldName_TimeDict: " + str(topFive_fieldName_TimeDict)) #Test

            avgSessionScoreByFieldList = sorted(avgSessionScoreByFieldList, reverse=True)
            avgSessionScoreByFieldList = avgSessionScoreByFieldList[:5]
            avgSessionHintByFieldList = sorted(avgSessionHintByFieldList)
            avgSessionHintByFieldList = avgSessionHintByFieldList[:5]
            avgSessionTimeTakenByFieldList = sorted(avgSessionTimeTakenByFieldList)
            avgSessionTimeTakenByFieldList = avgSessionTimeTakenByFieldList[:5]

            # For ALL CHARTS(field colors)
            colors = [
                    "rgb(17,112,170)", "rgb(200,82,0)", "rgb(252,125,11)",
                    "rgb(123,132,143)", "rgb(163,172,185)", "rgb(163,204,233)",
                    "rgb(87,96,108)", "rgb(255,188,121)", "rgb(95,162,206)",
                    "rgb(200,208,217)", "rgb(255, 194, 10)", "rgb(64, 176, 66)",
                    "rgb(93, 58, 155)", "rgb(211, 95, 183)", "rgb(212, 17, 89)",
                    "rgb(86, 1, 151)", "rgb(132, 0, 205)", "rgb(255, 146, 253)",
                    "rgb(90, 0, 15)", "rgb(164, 1, 34)", "rgb(69, 2, 112)",
                    "rgb(153, 79, 0)", "rgb(254, 254, 98)", "rgb(220, 76, 103)"
                ]

            allGameFieldColorsDict = {}
            allGameFields = quiz.models.GameField.objects.all().order_by('id')

            for i in range(len(allGameFields)):
                allGameFieldColorsDict[allGameFields[i].name] = colors[i]
            
            # print("allGameFieldColorsDict: " + str(allGameFieldColorsDict)) #Test

            playedFieldColorList = colors[:len(fieldNameList)]
            # END color designation

            return topFive_fieldName_CountDict, allGameFieldColorsDict, topFive_fieldName_ScoreDict, avgSessionScoreByFieldList, topFive_fieldName_HintDict, avgSessionHintByFieldList, topFive_fieldName_TimeDict, avgSessionTimeTakenByFieldList, playCount, totalScoreAllField, avgSessionScore, avgHintsUsed, avgSessionTimeTaken, lastPlayedTime, playerNameScoreList, playersCnt

        allFieldPlayerSessions = quiz.models.FieldPlayerSession.objects.filter(isFinish=True).order_by('id')

        results = get_chart_data(allFieldPlayerSessions)

        topFive_fieldName_CountDict = results[0]
        allGameFieldColorsDict = results[1]
        topFive_fieldName_ScoreDict = results[2]
        avgSessionScoreByFieldList = results[3]
        topFive_fieldName_HintDict = results[4]
        avgSessionHintByFieldList = results[5]
        topFive_fieldName_TimeDict = results[6]
        avgSessionTimeTakenByFieldList = results[7]
        playCount = results[8]
        totalScoreAllField = results[9]
        avgSessionScore = results[10]
        avgHintsUsed = results[11]
        avgSessionTimeTaken = results[12]
        lastPlayedTime = results[13]
        playerNameScoreList = results[14]
        playersCnt = results[15]
        
        def get_filtered_session(filteredFormID, filtered_form):
            if filteredFormID != 1:
                filteredHomeroomTeacherClass = dashboard.models.HomeroomTeacherClass.objects.get(className=filtered_form.name)
                # print("filteredHomeroomTeacherClass: " + str(filteredHomeroomTeacherClass)) #Test
            
                studentIDList = list(dashboard.models.Student.objects.filter(studentClass_id=filteredHomeroomTeacherClass).values_list("ID_id", flat=True))
                # print("studentIDList: " + str(studentIDList)) #Test
            else:
                # print("yes")

                filteredHomeroomTeacherClass = dashboard.models.HomeroomTeacherClass.objects.all()
                # print("filteredHomeroomTeacherClass: " + str(filteredHomeroomTeacherClass)) #Test

                studentIDList = list(dashboard.models.Student.objects.all().values_list("ID_id", flat=True))
                # print("studentIDList: " + str(studentIDList)) #Test

            playerIDList = list(quiz.models.Player.objects.filter(ID__in=studentIDList).values_list('ID', flat=True))
            # print("playerIDList: " + str(playerIDList)) #Test

            allFieldPlayerSessions = quiz.models.FieldPlayerSession.objects.filter(isFinish=True, fieldPlayerID_id__in=playerIDList).order_by('id')
            # print("allFieldPlayerSessions: " + str(allFieldPlayerSessions)) #Test

            return allFieldPlayerSessions

        allForms = dashboard.models.ClassList.objects.all().order_by('name')

        #For DIV 2: parent-eng
        def get_filtered_student(filtered_form_parent ,filteredStudentID):
            # print("----------------DIV 2: parent-eng----------------") #Test

            if filtered_form_parent.id != 1:
                filtered_HTC = dashboard.models.HomeroomTeacherClass.objects.get(className=filtered_form_parent.name)
                allStudents = dashboard.models.Student.objects.filter(studentClass_id=filtered_HTC).order_by('studentClass', 'name')
            else:
                allStudents = dashboard.models.Student.objects.all().order_by('studentClass', 'name')

            # print("allStudents after filtered form: " + str(allStudents)) #Test

            get_one_student = False
            filtered_student_record = None

            if filteredStudentID != None:
                if filteredStudentID != '1':
                    filtered_student_record = allStudents.get(ID=filteredStudentID)
                    listOfParentIDs = [filtered_student_record.parentID_id]
                    get_one_student = True
                    # print("filtered_student_record after filtered student: " + str(filtered_student_record)) #Test
                    # print("listOfParentIDs after filtered student: " + str(listOfParentIDs)) #Test

            # Card 1: TotalBlogViews
            # print("Card 1: TotalBlogViews") #Test

            if get_one_student == False:
                if allStudents.count() > 0:
                    listOfParentIDs = list(allStudents.values_list('parentID_id', flat=True))
                else:
                    listOfParentIDs = []
                
            parentViews = blog.models.BlogPostViewsUser.objects.filter(userID_id__in=listOfParentIDs)
            viewsCnt = 0

            if parentViews.count() > 0:
                viewsCntDict = parentViews.aggregate(Sum('noOfViews'))
                viewsCnt = viewsCntDict['noOfViews__sum']

            # print("parentViews: " + str(parentViews)) #Test
            # print("viewsCnt: " + str(viewsCnt)) #Test

            # Card 2: TotalBlogComments
            # print("Card 2: TotalBlogComments") #Test

            parentComments = blog.models.BlogPostComment.objects.filter(userID_id__in=listOfParentIDs)
            commentsCnt = 0

            if parentComments.count() > 0:
                commentsCnt = parentComments.count()

            # print("parentComments: " + str(parentComments)) #Test
            # print("commentsCnt: " + str(commentsCnt)) #Test

            # Card 3: TotalBookmarks
            # print("Card 3: TotalBookmarks") #Test

            parentBlogBookmarks = blog.models.BlogPostBookmark.objects.filter(userID_id__in=listOfParentIDs)
            parentInfoBookmarks = dashboard.models.InfoDashboardBookmark.objects.filter(userID_id__in=listOfParentIDs)
            bookmarkCnt = 0

            if parentBlogBookmarks.count() > 0:
                bookmarkCnt += parentBlogBookmarks.count()
            if parentInfoBookmarks.count() > 0:
                bookmarkCnt += parentInfoBookmarks.count()

            # print("parentBlogBookmarks: " + str(parentBlogBookmarks)) #Test
            # print("parentInfoBookmarks: " + str(parentInfoBookmarks)) #Test
            # print("bookmarkCnt: " + str(bookmarkCnt)) #Test

            # Card 4: TotalSuggestions
            # print("Card 4: TotalSuggestions") #Test
            parentSuggestions = dashboard.models.Suggestion.objects.filter(creatorID_id__in=listOfParentIDs)
            suggestionCnt = 0

            if parentSuggestions.count() > 0:
                suggestionCnt = parentSuggestions.count()

            # print("parentSuggestions: " + str(parentSuggestions)) #Test
            # print("suggestionCnt: " + str(suggestionCnt)) #Test

            # Card 5: LastChatTime
            # Get all parent chat records where senderID is in listOfParentIDs order by id
            selectedParentChats = dashboard.models.Message.objects.filter(creatorID_id__in=listOfParentIDs).order_by('id')

            # If count above > 0, 
                # Get the last parent chat record from above
                # Get the time sent
            # Else
                # lastChatTime = 0

            if selectedParentChats.count() > 0:
                lastChatTime = selectedParentChats.last().dateTimeSent
            else:
                lastChatTime = 0

            # print("parentChats: " + str(lastParentChat)) #Test
            # print("lastChatTime: " + str(lastChatTime)) #Test
        
            return allStudents, get_one_student, filtered_student_record, viewsCnt, commentsCnt, bookmarkCnt, suggestionCnt, lastChatTime

        if request.method == 'POST':
            if request.is_ajax():
                if request.POST['requestType'] == 'updateStudentListModal':
                    filteredFormID = int(request.POST['filteredFormID'])

                    filtered_form = allForms.get(id=filteredFormID)
                    # print("filtered_form: " + str(filtered_form)) #Test
                
                    allFieldPlayerSessions = get_filtered_session(filteredFormID, filtered_form)

                    playerNameScoreList = get_player_name_score_list(allFieldPlayerSessions)[0]

                    # print("playerNameScoreList: " + str(playerNameScoreList))

                    context = {
                        'playerNameScoreList': playerNameScoreList
                    } 
                    return render(request, 'dashboard/nonAdminReportContentTeacher2.html', context)
        else:
            if request.is_ajax():
                if request.GET.get("requestType") == "Charts":
                    filteredFormID = int(request.GET.get('filteredFormID', None))

                    filtered_form = allForms.get(id=filteredFormID)
                    # print("filtered_form: " + str(filtered_form)) #Test
                
                    allFieldPlayerSessions = get_filtered_session(filteredFormID, filtered_form)

                    results = get_chart_data(allFieldPlayerSessions)
                    
                    topFive_fieldName_CountDict = results[0]
                    allGameFieldColorsDict = results[1]
                    topFive_fieldName_ScoreDict = results[2]
                    avgSessionScoreByFieldList = results[3]
                    topFive_fieldName_HintDict = results[4]
                    avgSessionHintByFieldList = results[5]
                    topFive_fieldName_TimeDict = results[6]
                    avgSessionTimeTakenByFieldList = results[7]

                    # Card 7
                    # print("-----Card 7-----") #Test
                    playedFieldColorList = []

                    for field in list(topFive_fieldName_CountDict.keys()):
                        # print("field: " + field) #Test
                        # print("allGameFieldColorsDict[field]: " + str(allGameFieldColorsDict[field])) #Test
                        playedFieldColorList.append(allGameFieldColorsDict[field])

                    # print("playedFieldColorList: " + str(playedFieldColorList)) #Test

                    most_played_field_chart_data = {
                        "labels": list(topFive_fieldName_CountDict.keys()),
                        "datasets":[{
                            "label": "Bilangan Sesi",
                            "data": list(topFive_fieldName_CountDict.values()),
                            "backgroundColor": playedFieldColorList
                        }]
                    }
                    
                    # Card 8
                    # print("-----Card 8-----") #Test
                    playedFieldColorList = []

                    for field in list(topFive_fieldName_ScoreDict.keys()):
                        # print("field: " + field) #Test
                        # print("allGameFieldColorsDict[field]: " + str(allGameFieldColorsDict[field])) #Test
                        playedFieldColorList.append(allGameFieldColorsDict[field])

                    # print("playedFieldColorList: " + str(playedFieldColorList)) #Test

                    avg_field_session_score_chart_data = {
                        "labels": list(topFive_fieldName_ScoreDict.keys()),
                        "datasets":[{ 
                            "label": "Purata Markah per Sesi",
                            "data": avgSessionScoreByFieldList,
                            "backgroundColor": playedFieldColorList
                        }]
                    }

                    # Card 9
                    # print("-----Card 9-----") #Test
                    playedFieldColorList = []

                    for field in list(topFive_fieldName_HintDict.keys()):
                        # print("field: " + field) #Test
                        # print("allGameFieldColorsDict[field]: " + str(allGameFieldColorsDict[field])) #Test
                        playedFieldColorList.append(allGameFieldColorsDict[field])

                    # print("playedFieldColorList: " + str(playedFieldColorList)) #Test

                    avg_field_session_hints_chart_data = {
                        "labels": list(topFive_fieldName_HintDict.keys()),
                        "datasets":[{ 
                            "label": "Purata Petunjuk Digunakan per Sesi",
                            "data": avgSessionHintByFieldList,
                            "backgroundColor": playedFieldColorList
                        }]
                    }

                    # Card 10
                    avg_field_session_time_chart_data = {
                        "labels": list(topFive_fieldName_TimeDict.keys()),
                        "datasets":[{
                            "label": "Purata Masa Diambil per Sesi",
                            "data": avgSessionTimeTakenByFieldList,
                            "fill": False,
                            "borderColor": 'rgb(179, 97, 173)',
                            "tension": 0.1
                        }]
                    }

                    data_dict = {
                        "most_played_field_chart_data": most_played_field_chart_data,
                        "avg_field_session_score_chart_data": avg_field_session_score_chart_data,
                        "avg_field_session_hints_chart_data": avg_field_session_hints_chart_data,
                        "avg_field_session_time_chart_data": avg_field_session_time_chart_data
                    }

                    return JsonResponse(data=data_dict, safe=False)
                elif request.GET.get("requestType") == "filterForm":
                    filteredFormID = int(request.GET.get('filteredFormID', None))

                    filtered_form = allForms.get(id=filteredFormID)
                    # print("filtered_form: " + str(filtered_form)) #Test
                
                    allFieldPlayerSessions = get_filtered_session(filteredFormID, filtered_form)

                    results = get_chart_data(allFieldPlayerSessions)
                    
                    topFive_fieldName_CountDict = results[0]
                    allGameFieldColorsDict = results[1]
                    topFive_fieldName_ScoreDict = results[2]
                    avgSessionScoreByFieldList = results[3]
                    topFive_fieldName_HintDict = results[4]
                    avgSessionHintByFieldList = results[5]
                    topFive_fieldName_TimeDict = results[6]
                    avgSessionTimeTakenByFieldList = results[7]
                    playCount = results[8]
                    totalScoreAllField = results[9]
                    avgSessionScore = results[10]
                    avgHintsUsed = results[11]
                    avgSessionTimeTaken = results[12]
                    lastPlayedTime = results[13]
                    playerNameScoreList = results[14]
                    playersCnt = results[15]
                    
                    context = {
                        'filtered_form': filtered_form,
                        'allForms': allForms,
                        'playerNameScoreList': playerNameScoreList,
                        'playersCnt': playersCnt,
                        'playCount': playCount,
                        'totalScoreAllField': totalScoreAllField,
                        'avgSessionScore': avgSessionScore,
                        'avgHintsUsed': avgHintsUsed,
                        'avgSessionTimeTaken': avgSessionTimeTaken,
                        'lastPlayedTime': lastPlayedTime
                    }
                    return render(request, 'dashboard/nonAdminReportContentTeacher1.html', context)
                elif request.GET.get("requestType") == "filterFormParent":
                    # print("requestType: filterFormParent") #Test

                    filteredFormID = int(request.GET.get('filteredFormID', None))
                    filteredStudentID = None

                    if request.GET.get('filteredStudentID') != None:
                        filteredStudentID = request.GET.get('filteredStudentID')

                    filtered_form_parent = allForms.get(id=filteredFormID)
                    has_filtered_form = True
                    has_filtered_student = True
                    filtered_student_record = None
                    # print("filtered_form_parent: " + str(filtered_form_parent)) #Test
                    # print("filteredStudentID: " + str(filteredStudentID)) #Test

                    results = get_filtered_student(filtered_form_parent, filteredStudentID)

                    if results[1] == False:
                        if results[0].count() == 1:
                            filtered_student_record = results[0].first()
                            allStudentsCnt = 1
                        else:
                            allStudentsCnt = results[0].count()
                    else:
                        filtered_student_record = results[2]
                        allStudentsCnt = 1
                    
                    context = {
                        'allForms': allForms,
                        'filtered_form_parent': filtered_form_parent,
                        'has_filtered_form': has_filtered_form,
                        'has_filtered_student': has_filtered_student,
                        'allStudents': results[0],
                        'allStudentsCnt': allStudentsCnt,
                        'get_one_student': results[1],
                        'filtered_student_record': filtered_student_record,
                        'viewsCnt': results[3],
                        'commentsCnt': results[4],
                        'bookmarkCnt': results[5],
                        'suggestionCnt': results[6],
                        'lastChatTime': results[7]
                    }
                    return render(request, 'dashboard/nonAdminReportContentTeacher3.html', context)
            else:
                filtered_form = allForms.get(id=1)
                filtered_form_parent = allForms.get(id=1)
                filteredStudentID = None
                has_filtered_form = False
                has_filtered_student = False

                results = get_filtered_student(filtered_form_parent, filteredStudentID)

                context = {
                    'dashboardNav': dashboardNav,
                    'user_type': user_type,
                    'user_id': user_id,
                    'username': username,
                    'test': urlTest,
                    'blog': urlBlog,
                    'quiz': urlQuiz,
                    'search': urlSearch,
                    'dashboard':urlDashboard,
                    'logout': urlLogout,
                    'settings': urlProfile,
                    'bookmark': urlBookmark,
                    'report': urlReport,
                    'chat': urlChat,
                    'suggestions': urlSuggestion,
                    'allNotif': allNotif,
                    'unreadNotifCnt': unreadNotifCnt,
                    'filtered_form': filtered_form,
                    'allForms': allForms,
                    'playerNameScoreList': playerNameScoreList,
                    'playersCnt': playersCnt,
                    'playCount': playCount,
                    'totalScoreAllField': totalScoreAllField,
                    'avgSessionScore': avgSessionScore,
                    'avgHintsUsed': avgHintsUsed,
                    'avgSessionTimeTaken': avgSessionTimeTaken,
                    'lastPlayedTime': lastPlayedTime,
                    'filtered_form_parent': filtered_form_parent,
                    'has_filtered_form': has_filtered_form,
                    'has_filtered_student': has_filtered_student,
                    'allStudents': results[0],
                    'allStudentsCnt': results[0].count(),
                    'filtered_student_record': results[2],
                    'viewsCnt': results[3],
                    'commentsCnt': results[4],
                    'bookmarkCnt': results[5],
                    'suggestionCnt': results[6],
                    'lastChatTime': results[7]
                } 
                return render(request, 'dashboard/nonAdminReport.html', context)

# def nonAdminChat(request, user_type, user_id):
def Chat(request, user_type, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    username = userRecord.username

    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    if user_type == 'admin':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        user_type= "admin"

        urlClassSettings = 'dashboard:class-settings'
        urlSuggestions = 'dashboard:suggestions-admin'
        # urlChat = 'dashboard:chat-admin'
        urlChat = 'dashboard:chat'

        dashboardNav = " Admin"

        def get_info_for_admin():
            allChatsForNonAdmin = dashboard.models.Message.objects.exclude(recipientID_id='A1').order_by('-dateTimeSent')
            print("allChatsForNonAdmin: " + str(allChatsForNonAdmin)) #Test

            distinctRecipientIDList = []
            distinctChatForNonAdmin_IDList = []
            distinct_recipID_chatID_dict = {}

            for chat in allChatsForNonAdmin:
                if chat.recipientID_id not in distinctRecipientIDList:
                    distinctRecipientIDList.append(chat.recipientID_id)
                    distinctChatForNonAdmin_IDList.append(chat.id)
                    distinct_recipID_chatID_dict[chat.recipientID_id] = chat.id
            
            print("distinctRecipientIDList:" + str(distinctRecipientIDList)) #Test
            print("distinctChatForNonAdmin_IDList:" + str(distinctChatForNonAdmin_IDList)) #Test

            allChatsFromNonAdmin = dashboard.models.Message.objects.exclude(creatorID_id='A1').order_by('-dateTimeSent')
            print("allChatsFromNonAdmin: " + str(allChatsFromNonAdmin)) #Test

            distinctCreatorIDList = []
            distinctChatFromNonAdmin_IDList = []
            distinct_creID_chatID_dict = {}

            for chat in allChatsFromNonAdmin:
                if chat.creatorID_id not in distinctCreatorIDList:
                    distinctCreatorIDList.append(chat.creatorID_id)
                    distinctChatFromNonAdmin_IDList.append(chat.id)
                    distinct_creID_chatID_dict[chat.creatorID_id] = chat.id
            
            print("distinctCreatorIDList:" + str(distinctCreatorIDList)) #Test
            print("distinctChatFromNonAdmin_IDList:" + str(distinctChatFromNonAdmin_IDList)) #Test

            allDistinctChatUsersIDList = list(dict.fromkeys(distinctRecipientIDList + distinctCreatorIDList))
            print("allDistinctChatUsersIDList: " + str(allDistinctChatUsersIDList)) #Test

            allDistinctChatForFromNA_IDList = []

            for userID in allDistinctChatUsersIDList:
                if userID in list(distinct_recipID_chatID_dict.keys()):
                    if userID in list(distinct_creID_chatID_dict.keys()):
                        if distinct_recipID_chatID_dict[userID] > distinct_creID_chatID_dict[userID]:
                            allDistinctChatForFromNA_IDList.append(distinct_recipID_chatID_dict[userID])
                        else:
                            allDistinctChatForFromNA_IDList.append(distinct_creID_chatID_dict[userID])
                    else:
                        allDistinctChatForFromNA_IDList.append(distinct_recipID_chatID_dict[userID])
                else:
                    allDistinctChatForFromNA_IDList.append(distinct_creID_chatID_dict[userID])

            print("allDistinctChatForFromNA_IDList: " + str(allDistinctChatForFromNA_IDList)) #Test
            allDistinctChatForFromNA_IDList.sort(reverse=True)
            print("allDistinctChatForFromNA_IDList desc: " + str(allDistinctChatForFromNA_IDList)) #Test

            allChats = dashboard.models.Message.objects.order_by('-dateTimeSent')

            # For non-admin users with no chat yet
            allDistinctChatUsersIDList.append('A1')
            allDistinctChatUsersIDList.append('NA')
            print("allDistinctChatUsersIDList with admin & NA: " + str(allDistinctChatUsersIDList)) #Test

            allNonChatUsers = dashboard.models.User.objects.exclude(ID__in=allDistinctChatUsersIDList).order_by('ID')
            print("allNonChatUsers: " + str(allNonChatUsers)) #Test

            allStudents = dashboard.models.Student.objects.all()
            allParents = dashboard.models.Parent.objects.all()
            allTeachers = dashboard.models.Teacher.objects.all()

            return distinctChatForNonAdmin_IDList, distinctChatFromNonAdmin_IDList, allDistinctChatUsersIDList, allDistinctChatForFromNA_IDList, allChats, allNonChatUsers, allStudents, allParents, allTeachers

        if request.method == 'POST':
            if request.is_ajax():
                if request.POST['requestType'] == 'clickChat' or request.POST['requestType'] == 'updateMessageAdmin':
                    if request.POST['requestType'] == 'updateMessageAdmin':
                        print("?????")
                        
                    chosenRecipientID = request.POST['chosenRecipientID']
                    print("chosenRecipientID: " + str(chosenRecipientID)) #Test

                    if request.POST['requestType'] == 'updateMessageAdmin':
                        typedMessage = request.POST['typedMessage']
                    else:
                        typedMessage = ""
                    print("typedMessage: " + str(typedMessage)) #Test

                    if chosenRecipientID != "":
                        chosenRecipient = dashboard.models.User.objects.get(ID=chosenRecipientID)
                        print("chosenRecipient: " + str(chosenRecipient)) #Test
                    else:
                        chosenRecipient = None
                        print("chosenRecipient: " + str(chosenRecipient)) #Test

                    results = get_info_for_admin()
                    distinctChatForNonAdmin_IDList = results[0]
                    distinctChatFromNonAdmin_IDList = results[1]
                    allDistinctChatUsersIDList = results[2]
                    allDistinctChatForFromNA_IDList = results[3]
                    allChats = results[4]
                    allNonChatUsers = results[5]
                    allStudents = results[6]
                    allParents = results[7]
                    allTeachers = results[8]

                    if chosenRecipientID != "":
                        if chosenRecipientID in allDistinctChatUsersIDList:
                            chosenUserAllChats = allChats.filter(Q(creatorID_id=chosenRecipientID) | Q(recipientID_id=chosenRecipientID)).order_by('dateTimeSent')
                            chosenRecipientLatestChatID = chosenUserAllChats.last().id
                        else:
                            chosenUserAllChats = None
                            chosenRecipientLatestChatID = 0
                    else:
                        chosenUserAllChats = None
                        chosenRecipientLatestChatID = 0
                    print("chosenUserAllChats: " + str(chosenUserAllChats)) #Test
                    print("chosenRecipientLatestChatID: " + str(chosenRecipientLatestChatID)) #Test

                    if chosenUserAllChats:
                        allUnreadChatFromNANotif = dashboard.models.Notification.objects.filter(typeID_id=3, recipientID_id='A1', senderID_id=chosenRecipientID, isOpen=False)
                        print("allUnreadChatFromNANotif: " + str(allUnreadChatFromNANotif)) #Test

                        if chosenUserAllChats.last().creatorID_id == chosenRecipientID:
                            for chat2 in chosenUserAllChats:
                                if chat2.isRead == False:
                                    chat2.isRead = True
                                    chat2.save()
                            for notif in allUnreadChatFromNANotif:
                                notif.isOpen = True
                                notif.save()
                        else: #chosenUserAllChats.last().recipientID_id == chosenRecipientID
                            latestMsgSentByNonAdmin = chosenUserAllChats.filter(creatorID_id=chosenRecipientID)
                            
                            if latestMsgSentByNonAdmin:
                                latestMsgSentByNonAdminID = latestMsgSentByNonAdmin.last().id
                                for chat in chosenUserAllChats.filter(id__lte=latestMsgSentByNonAdminID):
                                    if chat.isRead == False:
                                        chat.isRead = True
                                        chat.save()

                            for i in range(len(chosenUserAllChats)-1):
                                if chosenUserAllChats[i].isRead == False:
                                    chosenUserAllChats[i].isRead = True
                                    chosenUserAllChats[i].save()

                    print("chosenUserAllChats: " + str(chosenUserAllChats)) #Test

                    context = {
                        'distinctChatForNonAdmin_IDList': distinctChatForNonAdmin_IDList,
                        'distinctChatFromNonAdmin_IDList': distinctChatFromNonAdmin_IDList,
                        'allDistinctChatUsersIDList': allDistinctChatUsersIDList,
                        'allDistinctChatForFromNA_IDList': allDistinctChatForFromNA_IDList,
                        'allChats': allChats,
                        'allNonChatUsers': allNonChatUsers,
                        'allStudents': allStudents,
                        'allParents': allParents,
                        'allTeachers': allTeachers,
                        'chosenRecipient': chosenRecipient,
                        'chosenUserAllChats': chosenUserAllChats,
                        'chosenRecipientLatestChatID': chosenRecipientLatestChatID,
                        'typedMessage': typedMessage
                    } 
                    return render(request, 'dashboard/chatContentAdmin.html', context)
                elif request.POST['requestType'] == 'adminSendMessage':
                    newMessage = request.POST['newMessage']
                    chosenRecipientID = request.POST['chosenRecipientID']
                    print("newMessage: " + newMessage) #Test
                    print("chosenRecipientID: " + str(chosenRecipientID)) #Test

                    chosenRecipient = dashboard.models.User.objects.get(ID=chosenRecipientID)
                    print("chosenRecipient: " + str(chosenRecipient)) #Test

                    newMessageRecord = dashboard.models.Message.objects.create(bodyText=newMessage, creatorID_id='A1', recipientID_id=chosenRecipientID)
                    print("newMessageRecord: " + str(newMessageRecord)) #Test

                    results = get_info_for_admin()
                    distinctChatForNonAdmin_IDList = results[0]
                    distinctChatFromNonAdmin_IDList = results[1]
                    allDistinctChatUsersIDList = results[2]
                    allDistinctChatForFromNA_IDList = results[3]
                    allChats = results[4]
                    allNonChatUsers = results[5]
                    allStudents = results[6]
                    allParents = results[7]
                    allTeachers = results[8]

                    print("allChats with newmsg: " + str(allChats)) #Test

                    if chosenRecipientID in allDistinctChatUsersIDList:
                        chosenUserAllChats = allChats.filter(Q(creatorID_id=chosenRecipientID) | Q(recipientID_id=chosenRecipientID)).order_by('dateTimeSent')
                        chosenRecipientLatestChatID = chosenUserAllChats.last().id
                    else:
                        chosenUserAllChats = None
                        chosenRecipientLatestChatID = 0
                    print("chosenUserAllChats: " + str(chosenUserAllChats)) #Test
                    print("chosenRecipientLatestChatID: " + str(chosenRecipientLatestChatID)) #Test

                    if chosenUserAllChats:
                        if chosenUserAllChats.last().creatorID_id == chosenRecipientID:
                            for chat2 in chosenUserAllChats:
                                if chat2.isRead == False:
                                    chat2.isRead = True
                                    chat2.save()
                        else: #chosenUserAllChats.last().recipientID_id == chosenRecipientID
                            latestMsgSentByNonAdmin = chosenUserAllChats.filter(creatorID_id=chosenRecipientID)
                            
                            if latestMsgSentByNonAdmin:
                                latestMsgSentByNonAdminID = latestMsgSentByNonAdmin.last().id
                                for chat in chosenUserAllChats.filter(id__lte=latestMsgSentByNonAdminID):
                                    if chat.isRead == False:
                                        chat.isRead = True
                                        chat.save()

                            for i in range(len(chosenUserAllChats)-1):
                                if chosenUserAllChats[i].isRead == False:
                                    chosenUserAllChats[i].isRead = True
                                    chosenUserAllChats[i].save()

                    print("chosenUserAllChats: " + str(chosenUserAllChats)) #Test

                    #create notification (Type id 3 - New message from admin to non-admin)
                    dashboard.models.Notification.objects.create(senderID_id='A1', recipientID_id=newMessageRecord.recipientID_id, messageID_id=newMessageRecord.id, typeID_id=3)

                    context = {
                        'distinctChatForNonAdmin_IDList': distinctChatForNonAdmin_IDList,
                        'distinctChatFromNonAdmin_IDList': distinctChatFromNonAdmin_IDList,
                        'allDistinctChatUsersIDList': allDistinctChatUsersIDList,
                        'allDistinctChatForFromNA_IDList': allDistinctChatForFromNA_IDList,
                        'allChats': allChats,
                        'allNonChatUsers': allNonChatUsers,
                        'allStudents': allStudents,
                        'allParents': allParents,
                        'allTeachers': allTeachers,
                        'chosenRecipient': chosenRecipient,
                        'chosenUserAllChats': chosenUserAllChats,
                        'chosenRecipientLatestChatID': chosenRecipientLatestChatID
                    } 
                    return render(request, 'dashboard/chatContentAdmin.html', context)
        else:
            results = get_info_for_admin()
            distinctChatForNonAdmin_IDList = results[0]
            distinctChatFromNonAdmin_IDList = results[1]
            allDistinctChatUsersIDList = results[2]
            allDistinctChatForFromNA_IDList = results[3]
            allChats = results[4]
            allNonChatUsers = results[5]
            allStudents = results[6]
            allParents = results[7]
            allTeachers = results[8]

            context = {
                'dashboardNav': dashboardNav,
                'user_type': user_type,
                'user_id': user_id,
                'username': username,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard': urlDashboard,
                'logout': urlLogout,
                'settings': urlClassSettings,
                'suggestions': urlSuggestions,
                'chat': urlChat,
                'allNotif': allNotif,
                'unreadNotifCnt': unreadNotifCnt,
                'distinctChatForNonAdmin_IDList': distinctChatForNonAdmin_IDList,
                'distinctChatFromNonAdmin_IDList': distinctChatFromNonAdmin_IDList,
                'allDistinctChatUsersIDList': allDistinctChatUsersIDList,
                'allDistinctChatForFromNA_IDList': allDistinctChatForFromNA_IDList,
                'allChats': allChats,
                'allNonChatUsers': allNonChatUsers,
                'allStudents': allStudents,
                'allParents': allParents,
                'allTeachers': allTeachers
            }
    else:
        urlTest = 'test:index-nonadmin'
        urlBlog = 'blog:index'
        urlQuiz = 'quiz:index-student'
        urlSearch = 'search:index-nonadmin'
        urlDashboard = 'dashboard:index-nonadmin'
        urlLogout = 'dashboard:logout-confirm'

        urlProfile = 'dashboard:profile-settings'
        urlBookmark = 'dashboard:bookmark'
        urlReport = 'dashboard:report'
        # urlChat = 'dashboard:chat-nonadmin'
        urlChat = 'dashboard:chat'
        urlSuggestion = 'dashboard:suggestions-nonadmin'

        if user_type == "pelajar" and 'S' in user_id:
            dashboardNav = " Pelajar"

        elif user_type == "penjaga" and 'P' in user_id:
            dashboardNav = " Penjaga"
            
        elif user_type == "guru" and 'T' in user_id:
            dashboardNav = " Guru"

        def get_current_chat_msgs():
            currentChatMessages = dashboard.models.Message.objects.filter(Q(creatorID_id=user_id) | Q(recipientID_id=user_id)).order_by('dateTimeSent')
            print("*******************************************************")
            print("currentChatMessages: " + str(currentChatMessages)) #Test

            allUnreadChatFromAdminNotif = dashboard.models.Notification.objects.filter(typeID_id=3, recipientID_id=user_id, isOpen=False)
            print("allUnreadChatFromAdminNotif: " + str(allUnreadChatFromAdminNotif)) #Test

            if currentChatMessages:
                if currentChatMessages.last().creatorID_id == 'A1':
                    for chat in currentChatMessages:
                        if chat.isRead == False:
                            chat.isRead = True
                            chat.save()
                    for notif in allUnreadChatFromAdminNotif:
                        notif.isOpen = True
                        notif.save()
                else:
                    latestMsgSentByAdmin = currentChatMessages.filter(creatorID_id="A1")
                    
                    if latestMsgSentByAdmin:
                        latestMsgSentByAdminID = latestMsgSentByAdmin.last().id
                        for chat in currentChatMessages.filter(id__lte=latestMsgSentByAdminID):
                            if chat.isRead == False:
                                chat.isRead = True
                                chat.save()

            print("-----------------------------------------------------------")
            print("currentChatMessages after update: " + str(currentChatMessages)) #Test
            print("allUnreadChatFromAdminNotif after update: " + str(allUnreadChatFromAdminNotif)) #Test

            return currentChatMessages

        if request.method == 'POST':
            if request.is_ajax():
                if request.POST['requestType'] == 'nonAdminSendMessage':
                    newMessage = request.POST['newMessage']
                    print("newMessage: " + newMessage) #Test

                    newMessageRecord = dashboard.models.Message.objects.create(bodyText=newMessage, creatorID_id=user_id, recipientID_id='A1')
                    print("newMessageRecord: " + str(newMessageRecord)) #Test

                    #create notification (Type id 3 - New message from non-admin to admin)
                    dashboard.models.Notification.objects.create(senderID_id=user_id, recipientID_id='A1', messageID_id=newMessageRecord.id, typeID_id=3)

                    context = {
                        'user_id': user_id,
                        'currentChatMessages': get_current_chat_msgs(),
                        'newMessageID': newMessageRecord.id
                    } 
                    return render(request, 'dashboard/chatContentNonAdmin.html', context)
                elif request.POST['requestType'] == 'updateMessageNonAdmin':
                    typedMessage = request.POST['typedMessage']
                    print("typedMessage: " + typedMessage) #Test

                    context = {
                        'user_id': user_id,
                        'typedMessage': typedMessage,
                        'currentChatMessages': get_current_chat_msgs(),
                    } 
                    return render(request, 'dashboard/chatContentNonAdmin.html', context)
        else:            
            context = {
                'dashboardNav': dashboardNav,
                'user_type': user_type,
                'user_id': user_id,
                'username': username,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard':urlDashboard,
                'logout': urlLogout,
                'settings': urlProfile,
                'bookmark': urlBookmark,
                'report': urlReport,
                'chat': urlChat,
                'suggestions': urlSuggestion,
                'allNotif': allNotif,
                'unreadNotifCnt': unreadNotifCnt,
                'currentChatMessages': get_current_chat_msgs()
            }

    return render(request, 'dashboard/chat.html', context)

def nonAdminSuggestions(request, user_type, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    username = userRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'

    urlProfile = 'dashboard:profile-settings'
    urlBookmark = 'dashboard:bookmark'
    urlReport = 'dashboard:report'
    # urlChat = 'dashboard:chat-nonadmin'
    urlChat = 'dashboard:chat'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    statusList = ['Dihantar', 'Sedang Diproses', 'Ditutup']
    allSuggestions = dashboard.models.Suggestion.objects.filter(creatorID_id=user_id).order_by('-dateIssued', '-timeIssued', 'title')
    allCategory = dashboard.models.SuggestionType.objects.all().order_by('name')

    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    if request.method == 'POST':
        # print("hi POST")
        if request.is_ajax():
            if request.POST['requestType'] == 'updateStatus':
                # print("hi POST ajax updateStatus") # Test
                newStatus = request.POST['newStatus']
                suggestionID = request.POST['suggestionID']

                # print("newStatus: " + newStatus) #Test
                # print("suggestionID: " + str(suggestionID)) #Test

                currentSuggestion = dashboard.models.Suggestion.objects.get(id=suggestionID)
                currentSuggestion.status = newStatus
                currentSuggestion.save()

                context = {
                    'doneUpdateStatus': "Yes"
                }

                return JsonResponse(context)
    else:      
        if request.is_ajax():
            cat_selected = request.GET.get('cat_selected', None)

            if cat_selected != 'Semua':
                for category in allCategory:
                    if category.name == cat_selected:
                        allSuggestions = allSuggestions.filter(typeID_id=category.id)
            
            context = {
                'statusList': statusList,
                'allSuggestions': allSuggestions,
                'allCategory': allCategory
            }

            return render(request, 'dashboard/nonAdminSuggestionsContent.html', context)
        else:
            if user_type == "pelajar" and 'S' in user_id:
                dashboardNav = " Pelajar"
            elif user_type == "penjaga" and 'P' in user_id:
                dashboardNav = " Penjaga"
            elif user_type == "guru" and 'T' in user_id:
                dashboardNav = " Guru"
                
            context = {
                'dashboardNav': dashboardNav,
                'user_type': user_type,
                'user_id': user_id,
                'username': username,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard':urlDashboard,
                'logout': urlLogout,
                'settings': urlProfile,
                'bookmark': urlBookmark,
                'report': urlReport,
                'chat': urlChat,
                'suggestions': urlSuggestion,
                'statusList': statusList,
                'allSuggestions': allSuggestions,
                'allCategory': allCategory,
                'allNotif': allNotif,
                'unreadNotifCnt': unreadNotifCnt
            } 
            return render(request, 'dashboard/nonAdminSuggestions.html', context)

def addSuggestion(request, user_type, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    username = userRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'

    urlProfile = 'dashboard:profile-settings'
    urlBookmark = 'dashboard:bookmark'
    urlReport = 'dashboard:report'
    # urlChat = 'dashboard:chat-nonadmin'
    urlChat = 'dashboard:chat'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    allNotif = dashboard.models.Notification.objects.filter(recipientID_id=user_id).order_by('-id')
    unreadNotifCnt = allNotif.filter(isOpen=False).count()

    if request.method == 'POST':
        form = AddSuggestionForm(request.POST)
        if form.is_valid():
            filledList = form.cleaned_data
            filledSubject = filledList['subject']
            filledCategory = filledList['category']
            filledContent = filledList['content']

            # print("filledSubject: " + filledSubject) #Test
            # print("filledCategory is String?: " + str(isinstance(filledCategory, str))) #Test
            # print("filledCategory: " + filledCategory) #Test
            # print("filledContent: " + filledContent) #Test

            newSuggestion = dashboard.models.Suggestion.objects.create(creatorID_id=user_id, typeID_id=int(filledCategory), dateUpdated=datetime.now().date(), timeUpdated=datetime.now().time(), title=filledSubject, subjectContent=filledContent, status='Dihantar')
            newSuggestion.dateUpdated = newSuggestion.dateIssued
            newSuggestion.timeUpdated = newSuggestion.timeIssued
            newSuggestion.save()

            #create notification (Type id 4 - New suggestion (for admin ONLY))
            dashboard.models.Notification.objects.create(senderID_id=newSuggestion.creatorID_id, recipientID_id='A1', suggestionID_id=newSuggestion.id, typeID_id=4)

            return redirect('dashboard:suggestions-nonadmin', user_type, user_id)
    else:
        form = AddSuggestionForm()

        if user_type == "pelajar" and 'S' in user_id:
            dashboardNav = " Pelajar"
        elif user_type == "penjaga" and 'P' in user_id:
            dashboardNav = " Penjaga"
        elif user_type == "guru" and 'T' in user_id:
            dashboardNav = " Guru"
            
        context = {
            'dashboardNav': dashboardNav,
            'user_type': user_type,
            'user_id': user_id,
            'username': username,
            'test': urlTest,
            'blog': urlBlog,
            'quiz': urlQuiz,
            'search': urlSearch,
            'dashboard':urlDashboard,
            'logout': urlLogout,
            'settings': urlProfile,
            'bookmark': urlBookmark,
            'report': urlReport,
            'chat': urlChat,
            'suggestions': urlSuggestion,
            'form': form,
            'allNotif': allNotif,
            'unreadNotifCnt': unreadNotifCnt
        } 
        return render(request, 'dashboard/addSuggestion.html', context)

def logoutConfirm(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    username = currentUserRecord.username
    context = {'username': username, 'user_id': user_id}
    return render(request, 'dashboard\logoutConfirm.html', context)

def loggingOut(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
    currentUserRecord.isActive = False
    currentUserRecord.save()
    response = "Jumpa lagi! Ke halaman utama dalam 3, 2, 1... "
    return render(request, 'dashboard\loggingOut.html', {'response': response})