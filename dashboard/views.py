from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse, response
from .forms import ChangePasswordForm, EditProfileStudentForm, EditProfileParentForm, EditProfileTeacherForm
import dashboard.models
import string, re

# Create your views here.
def dashboardMain(request, user_type, user_id):
    #response = "Hai! Anda berada di "
    userRecord = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')
        #login_warn =  "Sila log masuk terlebih dahulu."
        #context = {'login_warn': login_warn}
        #return render(request, 'home/loginIndex.html', context)

    username = userRecord.username
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
        dashboardNav = " Pelajar"
        urlProfile = 'dashboard:profile-settings-nonadmin' #same view for any nonadmin user (display setting)
        urlBookmark = 'dashboard:bookmarks' #same view for any nonadmin user (display bookmark list)
        urlReport = 'dashboard:reports-student' #so far i think report have diff view for every nonadmin type (student view and download, parent view childrens', homeroom teacher can filter, view, dl)
        urlChat = 'dashboard:chat-student' #tbc same view or not, if yes, omit 'student' use same url pattern for all nonadmin
        urlSuggestion = 'dashboard:suggestions-nonadmin' #same view for any nonadmin user (display suggestion list)
        context = {'dashboardNav': dashboardNav, 'user_type': user_type, 'user_id': user_id, 'username': username,
        'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout, 'profile': urlProfile,
        'bookmark': urlBookmark, 'report': urlReport, 'chat': urlChat, 'suggestion': urlSuggestion} 
        return render(request, 'dashboard/dashboardIndex.html', context)
    elif user_type == "penjaga" and 'P' in user_id:
        dashboardNav = " Penjaga"
        urlProfile = 'dashboard:profile-settings-nonadmin'
        urlBookmark = 'dashboard:bookmarks'
        urlReport = 'dashboard:reports-parent'
        urlChat = 'dashboard:chat-parent'
        urlSuggestion = 'dashboard:suggestions-nonadmin'
        context = {'dashboardNav': dashboardNav, 'user_type': user_type, 'user_id': user_id, 'username': username,
        'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout, 'profile': urlProfile,
        'bookmark': urlBookmark, 'report': urlReport, 'chat': urlChat, 'suggestion': urlSuggestion} 
        return render(request, 'dashboard\dashboardIndex.html', context)
    elif user_type == "guru" and 'T' in user_id:
        dashboardNav = " Guru"
        urlProfile = 'dashboard:profile-settings-nonadmin'
        urlBookmark = 'dashboard:bookmarks'
        urlReport = 'dashboard:reports-teacher'
        urlChat = 'dashboard:chat-teacher'
        urlSuggestion = 'dashboard:suggestions-nonadmin'
        context = {'dashboardNav': dashboardNav, 'user_type': user_type, 'user_id': user_id, 'username': username,
        'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout, 'profile': urlProfile,
        'bookmark': urlBookmark, 'report': urlReport, 'chat': urlChat, 'suggestion': urlSuggestion} 
        return render(request, 'dashboard\dashboardIndex.html', context)
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
        context = {'dashboardNav': dashboardNav, 'response': response, 'user_type': user_type, 'user_id': user_id,
        'username': username, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout}
        #context = {'title': title, 'response': response, 'nonadmin_id': user_id}
        return render(request, 'dashboard\dashboardIndexNonAdminError.html', context)

def dashboardMainAdmin(request, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)
    
    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'dashboard:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    if user_id == 'A1': #betul ni admin, render dashboard index admin
        #response = "Hai! Anda berada di "
        context = {'admin_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
        'dashboard':urlDashboard, 'logout': urlLogout}
        return render(request, 'dashboard\dashboardIndexAdmin.html', context)
    else: #url jadi admin/Sx @ Tx @ Px - manual enter
        response = "Halaman ini hanya boleh diakses oleh admin."
        #pass url navbar admin to error template
        context = {'response': response, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
        'dashboard':urlDashboard, 'logout': urlLogout}
        return render(request, 'dashboard\dashboardIndexAdminError.html', context)

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

