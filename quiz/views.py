from datetime import datetime
import dashboard.models
import quiz.models
import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import AvatarForm, AddFieldForm, AddQuestionForm, AddAnswerForm, AddHintForm, ChangeIconForm, CustomAnswerFormSet, CustomAnswerInlineFormSet, CustomHintFormSet, EditQuestionForm, EditHintForm, ChooseFieldForm, PlayForm
from django.forms import formset_factory, inlineformset_factory
from django.db import IntegrityError, transaction
from django.contrib import messages
from random import randint
from django.core.signals import request_finished
from datetime import timedelta

# Create your views here.
def quizMainAdmin(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        context = {'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz,
        'search': urlSearch, 'dashboard': urlDashboard, 'logout': urlLogout}
        return render(request, 'quiz\quizMainAdmin.html', context)
        #return HttpResponse(response % user_id)
    else:
        if 'S' in user_id:
            dashboardNav = " Pelajar"
            user_type = "pelajar"
        elif 'P' in user_id:
            dashboardNav = " Penjaga"
            user_type = "penjaga"
        elif 'T' in user_id:
            dashboardNav = " Guru"
            user_type = "guru"
        urlTest = 'test:index-nonadmin'
        urlBlog = 'blog:index-nonadmin'
        urlQuiz = 'quiz:index-student'
        urlSearch = 'search:index-nonadmin'
        urlDashboard = 'dashboard:index-nonadmin'
        urlLogout = 'dashboard:logout-confirm'
        username = currentUserRecord.username
        title = "Future Cruise: Permainan Kuiz Penerokaan Kerjaya"
        response = "Anda tidak dibenarkan untuk mengakses halaman ini."
        context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'response': response,
        'user_id': user_id, 'user_type': user_type, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz,
        'search': urlSearch, 'dashboard': urlDashboard, 'logout': urlLogout}
        return render(request, 'quiz/noAccessError.html', context)
        #return HttpResponse(response)

