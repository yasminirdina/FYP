from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from .forms import LoginFormAdmin, LoginFormNonAdmin, ResetPasswordForm, SignUpForm
import dashboard.models
import string
import re

# Create your views here.
def futureCruiseMain(request):
    #return HttpResponse("Selamat Datang ke Future Cruise: Portal Web Penerokaan Kerjaya bagi Pelajar Sekolah Menengah!")
    response = "Selamat Datang ke Future Cruise: Portal Web Penerokaan Kerjaya bagi Pelajar Sekolah Menengah!"
    return render(request, 'home/homeIndex.html', {'response': response})

def login(request):
    return render(request, 'home/loginIndex.html')

def signUp(request):
    filledList = {}

    def checkEmailExist(filledList):
        checkExistAllType = [False, False, False] #Student table, Parent, Teacher
        if filledList['email'] in list(dashboard.models.Student.objects.values_list('email', flat=True)):
            checkExistAllType[0] = True
        elif filledList['email'] in list(dashboard.models.Parent.objects.values_list('email', flat=True)):
            checkExistAllType[1] = True
        elif filledList['email'] in list(dashboard.models.Teacher.objects.values_list('email', flat=True)):
            checkExistAllType[2] = True
        return checkExistAllType

    def checkUsernameExistSpecificType(filledList):
        if filledList['userType'] == 'Student':
            StudentInUserRecord = dashboard.models.User.objects.filter(ID__startswith='S') #returns queryset
            if filledList['username'] in list(StudentInUserRecord.values_list('username', flat=True)):
                return True
        if filledList['userType'] == 'Parent':
            ParentInUserRecord = dashboard.models.User.objects.filter(ID__startswith='P') #returns queryset
            if filledList['username'] in list(ParentInUserRecord.values_list('username', flat=True)):
                return True
        if filledList['userType'] == 'Teacher':
            TeacherInUserRecord = dashboard.models.User.objects.filter(ID__startswith='T') #returns queryset
            if filledList['username'] in list(TeacherInUserRecord.values_list('username', flat=True)):
                return True

    def getLatestSpecificUserTypeID(AllUserTypeAInUserIDList):
        length = len(AllUserTypeAInUserIDList)
        latestID = AllUserTypeAInUserIDList[length-1]
        latestID_no = ""
        for i in range(1, len(latestID)):
            latestID_no += latestID[i]
        return int(latestID_no)

    def checkEmailFormat(email):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if(re.search(regex, email)):
            return True
        else:
            return False

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

    def errorMessageEmailInUse(request, form):
        #redirect to refreshed form with error message on top
        response = "Alamat emel yang anda masukkan telah digunakan."
        context = {'response': response, 'form': form}
        return render(request, 'home/signUp.html', context)

    def errorMessageEmailFormat(request, form):
        #redirect to refreshed form with error message on top
        response = "Alamat emel yang anda masukkan adalah tidak sah."
        context = {'response': response, 'form': form}
        return render(request, 'home/signUp.html', context)

    def errorMessageUsernameInUse(request, form):
        #redirect to refreshed form with error message on top
        response = "Nama panggilan yang anda masukkan telah digunakan."
        context = {'response': response, 'form': form}
        return render(request, 'home/signUp.html', context)

    def errorMessagePasswordTooShort(request, form):
        #redirect to refreshed form with error message on top
        response = "Kata laluan anda terlalu pendek."
        context = {'response': response, 'form': form}
        return render(request, 'home/signUp.html', context)

    def errorMessagePasswordFormat(request, form):
        #redirect to refreshed form with error message on top
        response = "Kata laluan mestilah mengandungi huruf besar, huruf kecil, angka dan aksara khas."
        context = {'response': response, 'form': form}
        return render(request, 'home/signUp.html', context)
    
    def errorTypeNotChosen(request, form):
        #redirect to refreshed form with error message on top
        response = "Anda wajib memilih jenis pengguna."
        context = {'response': response, 'form': form}
        return render(request, 'home/signUp.html', context)

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            filledList = form.cleaned_data
            #if a student
            if filledList['userType'] == 'Student':
                #if True is in Student table (have same email already in Student table)
                if True in checkEmailExist(filledList):
                    #display error message email already exist
                    form = SignUpForm()
                    return errorMessageEmailInUse(request, form)
                #if email format is not correct
                elif checkEmailFormat(filledList['email']) == False:
                    form = SignUpForm()
                    return errorMessageEmailFormat(request, form)
                #email available for use (is not existing, format is correct)
                elif True not in checkEmailExist(filledList) and checkEmailFormat(filledList['email']) == True:
                    #if entered username already exist in User table for all Students
                    if checkUsernameExistSpecificType(filledList) == True:
                        return errorMessageUsernameInUse(request, form)
                    #username available for use
                    else: 
                        #if entered password length is 10
                        if len(filledList['password']) == 10:
                            #if has at least 1 upper, lower, special and number characters
                            if checkChar(filledList['password']) == True:
                                #get all Student in User
                                AllStudentInUser = dashboard.models.User.objects.filter(ID__startswith='S').order_by('ID') #returns queryset
                                #get list of all student ID in User
                                AllStudentInUserIDList = list(AllStudentInUser.values_list('ID', flat=True))
                                newStudentID = "" #default
                                #if its the first Student registering (no Student in User yet)
                                if len(AllStudentInUserIDList) == 0:
                                    newStudentID = "S1" #first Student ID given
                                #already have other existing Student in User
                                else:
                                    #get new student ID (digit part), by getting latest ID digit, assign to new var and + 1
                                    newStudentID_no = getLatestSpecificUserTypeID(AllStudentInUserIDList) + 1
                                    newStudentID = "S" + str(newStudentID_no) #with 'S' for student
                                #create new User with new student ID    
                                dashboard.models.User.objects.create(ID=newStudentID, studentID=newStudentID, username=filledList['username'], isActive=False)
                                #create new Student with new Student ID after getting the newly added Student in User 
                                newStudentUserRecord = dashboard.models.User.objects.get(ID=newStudentID)
                                dashboard.models.Student.objects.create(ID=newStudentUserRecord, email=filledList['email'], password=filledList['password'])
                                #go to dashboard main page
                                #return redirect('dashboard:index', newStudentID)
                                #go to login page
                                #return redirect('home:login-nonadmin')
                                signUpSuccess = "Pendaftaran akaun berjaya. Sila log masuk ke akaun anda."
                                form = LoginFormNonAdmin()
                                context = {'success': signUpSuccess, 'form': form}
                                return render(request, 'home/loginNonAdmin.html', context) 
                            #if either has no upper/lower/special/number characters
                            else:
                                return errorMessagePasswordFormat(request, form)
                        #if entered password length is not 10
                        else:
                            return errorMessagePasswordTooShort(request, form)
            #if a parent
            elif filledList['userType'] == 'Parent':
                #if True is in Parent table (have same email already in Parent table)
                if True in checkEmailExist(filledList):
                    #display error message email already exist
                    form = SignUpForm()
                    return errorMessageEmailInUse(request, form)
                #if email format is not correct
                elif checkEmailFormat(filledList['email']) == False:
                    form = SignUpForm()
                    return errorMessageEmailFormat(request, form)
                #email available for use (is not existing, format is correct)
                elif True not in checkEmailExist(filledList) and checkEmailFormat(filledList['email']) == True:
                    #if entered username already exist in User table for all Parents
                    if checkUsernameExistSpecificType(filledList) == True:
                        return errorMessageUsernameInUse(request, form)
                    #username available for use
                    else: 
                        #if entered password length is 10
                        if len(filledList['password']) == 10:
                            #if has at least 1 upper, lower, special and number characters
                            if checkChar(filledList['password']) == True:
                                #get all Parent in User
                                AllParentInUser = dashboard.models.User.objects.filter(ID__startswith='P').order_by('ID') #returns queryset
                                #get list of all parent ID in User
                                AllParentInUserIDList = list(AllParentInUser.values_list('ID', flat=True))
                                newParentID = "" #default
                                #if its the first Parent registering (no Parent in User yet)
                                if len(AllParentInUserIDList) == 0:
                                    newParentID = "P1" #first Parent ID given
                                #already have other existing Parent in User
                                else:
                                    #get new parent ID (digit part), by getting latest ID digit, assign to new var and + 1
                                    newParentID_no = getLatestSpecificUserTypeID(AllParentInUserIDList) + 1
                                    newParentID = "P" + str(newParentID_no) #with 'P' for parent
                                #create new User with new parent ID    
                                dashboard.models.User.objects.create(ID=newParentID, parentID=newParentID, username=filledList['username'], isActive=False)
                                #create new Parent with new Parent ID after getting the newly added Parent in User 
                                newParentUserRecord = dashboard.models.User.objects.get(ID=newParentID)
                                dashboard.models.Parent.objects.create(ID=newParentUserRecord, email=filledList['email'], password=filledList['password'])
                                #go to dashboard main page
                                #return redirect('dashboard:index', newParentID)
                                #go to login page
                                #return redirect('home:login-nonadmin')
                                signUpSuccess = "Pendaftaran akaun berjaya. Sila log masuk ke akaun anda."
                                form = LoginFormNonAdmin()
                                context = {'success': signUpSuccess, 'form': form}
                                return render(request, 'home/loginNonAdmin.html', context)
                            #if either has no upper/lower/special/number characters
                            else:
                                return errorMessagePasswordFormat(request, form)
                        #if entered password length is not 10
                        else:
                            return errorMessagePasswordTooShort(request, form)
            #if a teacher
            elif filledList['userType'] == 'Teacher':
                #if True is in Teacher table (have same email already in Teacher table)
                if True in checkEmailExist(filledList):
                    #display error message email already exist
                    form = SignUpForm()
                    return errorMessageEmailInUse(request, form)
                #if email format is not correct
                elif checkEmailFormat(filledList['email']) == False:
                    form = SignUpForm()
                    return errorMessageEmailFormat(request, form)
                #email available for use (is not existing, format is correct)
                elif True not in checkEmailExist(filledList) and checkEmailFormat(filledList['email']) == True:
                    #if entered username already exist in User table for all Teachers
                    if checkUsernameExistSpecificType(filledList) == True:
                        return errorMessageUsernameInUse(request, form)
                    #username available for use
                    else: 
                        #if entered password length is 10
                        if len(filledList['password']) == 10:
                            #if has at least 1 upper, lower, special and number characters
                            if checkChar(filledList['password']) == True:
                                #get all Teacher in User
                                AllTeacherInUser = dashboard.models.User.objects.filter(ID__startswith='T').order_by('ID') #returns queryset
                                #get list of all teacher ID in User
                                AllTeacherInUserIDList = list(AllTeacherInUser.values_list('ID', flat=True))
                                newTeacherID = "" #default
                                #if its the first Teacher registering (no Teacher in User yet)
                                if len(AllTeacherInUserIDList) == 0:
                                    newTeacherID = "T1" #first Teacher ID given
                                #already have other existing Teacher in User
                                else:
                                    #get new teacher ID (digit part), by getting latest ID digit, assign to new var and + 1
                                    newTeacherID_no = getLatestSpecificUserTypeID(AllTeacherInUserIDList) + 1
                                    newTeacherID = "T" + str(newTeacherID_no) #with 'T' for teacher
                                #create new User with new teacher ID    
                                dashboard.models.User.objects.create(ID=newTeacherID, teacherID=newTeacherID, username=filledList['username'], isActive=False)
                                #create new Teacher with new Teacher ID after getting the newly added Teacher in User 
                                newTeacherUserRecord = dashboard.models.User.objects.get(ID=newTeacherID)
                                dashboard.models.Teacher.objects.create(ID=newTeacherUserRecord, email=filledList['email'], password=filledList['password'])
                                #go to dashboard main page
                                #return redirect('dashboard:index', newTeacherID)
                                #go to login page
                                signUpSuccess = "Pendaftaran akaun berjaya. Sila log masuk ke akaun anda."
                                form = LoginFormNonAdmin()
                                context = {'success': signUpSuccess, 'form': form}
                                return render(request, 'home/loginNonAdmin.html', context)
                            #if either has no upper/lower/special/number characters
                            else:
                                return errorMessagePasswordFormat(request, form)
                        #if entered password length is not 10
                        else:
                            return errorMessagePasswordTooShort(request, form)                
            else:
                form = SignUpForm()
                return errorTypeNotChosen(request, form)
    else:
        form = SignUpForm()
    return render(request, 'home/signUp.html', {'form':form})

