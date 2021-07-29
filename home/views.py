from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from .forms import LoginFormAdmin, LoginFormNonAdmin, ResetPasswordFormA, ResetPasswordFormB, ResetPasswordFormC, SignUpForm
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
import dashboard.models, string, re, random, json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

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
        remainingTry = str(3 - request.session['countWrong'])
        response = "Kata laluan yang anda masukkan adalah tidak tepat. Baki cubaan yang tinggal: " + remainingTry + " kali."
        context = {'response': response, 'form': form}
        return render(request, 'home/loginNonAdmin.html', context)
            
    def errorMessageEmail(request, form):
        #redirect to refreshed form with error message on top
        response = "Maklumat yang anda masukkan adalah tidak tepat."
        context = {'response': response, 'form': form}
        return render(request, 'home/loginNonAdmin.html', context)
            
    initial={'countWrong': request.session.setdefault('countWrong', 0), 'afterFailedLoginMsg': request.session.get('afterFailedLoginMsg', "")}

    if request.method == 'POST':
        form = LoginFormNonAdmin(request.POST, initial=initial)
        if form.is_valid():
            filledList = form.cleaned_data
            #if a student
            if filledList['userType'] == 'Student':
                #if entered email is in email column in Student table
                if filledList['email'] in getEmailList(filledList):
                    #get that Student record (object)
                    StudentRecord = getCurrentUserTypeRecord(filledList)
                    #if entered password = the Student record's password
                    if filledList['password'] == StudentRecord.password:
                        request.session['countWrong'] = 0
                        UserRecord = getUserRecord(StudentRecord)
                        return redirect('dashboard:index-nonadmin', 'pelajar', UserRecord.ID)
                    #entered password not match with Student record's password
                    else:
                        request.session['countWrong'] += 1
                        if request.session['countWrong'] <= 2:
                            return errorMessagePassword(request, form)
                        else:
                            #request.session['countWrong'] = 0
                            request.session['afterFailedLoginMsg'] = "Anda telah memasukkan kata laluan yang salah sebanyak 3 kali. Sila kemaskini kata laluan anda."
                            return redirect('home:reset-pass')
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
                        request.session['countWrong'] = 0
                        UserRecord = getUserRecord(ParentRecord)
                        return redirect('dashboard:index-nonadmin', 'penjaga', UserRecord.ID)
                    #entered password not match with Parent record's password
                    else:
                        request.session['countWrong'] += 1
                        if request.session['countWrong'] <= 2:
                            return errorMessagePassword(request, form)
                        else:
                            #request.session['countWrong'] = 0
                            request.session['afterFailedLoginMsg'] = "Anda telah memasukkan kata laluan yang salah sebanyak 3 kali. Sila kemaskini kata laluan anda."
                            return redirect('home:reset-pass')
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
                        request.session['countWrong'] = 0
                        UserRecord = getUserRecord(TeacherRecord)
                        return redirect('dashboard:index-nonadmin', 'guru', UserRecord.ID)
                    #entered password not match with Teacher record's password
                    else:
                        request.session['countWrong'] += 1
                        if request.session['countWrong'] <= 2:
                            return errorMessagePassword(request, form)
                        else:
                            #request.session['countWrong'] = 0
                            request.session['afterFailedLoginMsg'] = "Anda telah memasukkan kata laluan yang salah sebanyak 3 kali. Sila kemaskini kata laluan anda."
                            return redirect('home:reset-pass')
                #entered email does not exist in email column in Teacher table
                else:
                    form = LoginFormNonAdmin()
                    return errorMessageEmail(request, form)
            #else: #no matching password and email for any of the non-admin users
            #    return HttpResponse("Form not valid.") #nanti ganti dengan redirect to page error(?)
    else:
        request.session['countWrong'] = 0
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
            
    def errorMessage(request, form, response, isFirstPage):
        #redirect to refreshed form with error message on top
        context = {'response': response, 'form': form, 'isFirstPage': isFirstPage}
        return render(request, 'home/resetPassword.html', context)

    """def errorMessage2(request, form, response):
        #redirect to refreshed form with error message on top
        context = {'response': response, 'form': form}
        return render(request, 'home/resetPassword2.html', context)"""

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

    initialA={'userType': request.session.get('userType', None), 'email': request.session.get('email', None),
    'afterFailedLoginMsg': request.session.get('afterFailedLoginMsg', ""), 'countWrong': request.session.get('countWrong', 0)}
    initialB={'OTP': request.session.get('OTP', None), 'startTime': request.session.get('startTime', json.dumps(datetime.now(), cls=DateTimeEncoder))}

    if request.method == 'POST':
        A_form = ResetPasswordFormA(request.POST, initial=initialA)
        B_form = ResetPasswordFormB(request.POST, initial=initialB)
        C_form = ResetPasswordFormC(request.POST)
        if A_form.is_valid():
            filledList = A_form.cleaned_data
            #if entered email not exist in Student/Parent/Teacher table, return empty form with error message
            if filledList['email'] not in getEmailList(filledList):
                #render empty form A with error message
                A_form = ResetPasswordFormA()
                response = "Maklumat yang anda masukkan adalah tidak tepat."
                isFirstPage = True
                return errorMessage(request, A_form, response, isFirstPage)
            #if entered email exist in Student/Parent/Teacher table, redirect to page saying to enter OTP sent to email
            else:
                #generate random OTP
                randomOTP = str(random.randint(100000, 999999))
                request.session['userType'] = filledList['userType']
                request.session['email'] = filledList['email']
                request.session['OTP'] = randomOTP
                currentName = ""

                if filledList['userType'] == 'Student':
                    currentName = dashboard.models.Student.objects.get(email=filledList['email']).name
                elif filledList['userType'] == 'Parent':
                    currentName = dashboard.models.Parent.objects.get(email=filledList['email']).name
                elif filledList['userType'] == 'Teacher':
                    currentName = dashboard.models.Teacher.objects.get(email=filledList['email']).name

                #send email with OTP to entered email
                send_mail(
                    '[no-reply] Future Cruise: Kemaskini Kata Laluan',
                    'Hai ' + currentName + '. Berikut merupakan nombor pin OTP untuk reset kata laluan anda. ' +
                    'OTP: ' + randomOTP +
                    '. Sila abaikan emel ini jika anda tidak berhasrat untuk menukar kata laluan anda.',
                    'ddalgihwa304@gmail.com',
                    [request.session['email']],
                    fail_silently=False,
                )
                #start time
                request.session['startTime'] = json.dumps(datetime.now(), cls=DateTimeEncoder)
                B_form = ResetPasswordFormB()
                context = {'currentEmail' : filledList['email'], 'form': B_form}
                return render(request, 'home/enterOTP.html', context)

        if B_form.is_valid():
            #current time
            currentTime = json.dumps(datetime.now(), cls=DateTimeEncoder)
            startTime = request.session['startTime']
            currentUserType = request.session['userType']
            currentEmail = request.session['email']
            currentOTP = request.session['OTP']
            filledList = B_form.cleaned_data
            startTimeDeserialized = datetime.strptime(startTime.replace("\"",""), '%Y-%m-%dT%H:%M:%S.%f')
            currentTimeDeserialized = datetime.strptime(currentTime.replace("\"",""), '%Y-%m-%dT%H:%M:%S.%f')
            diff = currentTimeDeserialized - startTimeDeserialized
            total_seconds = diff.total_seconds()
            #diff_encoded = json.dumps(diff, cls=DateTimeEncoder)
            
            #while otp does not expire yet (less/equal to 3 mins)
            while total_seconds <= 30:
                #if otp matches, generate C_form
                if filledList['OTP'] == currentOTP:
                    C_form = ResetPasswordFormC()
                    isFirstPage = False
                    context = {'form': C_form, 'isFirstPage': isFirstPage}
                    #return render(request, 'home/resetPassword2.html', context)
                    return render(request, 'home/resetPassword.html', context)
                #if otp do not match, refresh B_form again but with same OTP
                else:
                    error = "Nombor pin OTP tidak tepat."
                    B_form = ResetPasswordFormB()
                    context = {'error': error, 'currentEmail' : currentEmail, 'form': B_form}
                    return render(request, 'home/enterOTP.html', context)
            #if otp expired, generate B_form from awal (new OTP, send email, render template)
            #generate random OTP
            randomOTP = str(random.randint(100000, 999999))
            request.session['OTP'] = randomOTP
            currentName = ""

            if currentUserType == 'Student':
                currentName = dashboard.models.Student.objects.get(email=currentEmail).name
            elif currentUserType == 'Parent':
                currentName = dashboard.models.Parent.objects.get(email=currentEmail).name
            elif currentUserType == 'Teacher':
                currentName = dashboard.models.Teacher.objects.get(email=currentEmail).name

            #send email with OTP to entered email
            send_mail(
                '[no-reply] Future Cruise: Kemaskini Kata Laluan',
                'Hai ' + currentName + '. Berikut merupakan nombor pin OTP untuk reset kata laluan anda. ' +
                'OTP: ' + randomOTP +
                '. Nombor pin OTP ini akan luput dalam 3 minit. Sila abaikan emel ini jika anda tidak berhasrat untuk menukar kata laluan anda.',
                'ddalgihwa304@gmail.com',
                [currentEmail],
                fail_silently=False,
            )
            #start time
            expired = "Nombor pin OTP telah luput."
            request.session['startTime'] = json.dumps(datetime.now(), cls=DateTimeEncoder)
            B_form = ResetPasswordFormB()
            context = {'expired': expired, 'currentEmail' : currentEmail, 'form': B_form}
            return render(request, 'home/enterOTP.html', context)

        if C_form.is_valid():
            currentUserType = request.session['userType']
            currentEmail = request.session['email']
            filledList = C_form.cleaned_data
            #if first and second entered password is the same
            if filledList['newPass'] == filledList['newPassConfirm']:
                #if entered password length is 10
                if len(filledList['newPass']) == 10:
                    #if has at least 1 upper, lower, special and number characters
                    if checkChar(filledList['newPass']) == True:
                        if currentUserType == 'Student':
                            #update password in Student record for the entered email
                            StudentRecord = dashboard.models.Student.objects.get(email=currentEmail)
                            StudentRecord.password = filledList['newPassConfirm']
                            StudentRecord.save()
                        elif currentUserType == 'Parent':
                            #update password in Parent record for the entered email
                            ParentRecord = dashboard.models.Parent.objects.get(email=currentEmail)
                            ParentRecord.password = filledList['newPassConfirm']
                            ParentRecord.save() 
                        elif currentUserType == 'Teacher':
                            #update password in Teacher record for the entered email
                            TeacherRecord = dashboard.models.Teacher.objects.get(email=currentEmail)
                            TeacherRecord.password = filledList['newPassConfirm']
                            TeacherRecord.save()   
                        #redirect to intermediary page which displays success message (not Django message)
                        #and after 3 seconds redirect to home:login-nonadmin   
                        return render(request, 'home/redirSuccess.html')
                    #if either has no upper/lower/special/number characters
                    else:
                        response = "Kata laluan mestilah mengandungi huruf besar, huruf kecil, angka dan aksara khas."
                        isFirstPage = False
                        return errorMessage(request, C_form, response, isFirstPage)
                #if entered password length is not 10
                else:
                    response = "Kata laluan anda terlalu pendek."
                    isFirstPage = False
                    return errorMessage(request, C_form, response, isFirstPage)
            #if first and second entered password do not match
            else:          
                #display error passwords do not match
                response = "Sila pastikan kedua-dua kata laluan adalah sama."
                isFirstPage = False
                return errorMessage(request, C_form, response, isFirstPage)
            """#if a parent
            elif filledList['userType'] == 'Parent':
                #if entered email not exist in Parent table, return empty form with error message
                if filledList['email'] not in getEmailList(filledList):
                    form = ResetPasswordFormA()
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
                    form = ResetPasswordFormA()
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
    """
    else: 
        #if countwrong NOT 3 (user tekan terus button reset pass OR cuba 1/2 kali masuk pass dkt login page pastu tekan button reset pass)
        if request.session['countWrong'] < 3:
            #set balik message to empty
            request.session['afterFailedLoginMsg'] = ""
        #untuk countwrong 3, message kat page reset pass akan jadi yg "...salah 3 kali..."
        isFirstPage = True
        form = ResetPasswordFormA()
        context = {'form': form, 'afterFailedLoginMsg': request.session['afterFailedLoginMsg'], 'isFirstPage': isFirstPage}

    return render(request, 'home/resetPassword.html', context)