def quizMain(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'
    #user_id = student_id
    #comment out bawah ni sebab dah disable tab "Permainan Kuiz" for non-student
    """if 'S' not in user_id: #meaning actualy not student id (can be Px, Tx, A1)
        #if admin, redirect to quizMainAdmin
        #if parent, response: "Kuiz hanya boleh dimain oleh pelajar. Kembali ke papan pemuka untuk melihat laporan visual kuiz anak anda."
        #if teacher, response: "Kuiz hanya boleh dimain oleh pelajar. Kembali ke papan pemuka untuk melihat laporan individu dan analisis keseluruhan kuiz pelajar."
        #anything must pass url navbar nonadmin, user type yg salah, student_id as 'user_id' to redirected template
        if 'A' in user_id:
            return redirect('quiz:index-admin', user_id)
        elif 'P' in user_id:
            dashboardNav = " Penjaga"
            user_type = "penjaga"
        elif 'T' in user_id:
            dashboardNav = " Guru"
            user_type = "guru"
        currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
        username = currentUserRecord.username
        title = "Future Cruise: Permainan Kuiz Penerokaan Kerjaya"
        response = "Kuiz hanya boleh dimain oleh pelajar. Klik butang di bawah untuk melihat laporan kuiz pelajar."
        context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'response': response,
        'user_id': user_id, 'user_type': user_type, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz,
        'search': urlSearch, 'dashboard': urlDashboard, 'logout': urlLogout}
        return render(request, 'quiz/noAccessError.html', context)"""
    request.session['student_id'] = user_id

    currentStudentDetails = dashboard.models.Student.objects.get(ID=user_id)

    #check whether the user id has a Player record already or not
    #create new Player object for that user if no Player record yet
    currentPlayerUsername = ""
    try:
        currentPlayerRecord = quiz.models.Player.objects.get(ID=user_id)
        currentPlayerUsername = currentPlayerRecord.ID.ID.username #give username from User model
    except quiz.models.Player.DoesNotExist:
        currentPlayerRecord = quiz.models.Player(ID=currentStudentDetails) #Player.ID should be an instance of Student model with default avatar
        currentPlayerRecord.save(force_insert=True)
        currentPlayerUsername = currentPlayerRecord.ID.ID.username

    currentAvatarDetailsObject = currentPlayerRecord.avatarID
    response = "Anda berada di muka utama permainan kuiz."
    context = {'dashboardNav': dashboardNav, 'response': response, 'username': currentPlayerUsername, 'user_type': user_type, 'user_id': user_id,
    'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
    'currentAvatarDetailsObject': currentAvatarDetailsObject}
    return render(request, 'quiz/quizMainNonAdmin.html', context)

def showAvatar(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    #currentStudentDetails = dashboard.models.Student.objects.get(ID=user_id)
    currentPlayerRecordObject = quiz.models.Player.objects.get(ID=user_id)
    currentPlayerUsername = currentPlayerRecordObject.ID.ID.username #give username from User model
    currentAvatarDetailsObject = currentPlayerRecordObject.avatarID
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'
    #user_id = student_id

    context = {'dashboardNav': dashboardNav, 'username': currentPlayerUsername, 'currentAvatarDetailsObject': currentAvatarDetailsObject,
    'user_type': user_type, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout}
    #context = {'student_id': student_id, 'currentPlayerUsername': currentPlayerUsername, 'currentAvatarDetailsObject': currentAvatarDetailsObject}
    return render(request, 'quiz/showAvatar.html', context)

def editAvatar(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    #allAvatarDetailsList = quiz.models.AvatarGenderImageFinal.objects.values().order_by('id')
    currentPlayerRecord = quiz.models.Player.objects.get(ID=user_id)
    currentPlayerUsername = currentPlayerRecord.ID.ID.username #give username from User model
    currentAvatarDetailsObject = currentPlayerRecord.avatarID
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'
    isSubmitted = False
    #user_id = student_id

    if request.method == 'POST':
        currentPlayerAvatarID = currentPlayerRecord.avatarID.avatarID.id
        currentAvatarDetails = quiz.models.AvatarGenderImageFinal.objects.get(id=currentPlayerAvatarID)
        avatarID = currentAvatarDetails.avatarID.id
        workplace = currentAvatarDetails.workplace.id
        avatarGender = currentAvatarDetails.avatarGender.id
        imageURL = currentAvatarDetails.imageURL.id
        form = AvatarForm(request.POST, initial={'avatarID': avatarID, 'workplace': workplace, 'avatarGender': avatarGender,
        'imageURL': imageURL})
        if form.is_valid():
            currentStudentDetails = dashboard.models.Student.objects.get(ID=user_id)
            currentPlayerRecord = quiz.models.Player.objects.get(ID=user_id)
            #currentPlayerAvatarID = currentPlayerRecord.avatarID.avatarID.id
            #currentAvatarDetails = quiz.models.AvatarGenderImageFinal.objects.get(id=currentPlayerAvatarID)

            allAvatarDetails = quiz.models.AvatarGenderImageFinal.objects.all()
            for x in allAvatarDetails:
                if x.avatarID.careerName == form.cleaned_data['avatarID'].careerName:
                    if x.avatarGender.avatarGender == form.cleaned_data['avatarGender'].avatarGender:
                        currentPlayerRecord.avatarID = x
                        break
            #form.save()
            currentPlayerRecord.save()
            #currentAvatarDetailsObject = currentPlayerRecord.avatarID
            title = "Future Cruise: Tetapan Avatar"
            #successMessage = "Avatar berjaya dikemaskini!"
            isSubmitted = True
            context = {'title': title, 'dashboardNav': dashboardNav, 'username': currentPlayerUsername,
            'user_type': user_type, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
            'dashboard':urlDashboard, 'logout': urlLogout}
            #return redirect('quiz:show-avatar', user_id)
            #return render(request, 'quiz/editAvatar.html', context)
    else:
        currentPlayerAvatarID = currentPlayerRecord.avatarID.id
        currentAvatarDetails = quiz.models.AvatarGenderImageFinal.objects.get(id=currentPlayerAvatarID)
        avatarID = currentAvatarDetails.avatarID.id
        workplace = currentAvatarDetails.workplace.id
        avatarGender = currentAvatarDetails.avatarGender.id
        imageURL = currentAvatarDetails.imageURL.id
        form = AvatarForm(initial={'avatarID': avatarID, 'workplace': workplace, 'avatarGender': avatarGender,
        'imageURL': imageURL})
        #form = AvatarForm()

    context = {'dashboardNav': dashboardNav, 'username': currentPlayerUsername, 'currentAvatarDetailsObject': currentAvatarDetailsObject,
    'user_type': user_type, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard':urlDashboard, 'logout': urlLogout, 'form': form, 'isSubmitted': isSubmitted}
    #return render(request, 'quiz/editAvatar.html', {'user_id': student_id, 'form': form, 'currentPlayerAvatar': currentPlayerRecord.avatarID})
    return render(request, 'quiz/editAvatar.html', context)

"""
def get_imageURL(request, avatarGender):
    #avatarID = quiz.models.Avatar.objects.get(pk=avatarID)
    avatarGender = quiz.models.AvatarGender.objects.get(pk=avatarGender.pk)
    imageURL = quiz.models.AvatarGenderImage.objects.get(avatarGender=avatarGender).imageURL

    #imageURL_dict = {}
    #for URL in imageURL:
    #    imageURL_dict[URL]

    return HttpResponse(json.dumps(imageURL), mimetype="application/json")
"""

def showField(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    if user_id == 'A1':
        urlTest = 'test:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        urlShowQuestion = 'quiz:show-question'
        urlChangeIcon = 'quiz:change-icon'

        if request.method == 'GET': # If the form is submitted / refresh page
            search_text = request.GET.get('kotak_carian', None)
            #if admin cari kerjaya (submit form search)
            if search_text is not None:
                gameFields = quiz.models.GameField.objects.filter(name__icontains=search_text).order_by('name')
                #if bidang yg dicari ada dalam GameField table
                if gameFields.exists():
                    fieldIDList = list(gameFields.values_list('id', flat=True).order_by('name'))
                    fieldIDinQuesValueList = list(quiz.models.GameQuestion.objects.values_list('fieldID', flat=True).order_by('id'))

                    fieldQuesCountList = []
                    for i in range(len(fieldIDList)):
                        fieldQuesCountList.append(0)

                    for id in fieldIDinQuesValueList:
                        for j in range(len(fieldIDList)):
                            if id == fieldIDList[j]:
                                fieldQuesCountList[j] += 1
                                break
                    
                    #fieldIDList = [gameFields.first().id]
                    #fieldIDinQuesValueList = list(quiz.models.GameQuestion.objects.values_list('fieldID', flat=True))
                    #fieldQuesCountList = [0]
                    #for id in fieldIDinQuesValueList:
                    #    if id == gameFields.first().id:
                    #        fieldQuesCountList[0] += 1
                else:
                    context = {'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
                    'dashboard': urlDashboard, 'logout': urlLogout, 'showquestion': urlShowQuestion, 'changeicon': urlChangeIcon,
                    'gameFields': gameFields, 'search_text': search_text, 'gameFieldsCount': gameFields.count()}
                    return render(request, 'quiz/showField.html', context)
            #if admin tak cari kerjaya (refresh page)
            else:
                gameFields = quiz.models.GameField.objects.all().order_by('name')
                fieldIDList = list(quiz.models.GameField.objects.values_list('id', flat=True).order_by('name'))
                fieldIDinQuesValueList = list(quiz.models.GameQuestion.objects.values_list('fieldID', flat=True).order_by('id'))

                fieldQuesCountList = []
                for k in range(len(fieldIDList)):
                    fieldQuesCountList.append(0)

                for id in fieldIDinQuesValueList:
                    for m in range(len(fieldIDList)):
                        if id == fieldIDList[m]:
                            fieldQuesCountList[m] += 1
                            break

        lengthFQCL = len(fieldQuesCountList)
        #cnt = 0
        #fixedCnt = 0
        context = {'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
        'dashboard': urlDashboard, 'logout': urlLogout, 'showquestion': urlShowQuestion, 'changeicon': urlChangeIcon,
        'gameFields': gameFields, 'fieldQuesCountList': fieldQuesCountList, 'lengthFQCL': lengthFQCL,
        'search_text': search_text, 'gameFieldsCount': gameFields.count()}
        return render(request, 'quiz/showField.html', context)
    else:
        if 'S' in user_id:
            dashboardNav = " Pelajar"
            user_type = "pelajar"
        elif 'P' in user_id:
            dashboardNav = " Penjaga"
            user_type = "penjaga"
        elif 'T' in user_id:
            dashboardNav = " Guru"
            user_type = "guru"
        urlTest = 'test:index-nonadmin'
        urlBlog = 'blog:index-nonadmin'
        urlQuiz = 'quiz:index-student'
        urlSearch = 'search:index-nonadmin'
        urlDashboard = 'dashboard:index-nonadmin'
        urlLogout = 'dashboard:logout-confirm'
        currentUserRecord = dashboard.models.User.objects.get(ID=user_id)
        username = currentUserRecord.username
        title = "Future Cruise: Permainan Kuiz Penerokaan Kerjaya"
        response = "Anda tidak dibenarkan untuk mengakses halaman ini."
        context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'response': response,
        'user_id': user_id, 'user_type': user_type, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz,
        'search': urlSearch, 'dashboard': urlDashboard, 'logout': urlLogout}
        return render(request, 'quiz/noAccessError.html', context)

def addField(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    allImageField = quiz.models.ImageField.objects.all()

    if request.method == 'POST':
        form = AddFieldForm(request.POST)
        if form.is_valid():
            filledList = form.cleaned_data
            allGameFields = quiz.models.GameField.objects.all()
            #fieldNameList = list(allGameFields.values_list('name', flat=True))
            containsFilledName = allGameFields.filter(name__icontains=filledList['name'])
            fieldNameListContainsFilledName = list(containsFilledName.values_list('name', flat=True))
            #if dah ada nama bidang kerjaya tu yg sama or lebih kurang dlm GameField table
            if len(fieldNameListContainsFilledName) > 0:
                errorMessage = "Bidang kerjaya telah wujud. Sila masukkan bidang kerjaya lain."
                form = AddFieldForm()
                context = {'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
                'dashboard': urlDashboard, 'logout': urlLogout, 'errorMessage': errorMessage,
                'allImageField': allImageField, 'form': form}
                return render(request, 'quiz/addField.html', context)
            #kalau memang takda
            else:
                allImageField = quiz.models.ImageField.objects.all()
                allImageFieldIDListinGameField = list(quiz.models.GameField.objects.values_list('imageURL', flat=True))
                selectedImageRecord = allImageField.get(imageURL=filledList['image'])
                #if filled/selected image is selain default (id 1) and already exist in GameField (used by other kerjaya)
                if (selectedImageRecord.id in allImageFieldIDListinGameField) and selectedImageRecord.id != 1:
                    errorMessage = "Ikon telah digunakan untuk bidang kerjaya lain. Sila pilih ikon yang lain."
                    form = AddFieldForm()
                    context = {'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
                    'dashboard': urlDashboard, 'logout': urlLogout, 'errorMessage': errorMessage,
                    'allImageField': allImageField, 'form': form}
                    return render(request, 'quiz/addField.html', context)
                else:
                    quiz.models.GameField.objects.create(name=filledList['name'], imageURL=selectedImageRecord)
                    return redirect('quiz:show-field', user_id)
    else:
        form = AddFieldForm()

    context = {'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard': urlDashboard, 'logout': urlLogout, 'allImageField': allImageField, 'form': form}
    return render(request, 'quiz/addField.html', context)

def changeIcon(request, user_id, field_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    allGameFields = quiz.models.GameField.objects.all()
    currentGameFieldRecord = allGameFields.get(id=field_id)
    currentGameFieldName = currentGameFieldRecord.name

    if request.method == 'POST':
        form = ChangeIconForm(request.POST)
        if form.is_valid():
            filledList = form.cleaned_data
            allImageField = quiz.models.ImageField.objects.all()
            allImageFieldIDListinGameField = list(quiz.models.GameField.objects.values_list('imageURL', flat=True))
            selectedImageRecord = allImageField.get(imageURL=filledList['image'])
            #if filled/selected image is selain default (id 1) and already exist in GameField (used by other kerjaya)
            if (selectedImageRecord.id in allImageFieldIDListinGameField) and selectedImageRecord.id != 1:
                errorMessage = "Ikon telah digunakan untuk bidang kerjaya lain. Sila pilih ikon yang lain."
                form = ChangeIconForm()
                context = {'user_id': user_id, 'field_id': field_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
                'dashboard': urlDashboard, 'logout': urlLogout, 'errorMessage': errorMessage,
                'currentGameFieldName': currentGameFieldName, 'form': form}
                return render(request, 'quiz/changeIcon.html', context)
            else:
                currentGameFieldRecord.imageURL = selectedImageRecord
                currentGameFieldRecord.save()
                return redirect('quiz:show-field', user_id)
    else:
        form = ChangeIconForm()

    context = {'user_id': user_id, 'field_id': field_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard': urlDashboard, 'logout': urlLogout, 'currentGameFieldName': currentGameFieldName, 'form': form}
    return render(request, 'quiz/changeIcon.html', context)

def showQuestion(request, user_id, field_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    allGameFields = quiz.models.GameField.objects.all()
    currentGameFieldRecord = allGameFields.get(id=field_id)
    currentGameFieldName = currentGameFieldRecord.name
    gameQuestions = quiz.models.GameQuestion.objects.filter(fieldID=currentGameFieldRecord).order_by('id')
    allGameQuesAns = quiz.models.GameAnswer.objects.order_by('id')
    allGameHintQuesIDList = quiz.models.GameHint.objects.order_by('id').values_list('questionID_id', flat=True)

    if request.method == 'GET': # If the form is submitted / refresh page
        search_text = request.GET.get('kotak_carian', None)
        filter_selected = request.GET.get('difficulty', None)
        #if admin ada search soalan (search form submitted = GET request)
        if search_text is not None:
            gameQuestions = gameQuestions.filter(questionText__icontains=search_text) #either exist or not (found or not)
            #if admin select filter difficulty selain value 'Tiada'
            if filter_selected != 'Tiada':
                gameQuestions = gameQuestions.filter(difficulty=filter_selected)
                #return HttpResponse(filter_selected + ", count: " + str(gameQuestions.count()))
            
    #if admin tak search soalan AND tak filter difficulty (refresh page = GET request)
    context = {'user_id': user_id, 'field_id': field_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard': urlDashboard, 'logout': urlLogout, 'currentGameFieldName': currentGameFieldName,
    'gameQuestions': gameQuestions, 'search_text': search_text, 'filter_selected': filter_selected,
    'gameQuestionsCount': gameQuestions.count(), 'allGameQuesAns': allGameQuesAns, 'allGameHintQuesIDList': allGameHintQuesIDList}
    return render(request, 'quiz/showQuestion.html', context)

def addQuestion(request, user_id, field_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    allGameFields = quiz.models.GameField.objects.all()
    currentGameFieldRecord = allGameFields.get(id=field_id)
    currentGameFieldName = currentGameFieldRecord.name

    answerFormSet = formset_factory(AddAnswerForm, formset=CustomAnswerFormSet, extra=2, min_num=2, max_num=4, validate_min=True) 
    hintFormSet = formset_factory(AddHintForm, formset=CustomHintFormSet, extra=3, max_num=3)
    errormsg1, errormsg2, errormsg3, errormsg4, errormsg5 = "", "", "", "", ""

    if request.method == 'POST':
        questionForm = AddQuestionForm(request.POST, request.FILES)
        answer_formset = answerFormSet(request.POST, prefix='answer', error_messages={'too_few_forms': 'Sila isi paling kurang 2 pilihan jawapan.'})
        hint_formset = hintFormSet(request.POST, request.FILES, prefix='hint')
        if questionForm.is_valid() and answer_formset.is_valid() and hint_formset.is_valid():
            #ADD QUESTION
            filledListQues = questionForm.cleaned_data
            questionText = filledListQues['questionText']
            questionImage = filledListQues['questionImage']
            difficulty = filledListQues['difficulty']
            lastEdited = datetime.now
            points = 0
            timeLimit = 0
            if difficulty == 'Mudah':
                points = 6
                timeLimit = 10
            elif difficulty == 'Sederhana':
                points = 8
                timeLimit = 20
            else:
                points = 10
                timeLimit = 30
            quiz.models.GameQuestion.objects.create(fieldID_id=field_id, questionText=questionText,
            questionImage=questionImage, difficulty=difficulty, points=points, timeLimit=timeLimit, lastEdited=lastEdited)

            latestQuestionRecord = quiz.models.GameQuestion.objects.order_by('-id').first()

            #ADD ANSWER
            new_ans = []

            for answer_form in answer_formset:
                answerText = answer_form.cleaned_data.get('answerText')
                isCorrect = answer_form.cleaned_data.get('isCorrect')

                if answerText:
                    if isCorrect == 'on':
                        isCorrect == True
                    else:
                        isCorrect == False
                    new_ans.append(quiz.models.GameAnswer(questionID_id=latestQuestionRecord.id,
                    answerText=answerText, isCorrect=isCorrect))

            #ADD HINT 
            new_hints = []

            for hint_form in hint_formset:
                hintText = hint_form.cleaned_data.get('hintText')
                hintImage = hint_form.cleaned_data.get('hintImage')
                value = hint_form.cleaned_data.get('value')

                if hintText and value:
                    new_hints.append(quiz.models.GameHint(questionID_id=latestQuestionRecord.id,
                    hintText=hintText, hintImage=hintImage, value=value))

            try:
                with transaction.atomic():
                    quiz.models.GameAnswer.objects.bulk_create(new_ans)
                    quiz.models.GameHint.objects.bulk_create(new_hints)
                    latestQuestionRecord.lastEdited = datetime.now
                    latestQuestionRecord.save()
                    currentGameFieldRecord.lastEdited = latestQuestionRecord.lastEdited
                    allGameQuesCurrField = quiz.models.GameQuestion.objects.filter(fieldID_id=field_id)
                    if allGameQuesCurrField.count() >= 10 and currentGameFieldRecord.show == False:
                        currentGameFieldRecord.show = True
                    currentGameFieldRecord.save()

                    # And notify our users that it worked
                    return redirect('quiz:show-question', user_id, field_id)

            except IntegrityError: #If the transaction failed
                return HttpResponse("Question, answers and hints failed to be added.") #test
        #not valid
        else:
            if (questionForm.is_valid() == False) or (questionForm.non_field_errors()):
                errormsg1 += str(questionForm.non_field_errors())
                #memang cannot make it appear different error message if no questionText entered (dia keluar yg popup kat field tu)

            if (answer_formset.is_valid() == False) or (answer_formset.non_form_errors()):
                for dict in answer_formset.non_form_errors():
                    #(1) if admin submit one non-empty answer only, either iscorrect ticked or not (others empty + not ticked correct)
                    #or submit one empty answer with iscorrect ticked
                    #means not enough answers/not reach minimum
                    if "Please submit at least" in dict:
                        errormsg2 += str("(1) Sila isi minimum " + str(answerFormSet.min_num) + " pilihan jawapan.")
                    else:
                        errormsg2 += str(dict)

                answerRequiredDict = {'answerText': ['This field is required.']}

                for dict in answer_formset.errors:
                    #(2) if admin tick iscorrect at empty answer (means nak add but no text), for total answer to be added >= minimum
                    #(1) & (2) display if add minimum but both empty + one ticked iscorrect
                    #break: for (1) & (2) do not display repeating required error
                    if answerRequiredDict == dict:
                        errormsg3 += "(2) Teks jawapan yang hendak ditambah mestilah diisi dan tidak dibiarkan kosong."
                        break

            if (hint_formset.is_valid() == False) or (hint_formset.non_form_errors()):
                #errormsg4 += str(hint_formset.non_form_errors())
                for dict in hint_formset.non_form_errors():
                        #(3): from forms.py customhintformset, error for same hinttext
                        errormsg4 += str(dict)

                hintRequiredDict = {'hintText': ['This field is required.']}
                valueRequiredDict = {'value':['This field is required.']}
                hintValueRequiredDict = {'hintText': ['This field is required.'], 'value': ['This field is required.']}
                for dict in hint_formset.errors:
                    #(1) if the hint is in DB (ada kotak "Buang?" kat hujung) but admin padam text and/or value dia and submit (maybe sbb nak delete), means mcm tak isi
                    # or if admin add new hint (only automatically indicated if got uploaded image) but its text and/or value is empty
                    if hintRequiredDict == dict or valueRequiredDict == dict or hintValueRequiredDict == dict:
                        errormsg5 += "(1) Teks dan nilai petunjuk yang hendak ditambah mestilah diisi dan tidak dibiarkan kosong."
                        break
    else:
        questionForm = AddQuestionForm()
        answer_formset = answerFormSet(prefix='answer')
        hint_formset = hintFormSet(prefix='hint')

    context = {'user_id': user_id, 'field_id': field_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard': urlDashboard, 'logout': urlLogout, 'currentGameFieldName': currentGameFieldName, 'questionForm': questionForm,
    'answer_formset': answer_formset, 'hint_formset': hint_formset, 'errormsg1': errormsg1, 'errormsg2': errormsg2,
    'errormsg3': errormsg3, 'errormsg4': errormsg4, 'errormsg5': errormsg5}
    return render(request, 'quiz/addQuestion.html', context) 

def editQuestion(request, user_id, field_id, question_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    allGameFields = quiz.models.GameField.objects.all()

    currentGameFieldRecord = allGameFields.get(id=field_id)
    currentGameFieldName = currentGameFieldRecord.name
    currentGameQuestionRecord = quiz.models.GameQuestion.objects.get(id=question_id)
    questionText = currentGameQuestionRecord.questionText
    questionImage = currentGameQuestionRecord.questionImage
    difficulty = currentGameQuestionRecord.difficulty

    currentGameAnswerRecords = quiz.models.GameAnswer.objects.filter(questionID_id=question_id)
    cnt_old_ans = currentGameAnswerRecords.count()
    extra_ans = 0

    if cnt_old_ans < 4:
        extra_ans = 4 - cnt_old_ans

    currentGameHintRecords = quiz.models.GameHint.objects.filter(questionID_id=question_id)
    cnt_old_hint = currentGameHintRecords.count()
    extra_hint = 0

    if cnt_old_hint < 3:
        extra_hint = 3 - cnt_old_hint

    answerInlineFormSet = inlineformset_factory(quiz.models.GameQuestion, quiz.models.GameAnswer, formset=CustomAnswerInlineFormSet, extra=extra_ans, min_num=2, max_num=4, validate_min=True, fields=('answerText', 'isCorrect',), can_delete=True)
    hintInlineFormSet = inlineformset_factory(quiz.models.GameQuestion, quiz.models.GameHint, form=EditHintForm, extra=extra_hint, max_num=3, fields=('hintText', 'hintImage', 'value',), can_delete=True)
    errormsg1, errormsg2, errormsg3, errormsg4, errormsg5, errormsg6, errormsg7, errormsg8 = "", "", "", "", "", "", "", ""

    if request.method == "POST":
        questionForm = EditQuestionForm(request.POST, request.FILES, initial={'questionText': questionText, 'questionImage': questionImage, 'difficulty': difficulty})
        answer_inlineformset = answerInlineFormSet(request.POST, instance=currentGameQuestionRecord, prefix='answer')
        hint_inlineformset = hintInlineFormSet(request.POST, request.FILES, instance=currentGameQuestionRecord, prefix='hint')

        if questionForm.is_valid() and answer_inlineformset.is_valid() and hint_inlineformset.is_valid():
            #EDIT QUESTION
            difficulty = questionForm.cleaned_data.get('difficulty')
            currentGameQuestionRecord.questionText = questionForm.cleaned_data.get('questionText')
            
            questionImage = questionForm.cleaned_data.get('questionImage')
            if questionImage == False:
                currentGameQuestionRecord.questionImage = None
            else:
                currentGameQuestionRecord.questionImage = questionImage
            
            if currentGameQuestionRecord.difficulty != difficulty:
                if difficulty == 'Mudah':
                    currentGameQuestionRecord.points = 6
                    currentGameQuestionRecord.timeLimit = 10
                elif difficulty == 'Sederhana':
                    currentGameQuestionRecord.points = 8
                    currentGameQuestionRecord.timeLimit = 20
                else:
                    currentGameQuestionRecord.points = 10
                    currentGameQuestionRecord.timeLimit = 30
            currentGameQuestionRecord.difficulty = difficulty

            #EDIT ANSWER
            for answer_form in answer_inlineformset:
                answerText = answer_form.cleaned_data.get('answerText')
                isDeleted = answer_form.cleaned_data.get('DELETE')

                if answerText is not None:
                    if isDeleted == True:
                        currentGameAnswerRecords.get(answerText=answerText).delete()
                    else:
                        answer_form.save()

            #EDIT HINTS
            for hint_form in hint_inlineformset:
                hintText = hint_form.cleaned_data.get('hintText')
                value = hint_form.cleaned_data.get('value')
                isDeleted = hint_form.cleaned_data.get('DELETE')

                if hintText and value:
                    if isDeleted == True:
                        currentGameHintRecords.get(hintText=hintText).delete()
                    else:
                        hint_form.save()

            currentGameQuestionRecord.lastEdited = datetime.now
            currentGameQuestionRecord.save()
            currentGameFieldRecord.lastEdited = currentGameQuestionRecord.lastEdited
            allGameQuesCurrField = quiz.models.GameQuestion.objects.filter(fieldID_id=field_id)
            if allGameQuesCurrField.count() >= 10 and currentGameFieldRecord.show == False:
                currentGameFieldRecord.show = True
            currentGameFieldRecord.save()
            
            return redirect('quiz:show-question', user_id, field_id)
        #not valid
        else:
            if (questionForm.is_valid() == False) or (questionForm.non_field_errors()):
                errormsg1 += str(questionForm.non_field_errors())

                for dict in questionForm.errors.as_data():
                    if 'questionText' == dict:
                        for errors in questionForm.errors['questionText'].as_data():
                            #questionForm.errors['questionText'].as_data() = [ValidationError(['This field is required.']), ....if got more]
                            for error in errors:
                                #errors (a list of errors for questionText field) = ['This field is required',...if ada more error for this field/item]
                                #(1) if the current question text is erased by admin, so it detects no value
                                if 'This field is required.' == error:
                                    #error (only error message) = 'This field is required.'
                                    errormsg2 += "(1) Teks soalan tidak boleh dibiarkan kosong."
                    elif 'questionImage' == dict:
                        for errors in questionForm.errors['questionImage'].as_data():
                            for error in errors:
                                #(2) if admin tick "padam gambar" and also upload new question image, will raise error to do either one je
                                if 'Please either submit a file or check the clear checkbox, not both.' == error:
                                    errormsg3 += "(2) Anda hanya boleh memadam gambar atau memuat naik gambar baharu, dan bukan kedua-duanya."

            if (answer_inlineformset.is_valid() == False) or (answer_inlineformset.non_form_errors()):
                for dict in answer_inlineformset.non_form_errors():
                    #(1) if admin nak tick "Buang?" dekat jawapan (tak kira kosong or not) but tu dah minimum jawapan needed,
                    #means tak cukup jawapan
                    if "Please submit at least" in dict:
                        errormsg4 += str("(1) Jumlah minimum pilihan jawapan yang perlu adalah " + str(answerInlineFormSet.min_num) + ".")
                    else:
                        errormsg4 += str(dict)
                
                answerRequiredDict = {'answerText': ['This field is required.']}

                for dict in answer_inlineformset.errors:
                    #(2) if the answer is in DB (ada kotak "Buang?" kat hujung) but admin padam text dia and submit sbb nak delete, means mcm tak isi
                    # or if admin add new answer (indicated by iscorrect ticked) but its empty
                    if answerRequiredDict == dict:
                        errormsg5 += "(2) Teks jawapan sedia ada (mempunyai kotak \"Buang?\") tidak boleh dibiarkan kosong. Jika anda ingin memadam mana-mana jawapan yang mempunyai kotak berkenaan, anda perlu menanda pada kotak tersebut dan bukan memadam teks jawapan. Ruangan teks jawapan juga tidak boleh dibiarkan kosong jika anda ingin menambah jawapan baharu (tiada kotak \"Buang?\")."
                    
                    #both (3 - from forms.py) & (2) error appear if jawapan ada 2/minimum (satu kosong),
                    #tapi admin tick delete dekat jawapan yg tak kosong, tapi jawapan satu lg kosong

            if (hint_inlineformset.is_valid() == False) or (hint_inlineformset.non_form_errors()):
                errormsg6 += str(hint_inlineformset.non_form_errors())

                hintRequiredDict = {'hintText': ['This field is required.']}
                valueRequiredDict = {'value':['This field is required.']}
                hintValueRequiredDict = {'hintText': ['This field is required.'], 'value': ['This field is required.']}
                clearOrUploadNewImageDict = {'hintImage': ['Please either submit a file or check the clear checkbox, not both.']}
                for dict in hint_inlineformset.errors:
                    #(1) if the hint is in DB (ada kotak "Buang?" kat hujung) but admin padam text and/or value dia and submit (maybe sbb nak delete), means mcm tak isi
                    # or if admin add new hint (only automatically indicated if got uploaded image) but its text and/or value is empty
                    if hintRequiredDict == dict or valueRequiredDict == dict or hintValueRequiredDict == dict:
                        errormsg7 += "(1) Teks dan nilai petunjuk sedia ada (mempunyai kotak \"Buang?\") tidak boleh dibiarkan kosong. Jika anda ingin memadam mana-mana petunjuk yang mempunyai kotak berkenaan, anda perlu menanda pada kotak tersebut dan bukan memadam teks atau nilai petunjuk. Ruangan teks dan nilai petunjuk juga tidak boleh dibiarkan kosong jika anda ingin menambah petunjuk baharu (tiada kotak \"Buang?\")."
                        break
                    #(2) if admin tick "padam gambar" and also upload new hint image, will raise error to do either one je
                    elif clearOrUploadNewImageDict == dict:
                        errormsg8 += "(2) Anda hanya boleh memadam gambar atau memuat naik gambar baharu, dan bukan kedua-duanya."
                        break
    else:
        questionForm = EditQuestionForm(initial={'questionText': questionText, 'questionImage': questionImage, 'difficulty': difficulty})
        answer_inlineformset = answerInlineFormSet(instance=currentGameQuestionRecord, prefix='answer')
        hint_inlineformset = hintInlineFormSet(instance=currentGameQuestionRecord, prefix='hint')

    context = {'user_id': user_id, 'field_id': field_id, 'question_id': question_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard': urlDashboard, 'logout': urlLogout, 'currentGameFieldName': currentGameFieldName, 'questionForm': questionForm,
    'answer_inlineformset': answer_inlineformset, 'hint_inlineformset': hint_inlineformset,
    'errormsg1': errormsg1, 'errormsg2': errormsg2,'errormsg3': errormsg3, 'errormsg4': errormsg4,
    'errormsg5': errormsg5, 'errormsg6': errormsg6, 'errormsg7': errormsg7, 'errormsg8': errormsg8}
    return render(request, 'quiz/editQuestion.html', context)  

def chooseField(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    currentPlayerRecordObject = quiz.models.Player.objects.get(ID=user_id)
    currentPlayerUsername = currentPlayerRecordObject.ID.ID.username #give username from User model
    currentAvatarDetailsObject = currentPlayerRecordObject.avatarID
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'

    isFieldSelected = False
    selectedFieldID = 0
    #get all field records ordered by True > False and ascending name order
    gameFields = quiz.models.GameField.objects.order_by('-show', 'name')
    #get values_list of field name, also ordered by True > False and ascending name order
    fieldNameList = list(gameFields.values_list('name', flat=True).order_by('-show', 'name'))
    #get values_list of field show column, also ordered by True > False and ascending name order
    fieldShowList = list(gameFields.values_list('show', flat=True).order_by('-show', 'name'))
    #get all field image records
    allFieldImage = quiz.models.ImageField.objects.all()
    #instantiate list of field image URL
    imageURLList = []

    #append image URL into imageURLList following the order of gameFields
    for field in gameFields:
        for image in allFieldImage:
            if field.imageURL_id == image.id:
                imageURLList.append(image.imageURL)
                break

    if request.method == 'POST':
        form = ChooseFieldForm(request.POST)
        if form.is_valid():
            filledList = form.cleaned_data
            selectedFieldRecord = gameFields.get(name=filledList['name'])
            selectedFieldID = selectedFieldRecord.id
            isFieldSelected = True

            context = {'dashboardNav': dashboardNav, 'username': currentPlayerUsername,
            'currentAvatarDetailsObject': currentAvatarDetailsObject, 'gameFields': gameFields,
            'user_type': user_type, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
            'dashboard': urlDashboard, 'logout': urlLogout, 'form': form, 'isFieldSelected': isFieldSelected,
            'selectedFieldID': selectedFieldID, 'imageURLList': imageURLList, 'fieldNameList': fieldNameList,
            'fieldShowList': fieldShowList}
            #return HttpResponse('dah pilih')
            return render(request, 'quiz/chooseField.html', context)
    else:
        form = ChooseFieldForm()

    context = {'dashboardNav': dashboardNav, 'username': currentPlayerUsername,
    'currentAvatarDetailsObject': currentAvatarDetailsObject, 'gameFields': gameFields,
    'user_type': user_type, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard': urlDashboard, 'logout': urlLogout, 'form': form, 'isFieldSelected': isFieldSelected,
    'selectedFieldID': selectedFieldID, 'imageURLList': imageURLList, 'fieldNameList': fieldNameList,
    'fieldShowList': fieldShowList}
    return render(request, 'quiz/chooseField.html', context)

def getRandomQuestion(cnt_ques, allQuestionsPerField, questionsExceptAttended):
    id_list = list(allQuestionsPerField.order_by('id').values_list('id', flat=True))
    min_id = min(id_list)
    max_id = max(id_list)

    while True:
        randomID = randint(min_id, max_id)
        if cnt_ques == 1:
            chosenQuestionRecord = allQuestionsPerField.filter(id=randomID).first()
        else:
            chosenQuestionRecord = questionsExceptAttended.filter(id=randomID).first()
        
        if chosenQuestionRecord:
            return chosenQuestionRecord

def getRandomHint(nextHintRecords):
    id_list = list(nextHintRecords.order_by('id').values_list('id', flat=True))
    min_id = min(id_list)
    max_id = max(id_list)

    while True:
        randomID = randint(min_id, max_id)
        chosenHintRecord = nextHintRecords.filter(id=randomID).first()

        if chosenHintRecord:
            return chosenHintRecord 

def play(request, user_id, field_id, cnt_ques):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    currentPlayerRecordObject = quiz.models.Player.objects.get(ID=user_id)
    currentPlayerUsername = currentPlayerRecordObject.ID.ID.username #give username from User model
    currentAvatarDetailsObject = currentPlayerRecordObject.avatarID
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'

    currentFieldRecord = quiz.models.GameField.objects.get(id=field_id)

    #[TEST] this one for test sementara je, biar dia guna the same record sbb tkmau create banyak2 record if refresh page play
    """ currentFieldPlayerSession = quiz.models.FieldPlayerSession.objects.get_or_create(
        fieldPlayerID_id=user_id,
        fieldID_id=field_id
    )[0]  """

    # real one
    allCurrFieldPlayerSession = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, fieldID_id=field_id).order_by('id')
    cntFieldPlayerSession = allCurrFieldPlayerSession.count()

    if cntFieldPlayerSession > 0:
        #if cnt_ques = 1 for GET request je (initial load), bukannya create waktu refresh page after submit first ques gak
        #note: if refresh page at first ques, still create a new record (redundancy? but the old one has default values)
        if int(cnt_ques) == 1 and request.method != 'POST': 
            currentFieldPlayerSession = quiz.models.FieldPlayerSession.objects.create(
                fieldPlayerID_id=user_id,
                fieldID_id=field_id
            )
        else:
            currentFieldPlayerSession = allCurrFieldPlayerSession.last()
    else:
        currentFieldPlayerSession = quiz.models.FieldPlayerSession.objects.create(
            fieldPlayerID_id=user_id,
            fieldID_id=field_id
        )

    currentPlayerAllFieldRecords = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id)
    currentPlayerTotalScoreAllFieldList = list(currentPlayerAllFieldRecords.values_list('currentPointsEarned', flat=True))
    currentPlayerTotalScoreAllField = 0
    for score in currentPlayerTotalScoreAllFieldList:
        currentPlayerTotalScoreAllField += score

    allQuestionsPerField = quiz.models.GameQuestion.objects.filter(fieldID_id=field_id)
    next_cnt_ques = str(int(cnt_ques) + 1)

    """ del request.session['attendedQuestions']
    del request.session['cntQuesList']
    del request.session['user_id']
    del request.session['field_id']
    del request.session['cnt_ques']
    del request.session['hasSubmittedList']
    del request.session['hasAnsweredList']
    del request.session['isCorrectList']
    del request.session['hintsUsedList']
    return HttpResponse("done") """

    """ return HttpResponse(
        "session list: " + str(request.session['attendedQuestions']) +
        ", cntQuesList: " + str(request.session['cntQuesList']) +
        ", hasSubmittedList: " + str(request.session['hasSubmittedList']) +
        ", hasAnsweredList: " + str(request.session['hasAnsweredList']) +
        ", isCorrectList: " + str(request.session['isCorrectList']) +
        ", hintUsedList: " + str(request.session['hintsUsedList']) +
        ", user_id req: " + str(request.session['user_id']) +
        ", field_id req: " + str(request.session['field_id']) +
        ", cnt_ques req: " + str(request.session['cnt_ques'])
    ) """

    #for first ques
    #if baru load page first ques (initial) OR refresh page first ques time belum jawab
    #   if the essential keys is a subset (exist) in current session keys
    #   or if the essential keys do not exist...
    #       give default values to request session keys to avoid guna attendedQuestions, cntQuesList yg sama as prev session
    #       for the same user AND same field/diff field
    #meaning whoever starts the quiz, no matter what field, will get default keys values initially
    required_keys = frozenset(('attendedQuestions','cntQuesList','user_id','field_id','cnt_ques','hasSubmittedList',
    'hasAnsweredList', 'isCorrectList', 'hintsUsedList'))

    if cnt_ques == '1' and request.method == 'GET':
        if required_keys <= request.session.keys():
            request.session['attendedQuestions'] = []
            request.session['cntQuesList'] = []
            request.session['user_id'] = user_id #test
            request.session['field_id'] = field_id #test
            request.session['cnt_ques'] = cnt_ques #test
            request.session['hasSubmittedList'] = [] #test
            request.session['hasAnsweredList'] = [] #test
            request.session['isCorrectList'] = [] #test
            request.session['hintsUsedList'] = [] 
        else:
            request.session['attendedQuestions'] = []
            request.session['cntQuesList'] = []
            request.session['user_id'] = user_id
            request.session['field_id'] = field_id
            request.session['cnt_ques'] = cnt_ques
            request.session['hasSubmittedList'] = []
            request.session['hasAnsweredList'] = []
            request.session['isCorrectList'] = []
            request.session['hintsUsedList'] = []

    attendedQuestionsIDsList = request.session['attendedQuestions']
    questionsExceptAttended = allQuestionsPerField #for getRandomQuestion condition cnt_ques = 1
    questionsExceptAttendedIDs = [] #[TEST] for display in template; if cnt_ques=1 - [], else - take from ifelse below

    #if have more than one cnt_ques in list (not into the first ques)
    if len(request.session['cntQuesList']) > 0:
        #if current cnt_ques same as the latest cnt_ques in list ((GET) page refreshed by user OR (POST) after submit while displaying answers)
        #display same ques
        if cnt_ques == request.session['cntQuesList'][-1]:
            nextQuestionRecord = quiz.models.GameQuestion.objects.get(id=request.session['attendedQuestions'][-1])
        #if cnt_ques dah the next one, now not at page after submit, but moved on to new ques page
        #fetch randomly new ques excluding prev question(s)
        else:
            request.session['cnt_ques'] = cnt_ques
            request.session['cntQuesList'].append(cnt_ques)

            questionsExceptAttended = allQuestionsPerField.exclude(id__in=attendedQuestionsIDsList).order_by('id')
            questionsExceptAttendedIDs = list(questionsExceptAttended.values_list('id', flat=True).order_by('id')) #test
            nextQuestionRecord = getRandomQuestion(cnt_ques, allQuestionsPerField, questionsExceptAttended)
            request.session['attendedQuestions'].append(nextQuestionRecord.id)
            attendedQuestionsIDsList = request.session['attendedQuestions']

            #[KIV] delete request session after 10th ques
            """ if cnt_ques == '10':
                del request.session['attendedQuestions']
                del request.session['cntQuesList'] """
    #if no cnt_ques in list (this is first ques)
    #fetch any random ques
    else:
        request.session['cnt_ques'] = cnt_ques
        request.session['cntQuesList'].append(cnt_ques)

        nextQuestionRecord = getRandomQuestion(cnt_ques, allQuestionsPerField, questionsExceptAttended)
        request.session['attendedQuestions'].append(nextQuestionRecord.id)
        attendedQuestionsIDsList = request.session['attendedQuestions']

    questionText = nextQuestionRecord.questionText
    indices = []
    questionTextOpt = []
    questionTextOnly = ""

    if 'I.' in questionText:
        indices.append(questionText.find('I.'))
        indices.append(questionText.find('II.'))
        indices.append(questionText.find('III.'))
        indices.append(questionText.find('IV.'))
    
        questionTextOnly = questionText[:indices[0]]

        for i in range(len(indices)):
            if i != len(indices)-1:
                questionTextOpt.append(questionText[indices[i]:indices[i+1]])
            else:
                questionTextOpt.append(questionText[indices[i]:])

    nextAnswerRecords = quiz.models.GameAnswer.objects.filter(questionID_id=nextQuestionRecord.id).order_by('id')
    ANSWER_CHOICES = []
    for i in range(len(nextAnswerRecords)):
        if nextAnswerRecords[i].isCorrect == True:
            ANSWER_CHOICES.append((str(nextAnswerRecords[i].isCorrect), nextAnswerRecords[i].answerText))
        else:
            ANSWER_CHOICES.append((str(nextAnswerRecords[i].isCorrect) + '_' + str(i+1), nextAnswerRecords[i].answerText))

    nextHintRecords = quiz.models.GameHint.objects.filter(questionID_id=nextQuestionRecord.id).order_by('id')
    cntHint = nextHintRecords.count()
    if cntHint > 0:
        randomHint = getRandomHint(nextHintRecords)
    else:
        randomHint = None

    isCorrect = False
    isClicked = 'False'
    hasSubmitted = False
    hasAnswered = False
    chosenAnswerText = ""

    if request.method == 'POST':
        if request.is_ajax():
            if request.POST['requestType'] == 'Next':
                isClicked = 'True'
                currentFieldPlayerSession.dateLastPlayed = datetime.now
                duration = 0
                if request.POST['timeLimit'] == '10':
                    duration = int(request.POST['endWidth'])/10
                elif request.POST['timeLimit'] == '20':
                    duration = int(request.POST['endWidth'])/5
                elif request.POST['timeLimit'] == '30':
                    duration = float(request.POST['endWidth'])/3.33
                currentFieldPlayerSession.timeTaken = currentFieldPlayerSession.timeTaken + timedelta(seconds=duration)
                currentFieldPlayerSession.save()

                result = {
                    'isClicked': isClicked,
                    'duration': duration
                    #test untuk tengok if for case pilih answer + click next, dia update duration ni je ke (BETUL),
                    #or update +timeLimit sekali (SALAH)
                }
                return JsonResponse(result)
            elif request.POST['requestType'] == 'updateBalanceHint_1':
                cntHint = int(request.POST['cntHint'])
            
                currentFieldPlayerSession.hintsUsedCount += 1
                currentFieldPlayerSession.currentPointsEarned -= nextHintRecords.get(id=int(request.POST['usedHintID'])).value
                currentFieldPlayerSession.save()

                currentPlayerTotalScoreAllField -= nextHintRecords.get(id=int(request.POST['usedHintID'])).value

                context = {
                    'cntHint': cntHint,
                    'currentFieldPlayerSession': currentFieldPlayerSession,
                    'currentPlayerTotalScoreAllField': currentPlayerTotalScoreAllField
                }
                return render(request, 'quiz/updateBalanceHint1.html', context)
            elif request.POST['requestType'] == 'updateBalanceHint_2':
                cntHint = int(request.POST['cntHint'])

                context = {
                    'cntHint': cntHint
                }
                return render(request, 'quiz/updateBalanceHint2.html', context)
            elif request.POST['requestType'] == 'updateHint_3':
                cntHint = int(request.POST['cntHint'])
                request.session['hintsUsedList'].append(int(request.POST['usedHintID']))
                updatedHintRecords = nextHintRecords.exclude(id__in=request.session['hintsUsedList']).order_by('id')
                if cntHint > 0:
                    randomHint = getRandomHint(updatedHintRecords)

                currentFieldPlayerSession = allCurrFieldPlayerSession.last()

                context = {
                    'cntHint': cntHint,
                    'currentFieldPlayerSession': currentFieldPlayerSession,
                    'randomHint': randomHint
                }
                return render(request, 'quiz/updateHint3.html', context)
            elif request.POST['requestType'] == 'updateHint_4':
                cntHint = int(request.POST['cntHint'])
                #request.session['hintsUsedList'].append(int(request.POST['usedHintID']))
                updatedHintRecords = nextHintRecords.exclude(id__in=request.session['hintsUsedList']).order_by('id')
                if cntHint > 0:
                    randomHint = getRandomHint(updatedHintRecords)

                context = {
                    'cntHint': cntHint,
                    'randomHint': randomHint
                }
                return render(request, 'quiz/updateHint4.html', context)
        else:
            hasSubmitted = True
            form = PlayForm(data=request.POST, answers=ANSWER_CHOICES)
            if form.is_valid():
                filledList = form.cleaned_data
                difficulty = nextQuestionRecord.difficulty
                
                if filledList['isClicked'] == 'True':
                    if filledList['answer_choices'] != "":
                        hasAnswered = True
                        #filledList['answer_choices'] is string, not Boolean

                        for index, choice in enumerate(ANSWER_CHOICES):
                            #choice[0] (value 'True'/'False_1'/'False_2'/'False_3') is string
                            #choice[1] (questionText) is a string

                            #since choice[0] and choice[1] are strings, and all the values (choice[0]) are unique,
                            #we can just find match of choice[0] and the filled value
                            #and assign choice[1] to chosenAnswerText right away
                            if filledList['answer_choices'] == choice[0]:
                                chosenAnswerText = choice[1]

                        if filledList['answer_choices'] == 'True':
                            isCorrect = True
                            currentFieldPlayerSession.totalCorrect += 1

                            if difficulty == 'Mudah':
                                currentFieldPlayerSession.countEasy += 1
                                currentFieldPlayerSession.countEasyCorrect += 1
                                currentFieldPlayerSession.currentPointsEarned += 6
                                currentPlayerTotalScoreAllField += 6
                            elif difficulty == 'Sederhana':
                                currentFieldPlayerSession.countMedium += 1
                                currentFieldPlayerSession.countMediumCorrect += 1
                                currentFieldPlayerSession.currentPointsEarned += 8
                                currentPlayerTotalScoreAllField += 8
                            elif difficulty == 'Sukar':
                                currentFieldPlayerSession.countHard += 1
                                currentFieldPlayerSession.countHardCorrect += 1
                                currentFieldPlayerSession.currentPointsEarned += 10
                                currentPlayerTotalScoreAllField += 10
                #if didn't click "Semak Jawapan", no matter clicked on any answer/not, add timeLimit to timeTaken (consider never submit on time)
                else:
                    currentFieldPlayerSession.timeTaken = currentFieldPlayerSession.timeTaken + timedelta(seconds=int(nextQuestionRecord.timeLimit))

                # if filledList['answer_choices'] is None, means time's up & tak jawab OR mmg tak jawab (tertekan next without click answer)
                # so hasAnswered remains False
                # but still save dateLastPlayed to current time
                # or maybe change the name to "dateFinished"???
                # note: everytime save() ni automatic yg dateLastPlayed updated to current time
                currentFieldPlayerSession.save()

                # TEST
                request.session['hasSubmittedList'].append(hasSubmitted)
                request.session['hasAnsweredList'].append(hasAnswered)
                request.session['isCorrectList'].append(isCorrect)

                context = {
                    'dashboardNav': dashboardNav,
                    'username': currentPlayerUsername,
                    'currentAvatarDetailsObject': currentAvatarDetailsObject, 
                    'user_type': user_type,
                    'user_id': user_id,
                    'test': urlTest,
                    'blog': urlBlog,
                    'quiz': urlQuiz,
                    'search': urlSearch,
                    'dashboard': urlDashboard,
                    'logout': urlLogout,
                    'form': form,
                    'currentFieldPlayerSession': currentFieldPlayerSession,
                    'currentPlayerTotalScoreAllField': currentPlayerTotalScoreAllField,
                    'nextQuestionRecord': nextQuestionRecord,
                    'nextAnswerRecords': nextAnswerRecords,
                    'nextHintRecords': nextHintRecords,
                    'cnt_ques': int(cnt_ques),
                    'isCorrect': isCorrect,
                    'field_id': field_id,
                    'questionTextOpt': questionTextOpt,
                    'questionTextOnly': questionTextOnly,
                    'chosenAnswerText': chosenAnswerText,
                    'hasAnswered': hasAnswered,
                    'hasSubmitted': hasSubmitted,
                    'sessionList': str(request.session['attendedQuestions']), #test
                    'cntQuesList': str(request.session['cntQuesList']), #test
                    'next_cnt_ques': next_cnt_ques,
                    'hasSubmittedList': str(request.session['hasSubmittedList']), #test
                    'hasAnsweredList': str(request.session['hasAnsweredList']), #test
                    'isCorrectList': str(request.session['isCorrectList']), #test
                    'questionsExceptAttendedIDs': questionsExceptAttendedIDs, #test
                    'cntHint': cntHint,
                    'randomHint': randomHint,
                    'hintsUsedList': str(request.session['hintsUsedList']), #test
                    'isClicked': filledList['isClicked']
                }
                
                return render(request, 'quiz/quizPlay.html', context)
    else:
        form = PlayForm(answers=ANSWER_CHOICES)

    context = {
        'dashboardNav': dashboardNav,
        'username': currentPlayerUsername,
        'currentAvatarDetailsObject': currentAvatarDetailsObject,
        'user_type': user_type,
        'user_id': user_id,
        'test': urlTest,
        'blog': urlBlog,
        'quiz': urlQuiz,
        'search': urlSearch,
        'dashboard': urlDashboard,
        'logout': urlLogout,
        'form': form,
        'currentFieldPlayerSession': currentFieldPlayerSession,
        'currentPlayerTotalScoreAllField': currentPlayerTotalScoreAllField,
        'nextQuestionRecord': nextQuestionRecord,
        'nextAnswerRecords': nextAnswerRecords,
        'nextHintRecords': nextHintRecords,
        'cnt_ques': int(cnt_ques),
        'isCorrect': isCorrect,
        'field_id': field_id,
        'questionTextOpt': questionTextOpt,
        'questionTextOnly': questionTextOnly,
        'chosenAnswerText': chosenAnswerText,
        'hasAnswered': hasAnswered,
        'hasSubmitted': hasSubmitted,
        'sessionList': str(request.session['attendedQuestions']), #test
        'cntQuesList': str(request.session['cntQuesList']),#test
        'next_cnt_ques': next_cnt_ques,
        'hasSubmittedList': str(request.session['hasSubmittedList']), #test
        'hasAnsweredList': str(request.session['hasAnsweredList']), #test
        'isCorrectList': str(request.session['isCorrectList']), #test
        'questionsExceptAttendedIDs': questionsExceptAttendedIDs, #test
        'cntHint': cntHint,
        'randomHint': randomHint,
        'hintsUsedList': str(request.session['hintsUsedList']), #test
        'isClicked': isClicked}

    return render(request, 'quiz/quizPlay.html', context)

def showResult(request, user_id, field_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    currentPlayerRecordObject = quiz.models.Player.objects.get(ID=user_id)
    currentPlayerUsername = currentPlayerRecordObject.ID.ID.username #give username from User model
    currentAvatarDetailsObject = currentPlayerRecordObject.avatarID
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'

    return HttpResponse("show result")

#[KIV] delete request.session after navigate away from play page
""" def check_url(sender, **kwargs):
    #original_path = reverse('quiz:play', args=(request.session['user_id'], request.session['field_id'], request.session['cnt_ques'],))
    original_path = '/pelajar/'+ request.session['user_id'] + '/mula/' + request.session['field_id'] + '/' + request.session['cnt_ques'] + '/'
    return HttpResponse('not same path')
    if HttpRequest.get_full_path(request) != original_path:
        #request.session.flush()
        return HttpResponse('not same path')
        if 'attendedQuestions' in request.session and 'cntQuesList' in request.session:
            del request.session['attendedQuestions']
            del request.session['cntQuesList']
            del request.session['user_id']
            del request.session['field_id']
            del request.session['cnt_ques']
            del request.session['hasSubmittedList']
            del request.session['hasAnsweredList']
            del request.session['isCorrectList']
            del request.session['hintsUsedList']
            return HttpResponse('done delete')
 """