def loginAdmin(request):
    UserRecord = dashboard.models.User.objects.get(ID="A1")
    AdminRecord = dashboard.models.Admin.objects.get(ID="A1")

    def errorMessageUsername(request, form):
        #redirect to refreshed form with error message on top
        response = "Nama pengguna yang anda masukkan adalah tidak sah."
        context = {'response': response, 'form': form}
        return render(request, 'home/loginAdmin.html', context)

    def errorMessagePassword(request, form):
        #redirect to refreshed form with error message on top
        response = "Kata laluan yang anda masukkan adalah tidak sah."
        context = {'response': response, 'form': form}
        return render(request, 'home/loginAdmin.html', context)

    if request.method == 'POST':
        form = LoginFormAdmin(request.POST)
        if form.is_valid():
            filledList = form.cleaned_data
            #if entered username matches username in Admin table
            if filledList['username'] == UserRecord.username:
                #if entered password matches password in Admin table
                if filledList['password'] == AdminRecord.password:
                    UserRecord.isActive = True
                    UserRecord.save()
                    admin_id = 'A1'
                    #return redirect('dashboard:index', "A1")
                    return redirect('dashboard:index-admin', admin_id)
                #wrong password entered
                else:
                    return errorMessagePassword(request, form)
            #if entered username do not match with username in Admin table
            else:
                form = LoginFormAdmin()
                return errorMessageUsername(request, form)
    else:
        form = LoginFormAdmin()

    return render(request, 'home/loginAdmin.html', {'form': form})