#profile settings - show current details
"""
def showProfile(request, user_id):
    response = "Profil Akaun Pengguna %s"
    return HttpResponse(response % user_id)
"""

"""
def showProfileAdmin(request, user_id):
    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'dashboard:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    if user_id == 'A1': 
        adminDetail = dashboard.models.Admin.objects.get(ID=user_id)
        response = "Profil Akaun Admin %s: %s" 
        return HttpResponse(response % (user_id, adminDetail.ID.username))
    else: #bukan admin
        title = "Future Cruise: Tetapan Akaun Admin"
        response = "Halaman ini hanya boleh diakses oleh admin."
        #pass url navbar admin to error template
        context = {'title': title, 'response': response, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
        'dashboard':urlDashboard, 'logout': urlLogout}
        return render(request, 'dashboard\dashboardIndexAdminError.html', context)
"""

#test try cuba untuk guna multiple user group, diff render html
def showProfileNonAdmin(request, user_type, user_id):
    userRecord = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if userRecord.isActive == False:
        return redirect('home:login')

    username = userRecord.username
    urlTest = 'dashboard:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
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
        response = "Profil Pelajar"
        #response = "User ID: " + user_id + " student class: " + studentDetail.studentClass.className #test
        context = {'title': title, 'dashboardNav': dashboardNav, 'userDetail': studentDetail, 'response': response, 'user_id': user_id, 'user_type': user_type,
        'username': username, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
        'dashboard':urlDashboard, 'logout': urlLogout}
        #return HttpResponse(response)
        return render(request, 'dashboard\showProfile.html', context)
    elif user_type == 'penjaga' and 'P' in user_id:
        title = " Tetapan Akaun Penjaga"
        dashboardNav = " Penjaga"
        parentDetail = dashboard.models.Parent.objects.get(ID=user_id)
        studentDetailQuery = dashboard.models.Student.objects.filter(parentID=parentDetail).order_by('name')
        response = "Profil Penjaga"
        context = {'title': title, 'dashboardNav': dashboardNav, 'userDetail': parentDetail, 'studentDetail': studentDetailQuery, 'response': response, 'user_id': user_id,
        'user_type': user_type, 'username': username, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
        'dashboard':urlDashboard, 'logout': urlLogout} 
        #return HttpResponse(response)
        return render(request, 'dashboard\showProfile.html', context)
    elif user_type == 'guru' and 'T' in user_id:
        title = " Tetapan Akaun Guru"
        dashboardNav = " Guru"
        response = "Profil Guru"
        teacherDetail = dashboard.models.Teacher.objects.get(ID=user_id)
        if teacherDetail.role == "Guru Kelas":
            homeroomDetail = dashboard.models.HomeroomTeacherClass.objects.get(teacherID=teacherDetail)
            studentDetailQuery = dashboard.models.Student.objects.filter(studentClass=homeroomDetail.className)
            context = {'title': title,'dashboardNav': dashboardNav, 'userDetail': teacherDetail,
            'studentDetail': studentDetailQuery, 'response': response, 'user_id': user_id, 'user_type': user_type,
            'username': username, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard,
            'logout': urlLogout}
        else:
            context = {'title': title,'dashboardNav': dashboardNav, 'userDetail': teacherDetail,
            'response': response, 'user_id': user_id, 'user_type': user_type, 'username': username, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
            'dashboard':urlDashboard, 'logout': urlLogout}
        #return HttpResponse(response % (user_id, teacherDetail))
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
    urlTest = 'dashboard:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    subtitle = "Tukar Kata Laluan" #h2 tag

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
        context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'user_id': user_id, 'user_type': user_type, 
        'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
        'subtitle': subtitle, 'errorMessage': errorMessage, 'form': form}
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
            if filledList['currentPass'] == currentUserTypeDetail.password:
                #if first and second entered password is the same
                if filledList['newPass'] == filledList['newPassConfirm']:
                    #if entered password length is 10
                    if len(filledList['newPass']) == 10:
                        #if has at least 1 upper, lower, special and number characters
                        if checkChar(filledList['newPass']) == True:
                            #update password in that usertype's table record for the entered email
                            currentUserTypeDetail.password = filledList['newPassConfirm']
                            currentUserTypeDetail.save()   
                            #render successUpdate.html - with context for navbar, title, subtitle,
                            #successmsg, variable for views url in template
                            successMessage = "Kata laluan berjaya dikemaskini!"
                            context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'user_id': user_id, 'user_type': user_type, 
                            'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
                            'subtitle': subtitle, 'successMessage': successMessage}
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

    context = {'title': title,'dashboardNav': dashboardNav, 'username': username, 'user_id': user_id, 'user_type': user_type,
    'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
    'subtitle': subtitle, 'form': form}
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
    urlTest = 'dashboard:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    subtitle = "Kemaskini Profil" #h2 tag

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
                context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'user_id': user_id, 'user_type': user_type, 
                'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
                'subtitle': subtitle, 'successMessage': successMessage}
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
                context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'user_id': user_id, 'user_type': user_type, 
                'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
                'subtitle': subtitle, 'successMessage': successMessage}
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
                            currentHTCforUserDetail.save()
                        currentUserTypeDetail.homeroomClass = 'NA'
                        currentUserTypeDetail.year = filledList['year'] #tak kisah tukar year tak sebab nak keluar dah lepas if ni
                        currentUserTypeDetail.save()
                        response = 'Profil berjaya dikemaskini!'
                        return HttpResponse(response)
                #if new/unchanged role = Guru Kelas #MEMANG GURU KElAS or NEW GURU KELAS
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
                                currentHTCforUserDetail.save()
                            #change teacherID in HTC to current user_id and SAVE (apply for both changed year or not)
                            #change role prev guru kelas (in Teacher table) to "NA"
                            #change homeroomClass of prev guru kelas to "NA" and SAVE record prev teacher
                            currentHTCforClassDetail.teacherID = currentUserTypeDetail
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
                                currentHTCforUserDetail.save()
                                #response = str(NATeacherDetail) + ",,, " + str(currentHTCforUserDetail)
                                #return HttpResponse(response)
                            #change teacherID in HTC from "NA" to current user_id and SAVE (apply for changed year or not)
                            #currentTeacherUserDetail = dashboard.models.User.objects.get(ID=user_id)
                            #currentTeacherDetail = dashboard.models.Teacher.objects.get(ID=currentTeacherUserDetail)
                            currentHTCforClassDetail.teacherID = currentUserTypeDetail
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
                    #render successpage
                    #response = 'Profil berjaya dikemaskini!'
                    #return HttpResponse(response)
                    #render successUpdate.html - with context for navbar, title, subtitle,
                    #successmsg, variable for views url in template
                    successMessage = "Profil berjaya dikemaskini!"
                    context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'user_id': user_id, 'user_type': user_type, 
                    'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
                    'subtitle': subtitle, 'successMessage': successMessage}
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
                    context = {'title': title,'dashboardNav': dashboardNav, 'username': username, 'user_id': user_id, 'user_type': user_type,
                    'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
                    'subtitle': subtitle, 'errorMessage': errorMessage,'form': form}
                    return render(request, 'dashboard/editProfile.html', context)

                #render successUpdate.html - with context for navbar, title, subtitle,
                #successmsg, variable for views url in template
                successMessage = "Profil berjaya dikemaskini!"
                context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'user_id': user_id, 'user_type': user_type, 
                'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
                'subtitle': subtitle, 'successMessage': successMessage}
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

    context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'user_type': user_type, 'user_id': user_id,
    'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
    'subtitle': subtitle, 'form': form}
    return render(request, 'dashboard/editProfile.html', context)


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