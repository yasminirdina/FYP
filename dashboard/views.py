from datetime import datetime
from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .forms import ChangePasswordForm, AddClassForm, EditProfileStudentForm, EditProfileParentForm, EditProfileTeacherForm
import dashboard.models
import string, re
from django.contrib.auth.hashers import make_password, check_password

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
    urlChat = 'dashboard:chat-admin'

    if user_id == 'A1': #betul ni admin, render dashboard index admin
        #response = "Hai! Anda berada di "
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
            'chat': urlChat
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
    urlChat = 'dashboard:chat-admin'

    allClass = dashboard.models.HomeroomTeacherClass.objects.exclude(className='NA').order_by('className')

    if request.method == 'POST':
        print("hi POST")
        if request.is_ajax():
            if request.POST['requestType'] == 'deleteClass':
                print("hi POST ajax deleteClass") # Test
                classToDelete = request.POST['className']

                print("classToDelete: " + classToDelete) #Test

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

                print("newClassCap: " + newClass.upper()) #Test

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
                        'form': form
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
                        'error': "Nama kelas yang dimasukkan telah wujud. Sila masukkan nama kelas yang lain."
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
            'form': form
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
    urlChat = 'dashboard:chat-admin'

    statusList = ['Dihantar', 'Sedang Diproses', 'Ditutup']
    allSuggestions = dashboard.models.Suggestion.objects.all().order_by('-dateIssued', '-timeIssued', 'title')
    allCategory = dashboard.models.SuggestionType.objects.all().order_by('name')

    if request.method == 'POST':
        print("hi POST")
        if request.is_ajax():
            if request.POST['requestType'] == 'updateStatus':
                print("hi POST ajax updateStatus") # Test
                newStatus = request.POST['newStatus']
                suggestionID = request.POST['suggestionID']

                print("newStatus: " + newStatus) #Test
                print("suggestionID: " + str(suggestionID)) #Test

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
                'allCategory': allCategory
            }

            return render(request, 'dashboard/adminSuggestions.html', context)

def adminChat(request, user_id):
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
    urlChat = 'dashboard:chat-admin'

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
        'chat': urlChat
    }

    return render(request, 'dashboard/adminChat.html', context)

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
    urlChat = 'dashboard:chat-nonadmin'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = " Pelajar"

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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminNotif.html', context)
    elif user_type == "penjaga" and 'P' in user_id:
        dashboardNav = " Penjaga"
        
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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminNotif.html', context)
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
            'suggestions': urlSuggestion
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
    urlChat = 'dashboard:chat-nonadmin'
    urlSuggestion = 'dashboard:suggestions-nonadmin'
    
    #if user_id is admin
        #response = admin id
        #get admin profile detail
        #render dashboard\showProfile.html pass context (response, profile detail) to display in html
    #if student
        #same as admin but change to student id
    #if parent
        #^^
    #if teacher
        #^^
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
            'suggestions': urlSuggestion
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
            'suggestions': urlSuggestion
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
                    'suggestions': urlSuggestion
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
                    'suggestions': urlSuggestion
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
                'suggestions': urlSuggestion
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
    urlChat = 'dashboard:chat-nonadmin'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

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
            'form': form
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
            print("filledpassraw: " + filledList['currentPass']) #Test
            print("filledpasshash: " + make_password(filledList['currentPass'])) #Test
            print("currentpassraw: " + currentUserTypeDetail.password) #Test
            print("currentpasshash: " + make_password(currentUserTypeDetail.password)) #Test
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
                                'successMessage': successMessage
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
        'form': form
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
    urlChat = 'dashboard:chat-nonadmin'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

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
                    'successMessage': successMessage
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
                    'successMessage': successMessage
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
                            'successMessage': successMessage
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
                        'successMessage': successMessage
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
                        'form': form
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
                    'successMessage': successMessage
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
        # 'errorMessage': errorMessage,
        'form': form
    }

    """ context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'user_type': user_type, 'user_id': user_id,
    'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
    'subtitle': subtitle, 'form': form} """
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
    urlChat = 'dashboard:chat-nonadmin'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = " Pelajar"

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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminBookmark.html', context)
    elif user_type == "penjaga" and 'P' in user_id:
        dashboardNav = " Penjaga"
        
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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminBookmark.html', context)
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
            'suggestions': urlSuggestion
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
    urlChat = 'dashboard:chat-nonadmin'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = " Pelajar"

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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminReport.html', context)
    elif user_type == "penjaga" and 'P' in user_id:
        dashboardNav = " Penjaga"
        
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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminReport.html', context)
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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminReport.html', context)

def nonAdminChat(request, user_type, user_id):
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
    urlChat = 'dashboard:chat-nonadmin'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = " Pelajar"

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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminChat.html', context)
    elif user_type == "penjaga" and 'P' in user_id:
        dashboardNav = " Penjaga"
        
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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminChat.html', context)
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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminChat.html', context)

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
    urlChat = 'dashboard:chat-nonadmin'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = " Pelajar"

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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminSuggestions.html', context)
    elif user_type == "penjaga" and 'P' in user_id:
        dashboardNav = " Penjaga"
        
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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/nonAdminSuggestions.html', context)
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
            'suggestions': urlSuggestion
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
    urlChat = 'dashboard:chat-nonadmin'
    urlSuggestion = 'dashboard:suggestions-nonadmin'

    if user_type == "pelajar" and 'S' in user_id:
        dashboardNav = " Pelajar"

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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/addSuggestion.html', context)
    elif user_type == "penjaga" and 'P' in user_id:
        dashboardNav = " Penjaga"
        
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
            'suggestions': urlSuggestion
        } 
        return render(request, 'dashboard/addSuggestion.html', context)
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
            'suggestions': urlSuggestion
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

#bookmarks
def showBookmarks(request, user_type, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    response = "Penanda Pengguna %s"
    return HttpResponse(response % user_id)

#reports
def showReports(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    response = "Laporan Visual Pengguna %s"
    return HttpResponse(response % user_id)

#chat
def showChat(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    response = "Ruang Mesej Pengguna %s bersama Guru Kaunseling"
    return HttpResponse(response % user_id)

#suggestions
def showSuggestionsNonAdmin(request, user_type, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    response = "%s, kongsikan cadangan penambahbaikan kandungan portal!"
    return HttpResponse(response % user_id)

def showSuggestionsAdmin(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    response = "Cadangan Penambahbaikan Kandungan Portal oleh Pengguna"
    return HttpResponse(response)

#notifications