def loginNonAdmin(request):
    filledList = {}
    def getEmailList(filledList):
        emailList = {}
        if filledList['userType'] == 'Student':
            emailList = list(dashboard.models.Student.objects.values_list('email', flat=True))
            return emailList
        elif filledList['userType'] == 'Parent':
            emailList = list(dashboard.models.Parent.objects.values_list('email', flat=True))
            return emailList
        elif filledList['userType'] == 'Teacher':
            emailList = list(dashboard.models.Teacher.objects.values_list('email', flat=True))
            return emailList
        
    def getCurrentUserTypeRecord(filledList):
        if filledList['userType'] == 'Student':
            currentUserTypeRecord = dashboard.models.Student.objects.get(email=filledList['email'])
            return currentUserTypeRecord
        elif filledList['userType'] == 'Parent':
            currentUserTypeRecord = dashboard.models.Parent.objects.get(email=filledList['email'])
            return currentUserTypeRecord
        elif filledList['userType'] == 'Teacher':
            currentUserTypeRecord = dashboard.models.Teacher.objects.get(email=filledList['email'])
            return currentUserTypeRecord

    def getUserRecord(currentUserTypeRecord):
        userRecord = dashboard.models.User.objects.get(ID=currentUserTypeRecord.ID.ID)
        userRecord.isActive = True
        userRecord.save()
        return userRecord
        
    def errorMessagePassword(request, form):
        #redirect to refreshed form with error message on top
        response = "Kata laluan yang anda masukkan adalah tidak tepat."
        context = {'response': response, 'form': form}
        return render(request, 'home/loginNonAdmin.html', context)
            
    def errorMessageEmail(request, form):
        #redirect to refreshed form with error message on top
        response = "Maklumat yang anda masukkan adalah tidak tepat."
        context = {'response': response, 'form': form}
        return render(request, 'home/loginNonAdmin.html', context)
            
    if request.method == 'POST':
        form = LoginFormNonAdmin(request.POST)
        if form.is_valid():
            filledList = form.cleaned_data
            #2nd way
            #if a student
            if filledList['userType'] == 'Student':
                #if entered email is in email column in Student table
                if filledList['email'] in getEmailList(filledList):
                    #get that Student record (object)
                    StudentRecord = getCurrentUserTypeRecord(filledList)
                    #if entered password = the Student record's password
                    if filledList['password'] == StudentRecord.password:
                        UserRecord = getUserRecord(StudentRecord)
                        #response = "Anda berjaya log masuk! Nama pelajar: %s. Status pelajar: Online"
                        #context = {'response': response % StudentRecord.name, 'user_id': UserRecord.ID}
                        #return redirect('dashboard:index', UserRecord.ID)
                        return redirect('dashboard:index-nonadmin', 'pelajar', UserRecord.ID)
                    #entered password not match with Student record's password
                    else:
                        return errorMessagePassword(request, form)
                #entered email does not exist in email column in Student table
                else:
                    form = LoginFormNonAdmin()
                    return errorMessageEmail(request, form)
            #if a parent
            elif filledList['userType'] == 'Parent':
                #if entered email is in email column in Parent table
                if filledList['email'] in getEmailList(filledList):
                    #get that Parent record (object)
                    ParentRecord = getCurrentUserTypeRecord(filledList)
                    #if entered password = the Parent record's password
                    if filledList['password'] == ParentRecord.password:
                        UserRecord = getUserRecord(ParentRecord)
                        #response = "Anda berjaya log masuk! Nama penjaga: %s. Status penjaga: Online"
                        #context = {'response': response % ParentRecord.name, 'user_id': UserRecord.ID}
                        #return redirect('dashboard:index', UserRecord.ID)
                        return redirect('dashboard:index-nonadmin', 'penjaga', UserRecord.ID)
                    #entered password not match with Parent record's password
                    else:
                        return errorMessagePassword(request, form)
                #entered email does not exist in email column in Parent table
                else:
                    form = LoginFormNonAdmin()
                    return errorMessageEmail(request, form)
            #if a teacher
            elif filledList['userType'] == 'Teacher':
                #if entered email is in email column in Teacher table
                if filledList['email'] in getEmailList(filledList):
                    #get that Teacher record (object)
                    TeacherRecord = getCurrentUserTypeRecord(filledList)
                    #if entered password = the Teacher record's password
                    if filledList['password'] == TeacherRecord.password:
                        UserRecord = getUserRecord(TeacherRecord)
                        #response = "Anda berjaya log masuk! Nama guru: %s. Status guru: Online"
                        #context = {'response': response % TeacherRecord.name, 'user_id': UserRecord.ID}
                        #return redirect('dashboard:index', UserRecord.ID)
                        return redirect('dashboard:index-nonadmin', 'guru', UserRecord.ID)
                    #entered password not match with Teacher record's password
                    else:
                        return errorMessagePassword(request, form)
                #entered email does not exist in email column in Teacher table
                else:
                    form = LoginFormNonAdmin()
                    return errorMessageEmail(request, form)
            #else: #no matching password and email for any of the non-admin users
            #    return HttpResponse("Form not valid.") #nanti ganti dengan redirect to page error(?)
    else:
        form = LoginFormNonAdmin()

    return render(request, 'home/loginNonAdmin.html', {'form': form})

def resetPassword(request):
    #for each type selected
    #if entered email exist in the selected user type table
        #baru proceed reset password
        #save in database
        #back to login page kosong
    #if no email match in selected user type OR in ANY user type table
        #error maklumat tak tepat
        #load empty page balik
    
    filledList = {}

    def getEmailList(filledList):
        emailList = {}
        if filledList['userType'] == 'Student':
            emailList = list(dashboard.models.Student.objects.values_list('email', flat=True))
            return emailList
        elif filledList['userType'] == 'Parent':
            emailList = list(dashboard.models.Parent.objects.values_list('email', flat=True))
            return emailList
        elif filledList['userType'] == 'Teacher':
            emailList = list(dashboard.models.Teacher.objects.values_list('email', flat=True))
            return emailList
            
    def errorMessage(request, form, response):
        #redirect to refreshed form with error message on top
        context = {'response': response, 'form': form}
        return render(request, 'home/resetPassword.html', context)

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
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            filledList = form.cleaned_data
            #if a student
            if filledList['userType'] == 'Student':
                #if entered email not exist in Student table, return empty form with error message
                if filledList['email'] not in getEmailList(filledList):
                    form = ResetPasswordForm()
                    response = "Maklumat yang anda masukkan adalah tidak tepat."
                    return errorMessage(request, form, response)
                #if entered email exist in Student table,
                else:
                    #if first and second entered password is the same
                    if filledList['newPass'] == filledList['newPassConfirm']:
                        #if entered password length is 10
                        if len(filledList['newPass']) == 10:
                            #if has at least 1 upper, lower, special and number characters
                            if checkChar(filledList['newPass']) == True:
                                #update password in Student record for the entered email
                                StudentRecord = dashboard.models.Student.objects.get(email=filledList['email'])
                                StudentRecord.password = filledList['newPassConfirm']
                                StudentRecord.save()   
                                #redirect to intermediary page which displays success message (not Django message)
                                #and after 3 seconds redirect to home:login-nonadmin   
                                return render(request, 'home/redirSuccess.html')
                            #if either has no upper/lower/special/number characters
                            else:
                                response = "Kata laluan mestilah mengandungi huruf besar, huruf kecil, angka dan aksara khas."
                                return errorMessage(request, form, response)
                        #if entered password length is not 10
                        else:
                            response = "Kata laluan anda terlalu pendek."
                            return errorMessage(request, form, response)
                    #if first and second entered password do not match
                    else:          
                        #display error passwords do not match
                        response = "Sila pastikan kedua-dua kata laluan adalah sama."
                        return errorMessage(request, form, response)
            #if a parent
            elif filledList['userType'] == 'Parent':
                #if entered email not exist in Parent table, return empty form with error message
                if filledList['email'] not in getEmailList(filledList):
                    form = ResetPasswordForm()
                    response = "Maklumat yang anda masukkan adalah tidak tepat."
                    return errorMessage(request, form, response)
                #if entered email exist in Parent table,
                else:
                    #if first and second entered password is the same
                    if filledList['newPass'] == filledList['newPassConfirm']:
                        #if entered password length is 10
                        if len(filledList['newPass']) == 10:
                            #if has at least 1 upper, lower, special and number characters
                            if checkChar(filledList['newPass']) == True:
                                #update password in Parentt record for the entered email
                                ParentRecord = dashboard.models.Parent.objects.get(email=filledList['email'])
                                ParentRecord.password = filledList['newPassConfirm']
                                ParentRecord.save()   
                                #redirect to intermediary page which displays success message (not Django message)
                                #and after 3 seconds redirect to home:login-nonadmin   
                                return render(request, 'home/redirSuccess.html')
                            #if either has no upper/lower/special/number characters
                            else:
                                response = "Kata laluan mestilah mengandungi huruf besar, huruf kecil, angka dan aksara khas."
                                return errorMessage(request, form, response)
                        #if entered password length is not 10
                        else:
                            response = "Kata laluan anda terlalu pendek."
                            return errorMessage(request, form, response)
                    #if first and second entered password do not match
                    else:          
                        #display error passwords do not match
                        response = "Sila pastikan kedua-dua kata laluan adalah sama."
                        return errorMessage(request, form, response) 
            #if a teacher
            elif filledList['userType'] == 'Teacher':
                #if entered email not exist in Teacher table, return empty form with error message
                if filledList['email'] not in getEmailList(filledList):
                    form = ResetPasswordForm()
                    response = "Maklumat yang anda masukkan adalah tidak tepat."
                    return errorMessage(request, form, response)
                #if entered email exist in Teacher table,
                else:
                    #if first and second entered password is the same
                    if filledList['newPass'] == filledList['newPassConfirm']:
                        #if entered password length is 10
                        if len(filledList['newPass']) == 10:
                            #if has at least 1 upper, lower, special and number characters
                            if checkChar(filledList['newPass']) == True:
                                #update password in Teacher record for the entered email
                                TeacherRecord = dashboard.models.Teacher.objects.get(email=filledList['email'])
                                TeacherRecord.password = filledList['newPassConfirm']
                                TeacherRecord.save()   
                                #redirect to intermediary page which displays success message (not Django message)
                                #and after 3 seconds redirect to home:login-nonadmin   
                                return render(request, 'home/redirSuccess.html')
                            #if either has no upper/lower/special/number characters
                            else:
                                response = "Kata laluan mestilah mengandungi huruf besar, huruf kecil, angka dan aksara khas."
                                return errorMessage(request, form, response)
                        #if entered password length is not 10
                        else:
                            response = "Kata laluan anda terlalu pendek."
                            return errorMessage(request, form, response)
                    #if first and second entered password do not match
                    else:          
                        #display error passwords do not match
                        response = "Sila pastikan kedua-dua kata laluan adalah sama."
                        return errorMessage(request, form, response)                          
    else: 
        form = ResetPasswordForm()

    return render(request, 'home/resetPassword.html', {'form': form})