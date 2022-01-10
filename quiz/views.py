from datetime import datetime
from operator import itemgetter
from re import I
import dashboard.models
import quiz.models
import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.urls import reverse
from .forms import AvatarForm, AddFieldForm, AddQuestionForm, AddAnswerForm, AddHintForm, ChangeIconForm, CustomAnswerFormSet, CustomAnswerInlineFormSet, CustomHintFormSet, EditQuestionForm, EditHintForm, ChooseFieldForm, PlayForm
from django.forms import formset_factory, inlineformset_factory
from django.db import IntegrityError, transaction
from django.contrib import messages
from random import randint
from django.core.signals import request_finished
from datetime import timedelta
from django.db.models import Sum
from collections import Counter
from wsgiref.util import FileWrapper
from django.core.files.storage import FileSystemStorage

# Create your views here.
def quizMainAdmin(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    # if user_id == 'A1':
    urlTest = 'test:index-admin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    user_type = "admin"

    allGameFields = quiz.models.GameField.objects.all().order_by('id')
    lastEdited = allGameFields.order_by('-lastEdited').first().lastEdited

    #Card 1
    countAllFields = allGameFields.count()
    countShownFields = allGameFields.filter(show=True).count()

    #Card 2
    allGameQuestions = quiz.models.GameQuestion.objects.all().order_by('id')
    shownFieldIDList = list(allGameFields.filter(show=True).values_list('id', flat=True))

    countAllQues = allGameQuestions.count()
    countShownQues = allGameQuestions.filter(fieldID_id__in=shownFieldIDList).count()

    #Card 3
    countEasyQues = allGameQuestions.filter(difficulty='Mudah').count()
    countMediumQues = allGameQuestions.filter(difficulty='Sederhana').count()
    countHardQues = allGameQuestions.filter(difficulty='Sukar').count()

    #Card 4
    allGameHints = quiz.models.GameHint.objects.all().order_by('id')
    countAllHints = allGameHints.count()

    #Card 5
    fieldNameList = list(allGameFields.values_list('name', flat=True))
    countQuesByFieldList = []

    for field in allGameFields:
        countQuesByFieldList.append(allGameQuestions.filter(fieldID_id=field.id).count())

    #Card 6
    fieldIDList = list(allGameFields.values_list('id', flat=True))
    percEasyQuesList = []
    percMediumQuesList = []
    percHardQuesList = []

    for i in range(len(fieldIDList)):
        currentFieldQues = allGameQuestions.filter(fieldID_id=fieldIDList[i])

        #Easy
        countEasy = currentFieldQues.filter(difficulty='Mudah').count()
        percEasyQuesList.append(round((countEasy/currentFieldQues.count())*100, 2))

        #Medium
        countMedium = currentFieldQues.filter(difficulty='Sederhana').count()
        percMediumQuesList.append(round((countMedium/currentFieldQues.count())*100, 2))

        #Easy
        countHard = currentFieldQues.filter(difficulty='Sukar').count()
        percHardQuesList.append(round((countHard/currentFieldQues.count())*100, 2))

    # For ALL CHARTS(field colors)
    colors = [
            "rgb(255, 129, 129)", "rgb(71, 91, 191)", "rgb(94, 208, 181)",
            "rgb(178, 143, 249)", "rgb(253, 165, 126)", "rgb(98, 194, 239)",
            "rgb(223, 129, 129)", "rgb(92, 105, 167)", "rgb(102, 188, 168)",
            "rgb(153, 135, 188)", "rgb(222, 156, 126)", "rgb(150, 200, 213)",
            "rgb(191, 128, 128)", "rgb(106, 114, 151)", "rgb(111, 168, 154)",
            "rgb(123, 95, 179)", "rgb(224, 97, 40)", "rgb(93, 194, 218)",
            "rgb(255, 75, 75)", "rgb(155, 172, 255)", "rgb(161, 230, 213)",
            "rgb(109, 79, 172)", "rgb(200, 105, 62)", "rgb(58, 158, 183)",
            "rgb(208, 36, 36)", "rgb(30, 51, 153)", "rgb(19, 134, 106)",
            "rgb(99, 80, 139)", "rgb(222, 110, 16)", "rgb(64, 136, 154)"
        ]
    
    fieldColorList = colors[:allGameFields.count()]
    # END color designation

    if request.is_ajax():
        # Card 5
        # return fieldNameList, countQuesByFieldList, fieldColorList

        # Card 6
        dist_ques_difficulty_chart_data = {
            "labels": fieldNameList,
            "datasets":[{
                "label": "Mudah",
                "data": percEasyQuesList,
                "backgroundColor": "rgb(216, 144, 211)"
            }, {
                "label": "Sederhana",
                "data": percMediumQuesList,
                "backgroundColor": "rgb(179, 97, 173)"
            }, {
                "label": "Sukar",
                "data": percHardQuesList,
                "backgroundColor": "rgb(141, 56, 135)"
            }]
        }

        data_dict = {
            "fieldNameList": fieldNameList,
            "countQuesByFieldList": countQuesByFieldList,
            "fieldColorList": fieldColorList,
            "dist_ques_difficulty_chart_data": dist_ques_difficulty_chart_data
        }

        return JsonResponse(data=data_dict, safe=False)

    context = {
        'user_id': user_id,
        'test': urlTest,
        'blog': urlBlog,
        'quiz': urlQuiz,
        'search': urlSearch,
        'dashboard': urlDashboard,
        'logout': urlLogout,
        'user_type': user_type,
        'countAllFields': countAllFields,
        'countShownFields': countShownFields,
        'countAllQues': countAllQues,
        'countShownQues': countShownQues,
        'countEasyQues': countEasyQues,
        'countMediumQues': countMediumQues,
        'countHardQues': countHardQues,
        'countAllHints': countAllHints,
        'lastEdited': lastEdited
    }
    return render(request, 'quiz\quizMainAdmin.html', context)

def quizMain(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'

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

    currentPlayerAllFieldRecords = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, isFinish=True)
    playCount = currentPlayerAllFieldRecords.count()

    response = "Anda berada di muka utama permainan kuiz."
    context = {'dashboardNav': dashboardNav, 'response': response, 'username': currentPlayerUsername, 'user_type': user_type, 'user_id': user_id,
    'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout,
    'currentAvatarDetailsObject': currentAvatarDetailsObject, 'playCount': playCount}
    return render(request, 'quiz/quizMainNonAdmin.html', context)

def showAvatar(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    currentPlayerRecordObject = quiz.models.Player.objects.get(ID=user_id)
    currentPlayerUsername = currentPlayerRecordObject.ID.ID.username #give username from User model
    currentAvatarDetailsObject = currentPlayerRecordObject.avatarID
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'

    context = {'dashboardNav': dashboardNav, 'username': currentPlayerUsername, 'currentAvatarDetailsObject': currentAvatarDetailsObject,
    'user_type': user_type, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout}
    return render(request, 'quiz/showAvatar.html', context)

def editAvatar(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    currentPlayerRecord = quiz.models.Player.objects.get(ID=user_id)
    currentPlayerUsername = currentPlayerRecord.ID.ID.username #give username from User model
    currentAvatarDetailsObject = currentPlayerRecord.avatarID
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'
    isSubmitted = False

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

            allAvatarDetails = quiz.models.AvatarGenderImageFinal.objects.all()
            for x in allAvatarDetails:
                if x.avatarID.careerName == form.cleaned_data['avatarID'].careerName:
                    if x.avatarGender.avatarGender == form.cleaned_data['avatarGender'].avatarGender:
                        currentPlayerRecord.avatarID = x
                        break
            currentPlayerRecord.save()
            title = "Future Cruise: Tetapan Avatar"
            isSubmitted = True
            context = {'title': title, 'dashboardNav': dashboardNav, 'username': currentPlayerUsername,
            'user_type': user_type, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
            'dashboard':urlDashboard, 'logout': urlLogout}
    else:
        currentPlayerAvatarID = currentPlayerRecord.avatarID.id
        currentAvatarDetails = quiz.models.AvatarGenderImageFinal.objects.get(id=currentPlayerAvatarID)
        avatarID = currentAvatarDetails.avatarID.id
        workplace = currentAvatarDetails.workplace.id
        avatarGender = currentAvatarDetails.avatarGender.id
        imageURL = currentAvatarDetails.imageURL.id
        form = AvatarForm(initial={'avatarID': avatarID, 'workplace': workplace, 'avatarGender': avatarGender,
        'imageURL': imageURL})

    context = {'dashboardNav': dashboardNav, 'username': currentPlayerUsername, 'currentAvatarDetailsObject': currentAvatarDetailsObject,
    'user_type': user_type, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard':urlDashboard, 'logout': urlLogout, 'form': form, 'isSubmitted': isSubmitted}
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
        urlBlog = 'blog:index'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
        urlLogout = 'dashboard:logout-confirm'
        urlShowQuestion = 'quiz:show-question'
        urlChangeIcon = 'quiz:change-icon'
        user_type = "admin"

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
                else:
                    context = {'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
                    'dashboard': urlDashboard, 'logout': urlLogout, 'user_type': user_type, 'showquestion': urlShowQuestion, 'changeicon': urlChangeIcon,
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
        context = {'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
        'dashboard': urlDashboard, 'logout': urlLogout, 'user_type': user_type, 'showquestion': urlShowQuestion, 'changeicon': urlChangeIcon,
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
        urlBlog = 'blog:index'
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
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    allImageField = quiz.models.ImageField.objects.all()
    user_type = "admin"

    #get all objects (image records) in ImageField table
    allFieldImage = quiz.models.ImageField.objects.all().order_by('id')
    #get values_list of imageURL in ImageField, ordered by id
    imageURLList = list(allFieldImage.values_list('imageURL', flat=True).order_by('id'))

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
                'dashboard': urlDashboard, 'logout': urlLogout, 'user_type': user_type, 'errorMessage': errorMessage,
                'allImageField': allImageField, 'form': form,'imageURLList': imageURLList}
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
                    'dashboard': urlDashboard, 'logout': urlLogout, 'user_type': user_type, 'errorMessage': errorMessage,
                    'allImageField': allImageField, 'form': form, 'imageURLList': imageURLList}
                    return render(request, 'quiz/addField.html', context)
                else:
                    quiz.models.GameField.objects.create(name=filledList['name'], imageURL=selectedImageRecord)
                    return redirect('quiz:show-field', user_id)
    else:
        form = AddFieldForm()

    context = {'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard': urlDashboard, 'logout': urlLogout, 'user_type': user_type, 'allImageField': allImageField, 'form': form,
    'imageURLList': imageURLList}
    return render(request, 'quiz/addField.html', context)

def changeIcon(request, user_id, field_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    allGameFields = quiz.models.GameField.objects.all()
    currentGameFieldRecord = allGameFields.get(id=field_id)
    currentGameFieldName = currentGameFieldRecord.name
    user_type = "admin"

    #get all objects (image records) in ImageField table
    allFieldImage = quiz.models.ImageField.objects.all().order_by('id')
    #get values_list of imageURL in ImageField, ordered by id
    imageURLList = list(allFieldImage.values_list('imageURL', flat=True).order_by('id'))

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
                'dashboard': urlDashboard, 'logout': urlLogout, 'user_type': user_type, 'errorMessage': errorMessage,
                'currentGameFieldName': currentGameFieldName, 'form': form, 'imageURLList': imageURLList}
                return render(request, 'quiz/changeIcon.html', context)
            else:
                currentGameFieldRecord.imageURL = selectedImageRecord
                currentGameFieldRecord.save()
                return redirect('quiz:show-field', user_id)
    else:
        form = ChangeIconForm()

    context = {'user_id': user_id, 'field_id': field_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard': urlDashboard, 'logout': urlLogout, 'user_type': user_type, 'currentGameFieldName': currentGameFieldName, 'form': form,
    'imageURLList': imageURLList}
    return render(request, 'quiz/changeIcon.html', context)

def showQuestion(request, user_id, field_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index'
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
    user_type = "admin"

    if request.method == 'GET': # If the form is submitted / refresh page
        search_text = request.GET.get('kotak_carian', None)
        filter_selected = request.GET.get('difficulty', None)
        #if admin ada search soalan (search form submitted = GET request)
        if search_text is not None:
            gameQuestions = gameQuestions.filter(questionText__icontains=search_text) #either exist or not (found or not)
            #if admin select filter difficulty selain value 'Tiada'
            if filter_selected != 'Tiada':
                gameQuestions = gameQuestions.filter(difficulty=filter_selected)
            
    #if admin tak search soalan AND tak filter difficulty (refresh page = GET request)
    context = {'user_id': user_id, 'field_id': field_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
    'dashboard': urlDashboard, 'logout': urlLogout, 'user_type': user_type, 'currentGameFieldName': currentGameFieldName,
    'gameQuestions': gameQuestions, 'search_text': search_text, 'filter_selected': filter_selected,
    'gameQuestionsCount': gameQuestions.count(), 'allGameQuesAns': allGameQuesAns, 'allGameHintQuesIDList': allGameHintQuesIDList}
    return render(request, 'quiz/showQuestion.html', context)

def addQuestion(request, user_id, field_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    allGameFields = quiz.models.GameField.objects.all()
    currentGameFieldRecord = allGameFields.get(id=field_id)
    currentGameFieldName = currentGameFieldRecord.name
    user_type = "admin"

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
    'dashboard': urlDashboard, 'logout': urlLogout,'user_type': user_type, 'currentGameFieldName': currentGameFieldName, 'questionForm': questionForm,
    'answer_formset': answer_formset, 'hint_formset': hint_formset, 'errormsg1': errormsg1, 'errormsg2': errormsg2,
    'errormsg3': errormsg3, 'errormsg4': errormsg4, 'errormsg5': errormsg5}
    return render(request, 'quiz/addQuestion.html', context) 

def editQuestion(request, user_id, field_id, question_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'test:index-admin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'search:index-admin'
    urlDashboard = 'dashboard:index-admin'
    urlLogout = 'dashboard:logout-confirm'
    allGameFields = quiz.models.GameField.objects.all()
    user_type = "admin"

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
    'dashboard': urlDashboard, 'logout': urlLogout, 'user_type': user_type, 'currentGameFieldName': currentGameFieldName, 'questionForm': questionForm,
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
    urlBlog = 'blog:index'
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
        if cnt_ques == '1':
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

# def play(request, user_id, field_id, cnt_ques):
def play(request, user_id, field_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    currentPlayerRecordObject = quiz.models.Player.objects.get(ID=user_id)
    currentPlayerUsername = currentPlayerRecordObject.ID.ID.username #give username from User model
    currentAvatarDetailsObject = currentPlayerRecordObject.avatarID
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'

    currentFieldRecord = quiz.models.GameField.objects.get(id=field_id)

    # AJAX:
    #   if click "Seterusnya" and go through ajax request to this url with next cnt ques for new question
    #   or
    #       if go through form submit ajax request but taking in cnt_ques from quizPlay2.html (dynamic)
    #       if click "Semak Jawapan" OR using hints
    # NOT AJAX:
    #   initial page reload (GET) ques 1
    if request.is_ajax():
        if request.method == 'GET': #when load (GET) ques 2 and above only
            cnt_ques = request.GET.get('cnt_ques')
        elif request.method == 'POST':
            if 'requestType' not in request.POST: #after finished ajax request for when clicked "semak jawapan" (POST 1) = submit (POST 2)
                print("???") #TEST
                cnt_ques = request.POST['cnt_ques']
            else: #for ajax post request Next and hint update stuffs
                print("~~~") #TEST
                cnt_ques = request.session['cnt_ques']
    else:
        cnt_ques = '1' #when load (GET) ques 1

    # real one
    allCurrFieldPlayerSession = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, fieldID_id=field_id).order_by('id')
    cntFieldPlayerSession = allCurrFieldPlayerSession.count()

    if cntFieldPlayerSession > 0:
        #if cnt_ques = 1 for GET request je (initial load), bukannya create waktu refresh page after submit first ques gak
        #note: if refresh page at first ques, still create a new record (redundancy? but the old one has default values)
        if cnt_ques == '1' and request.method != 'POST': 
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

    currentPlayerAllFieldIDList = list(quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, isFinish=True).values_list('id', flat=True).order_by('id'))
    currentPlayerAllFieldIDList.append(currentFieldPlayerSession.id)
    currentPlayerAllFieldRecords = quiz.models.FieldPlayerSession.objects.filter(id__in=currentPlayerAllFieldIDList)
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
    #note: opening two different tabs with same browsers with different/same user and/or field, will result in
    #      both tabs having same request.session values (combined both tabs' actions)
    #      bcs of cookies in browser.
    #Solution: if ever want to play simultaneously on same device, need to open diff browsers bc different cookies
    required_keys = frozenset(('attendedQuestions','cntQuesList','user_id','field_id','cnt_ques','hasSubmittedList',
    'hasAnsweredList', 'isCorrectList', 'hintsUsedList', 'randomHintID'))

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
            request.session['randomHintID'] = [] 
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
            request.session['randomHintID'] = [] 

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
        if 'requestType' in request.POST:
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
                    request.session['randomHintID'] = randomHint.id

                currentFieldPlayerSession = allCurrFieldPlayerSession.last()

                context = {
                    'cntHint': cntHint,
                    'currentFieldPlayerSession': currentFieldPlayerSession,
                    'randomHint': randomHint
                }
                return render(request, 'quiz/updateHint3.html', context)
            elif request.POST['requestType'] == 'updateHint_4':
                cntHint = int(request.POST['cntHint'])
                # updatedHintRecords = nextHintRecords.exclude(id__in=request.session['hintsUsedList']).order_by('id')
                if cntHint > 0:
                    # randomHint = getRandomHint(updatedHintRecords)
                    randomHint = nextHintRecords.get(id=request.session['randomHintID'])

                context = {
                    'cntHint': cntHint,
                    'randomHint': randomHint
                }
                return render(request, 'quiz/updateHint4.html', context)
            elif request.POST['requestType'] == 'updateStatusSessionRecord':
                currentFieldPlayerSession.isFinish = True
                currentFieldPlayerSession.save()

                return HttpResponse("Success")
        else:
            print("Hi")
            hasSubmitted = True
            form = PlayForm(data=request.POST, answers=ANSWER_CHOICES)
            if form.is_valid():
                filledList = form.cleaned_data
                difficulty = nextQuestionRecord.difficulty
                
                if difficulty == 'Mudah':
                    currentFieldPlayerSession.countEasy += 1
                elif difficulty == 'Sederhana':
                    currentFieldPlayerSession.countMedium += 1
                elif difficulty == 'Sukar':
                    currentFieldPlayerSession.countHard += 1

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
                                currentFieldPlayerSession.countEasyCorrect += 1
                                currentFieldPlayerSession.currentPointsEarned += 6
                                currentPlayerTotalScoreAllField += 6
                            elif difficulty == 'Sederhana':
                                currentFieldPlayerSession.countMediumCorrect += 1
                                currentFieldPlayerSession.currentPointsEarned += 8
                                currentPlayerTotalScoreAllField += 8
                            elif difficulty == 'Sukar':
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
                    'user_id': user_id,
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

                return render(request, 'quiz/quizPlay2.html', context)
    else:
        form = PlayForm(answers=ANSWER_CHOICES)
        if request.is_ajax():
            context = {
                'user_id': user_id,
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
                'isClicked': isClicked
            }
            return render(request, 'quiz/quizPlay2.html', context)
        else: 
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
                'isClicked': isClicked
            }
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
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'

    currentFieldRecord = quiz.models.GameField.objects.get(id=field_id)

    allCurrFieldPlayerSession = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, fieldID_id=field_id).order_by('id')
    cntFieldPlayerSession = allCurrFieldPlayerSession.count()
    currentFieldPlayerSession = allCurrFieldPlayerSession.last()

    currentPlayerAllFieldRecords = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, isFinish=True)
    currentPlayerTotalScoreAllFieldList = list(currentPlayerAllFieldRecords.values_list('currentPointsEarned', flat=True))
    currentPlayerTotalScoreAllField = 0
    for score in currentPlayerTotalScoreAllFieldList:
        currentPlayerTotalScoreAllField += score

    points = []
    points.append((currentFieldPlayerSession.countEasyCorrect)*6)
    points.append((currentFieldPlayerSession.countEasy)*6)
    points.append((currentFieldPlayerSession.countMediumCorrect)*8)
    points.append((currentFieldPlayerSession.countMedium)*8)
    points.append((currentFieldPlayerSession.countHardCorrect)*10)
    points.append((currentFieldPlayerSession.countHard)*10)

    fullScore = points[1] + points[3] + points[5]
    if fullScore > 0:
        percentageScore = round((currentFieldPlayerSession.currentPointsEarned/fullScore)*100, 2)
    else:
        percentageScore = 0

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
        'field_id': field_id,
        'currentFieldRecord': currentFieldRecord,
        'points': points,
        'fullScore': fullScore,
        'percentageScore': percentageScore,
        'currentFieldPlayerSession': currentFieldPlayerSession,
        'currentPlayerTotalScoreAllField': currentPlayerTotalScoreAllField
    }

    return render(request, 'quiz/showResult.html', context)

def seeRanking(request, user_id, field_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    currentPlayerRecordObject = quiz.models.Player.objects.get(ID=user_id)
    currentPlayerUsername = currentPlayerRecordObject.ID.ID.username #give username from User model
    currentAvatarDetailsObject = currentPlayerRecordObject.avatarID
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'

    currentFieldRecord = quiz.models.GameField.objects.get(id=field_id)

    allCurrFieldPlayerSession = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, fieldID_id=field_id).order_by('id')
    cntFieldPlayerSession = allCurrFieldPlayerSession.count()
    currentFieldPlayerSession = allCurrFieldPlayerSession.last()

    currentPlayerAllFieldRecords = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, isFinish=True)
    currentPlayerTotalScoreAllFieldList = list(currentPlayerAllFieldRecords.values_list('currentPointsEarned', flat=True))
    currentPlayerTotalScoreAllField = 0
    for score in currentPlayerTotalScoreAllFieldList:
        currentPlayerTotalScoreAllField += score

    shownFields = quiz.models.GameField.objects.filter(show=True).order_by('name')
    playerFieldRecords = []
    indPlayer = []
    playerScoreDict = {}
    allPlayerRecords = []

    if request.method == 'GET':
        if request.is_ajax():
            field_selected = request.GET.get('field', None)
            currentFieldinSession = quiz.models.FieldPlayerSession.objects.filter(fieldID_id=int(field_selected), isFinish=True).order_by('id')
            playerIDList = list(currentFieldinSession.values_list('fieldPlayerID', flat=True).distinct().order_by())

            for playerID in playerIDList:
                indPlayer.append(quiz.models.Player.objects.get(ID=playerID).avatarID.imageURL)
                indPlayer.append(quiz.models.Player.objects.get(ID=playerID).ID.ID.username)
                playerScoreDict = currentFieldinSession.filter(fieldPlayerID_id=playerID).aggregate(Sum('currentPointsEarned'))
                indPlayer.append(playerScoreDict['currentPointsEarned__sum'])
                playerFieldRecords.append(indPlayer)
                indPlayer = []

            playerFieldRecords = sorted(playerFieldRecords, key=itemgetter(2), reverse=True)

            context = {
                'shownFields': shownFields,
                'field_selected': int(field_selected),
                'playerFieldRecords': playerFieldRecords
            }
            return render(request, 'quiz/selectedField.html', context)
        else: #refreshed
            #for div-field
            currentFieldinSession = quiz.models.FieldPlayerSession.objects.filter(fieldID_id=field_id, isFinish=True).order_by('id')
            playerIDList = list(currentFieldinSession.values_list('fieldPlayerID', flat=True).distinct().order_by())

            for playerID in playerIDList:
                indPlayer.append(quiz.models.Player.objects.get(ID=playerID).avatarID.imageURL)
                indPlayer.append(quiz.models.Player.objects.get(ID=playerID).ID.ID.username)
                playerScoreDict = currentFieldinSession.filter(fieldPlayerID_id=playerID).aggregate(Sum('currentPointsEarned'))
                indPlayer.append(playerScoreDict['currentPointsEarned__sum'])
                playerFieldRecords.append(indPlayer)
                indPlayer = []
            
            playerFieldRecords = sorted(playerFieldRecords, key=itemgetter(2), reverse=True)

            #for div-overall
            #not finish and not start play = not played
            #only finished sessions counted
            allCompletedSession = quiz.models.FieldPlayerSession.objects.filter(isFinish=True).order_by('id')
            allPlayerIDList = list(quiz.models.Player.objects.values_list('ID', flat=True).order_by('ID'))
            playedPlayerIDList = list(allCompletedSession.values_list('fieldPlayerID', flat=True).distinct().order_by())

            for playerID in allPlayerIDList:
                indPlayer.append(quiz.models.Player.objects.get(ID=playerID).avatarID.imageURL)
                indPlayer.append(quiz.models.Player.objects.get(ID=playerID).ID.ID.username)
                if playerID in playedPlayerIDList:
                    playerScoreDict = allCompletedSession.filter(fieldPlayerID=playerID).aggregate(Sum('currentPointsEarned'))
                    indPlayer.append(playerScoreDict['currentPointsEarned__sum'])
                    indPlayer.append(True) #hasPlayed
                else:
                    indPlayer.append(0)
                    indPlayer.append(False)
                allPlayerRecords.append(indPlayer)
                indPlayer = []

            allPlayerRecords = sorted(allPlayerRecords, key=itemgetter(2), reverse=True)

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
        'field_id': int(field_id),
        'currentFieldRecord': currentFieldRecord,
        'currentFieldPlayerSession': currentFieldPlayerSession,
        'currentPlayerTotalScoreAllField': currentPlayerTotalScoreAllField,
        'shownFields': shownFields,
        'playerFieldRecords': playerFieldRecords,
        'allPlayerRecords': allPlayerRecords
    }

    return render(request, 'quiz/seeRanking.html', context)

def seeStatistic(request, user_id, field_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    currentPlayerRecordObject = quiz.models.Player.objects.get(ID=user_id)
    currentPlayerUsername = currentPlayerRecordObject.ID.ID.username #give username from User model
    currentAvatarDetailsObject = currentPlayerRecordObject.avatarID
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'

    currentFieldRecord = quiz.models.GameField.objects.get(id=field_id)

    allCurrFieldPlayerSession = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, fieldID_id=field_id).order_by('id')
    cntFieldPlayerSession = allCurrFieldPlayerSession.count()
    currentFieldPlayerSession = allCurrFieldPlayerSession.last()

    currentPlayerAllFieldRecords = quiz.models.FieldPlayerSession.objects.filter(fieldPlayerID_id=user_id, isFinish=True)
    currentPlayerTotalScoreAllFieldList = list(currentPlayerAllFieldRecords.values_list('currentPointsEarned', flat=True))

    # From main page, bcs we use field id = 1, but the player did not have any record with field id 1 (they have others),
    # we take the last record in fieldplayersession for that player (no matter what field)
    if currentFieldPlayerSession == None:
        currentFieldPlayerSession = currentPlayerAllFieldRecords.last()

    #For DIV 1: game-perf
    #Card 1: Total No of Plays
    playCount = currentPlayerAllFieldRecords.count()

    #Card 2: Total Score All Fields
    currentPlayerTotalScoreAllField = 0
    for score in currentPlayerTotalScoreAllFieldList:
        currentPlayerTotalScoreAllField += score

    #Card 3: Average score per session (all fields)
    avgSessionScore = int(round(currentPlayerTotalScoreAllField/playCount, 0))

    #Card 4: Average hints used per session (all fields)
    totalHintsUsedDict = currentPlayerAllFieldRecords.aggregate(Sum('hintsUsedCount'))
    avgHintsUsed = int(round(totalHintsUsedDict['hintsUsedCount__sum']/playCount, 0))

    #Card 5: Last Played Time
    lastPlayedTime = currentFieldPlayerSession.dateLastPlayed #Format to string HH:mmPM, DD/MM/YYYY

    #Card 6: Average time taken per session (all fields)
    timeList = list(currentPlayerAllFieldRecords.values_list('timeTaken', flat=True))
    totalTimeTaken = timedelta(seconds=sum(td.total_seconds() for td in timeList))
    avgSessionTimeTaken = int(round(totalTimeTaken.total_seconds()/playCount, 0))

    minutes = avgSessionTimeTaken // 60
    seconds = avgSessionTimeTaken % 60

    if minutes != 0 and seconds != 0:
        avgSessionTimeTaken = '{} minit {} saat'.format(minutes, seconds)
    elif minutes == 0:
        avgSessionTimeTaken = '{} saat'.format(seconds)
    elif seconds == 0:
        avgSessionTimeTaken = '{} minit'.format(minutes)

    #Card 7: (Bar Chart) Most Played Field
    fieldIDList = list(currentPlayerAllFieldRecords.order_by('fieldID_id').values_list("fieldID_id", flat=True).distinct("fieldID_id"))
    allGameFields = quiz.models.GameField.objects.filter(id__in=fieldIDList).order_by('id')

    fieldPlayedCountList = []
    fieldNameList = []
    fieldName_CountDict = {}

    for fieldID in fieldIDList:
        fieldPlayedCountList.append(0)

    for session in currentPlayerAllFieldRecords:
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

    # Card 8
    fieldEasyCorrectList = []
    fieldMediumCorrectList = []
    fieldHardCorrectList = []

    for i in range(len(fieldIDList)):
        #Easy
        totalCurrentFieldEasyDict = currentPlayerAllFieldRecords.filter(fieldID_id=fieldIDList[i]).aggregate(Sum('countEasy'))
        totalCurrentFieldEasyCorrectDict = currentPlayerAllFieldRecords.filter(fieldID_id=fieldIDList[i]).aggregate(Sum('countEasyCorrect'))
        
        if totalCurrentFieldEasyCorrectDict['countEasyCorrect__sum'] > 0:
            percEasy = round((totalCurrentFieldEasyCorrectDict['countEasyCorrect__sum']/totalCurrentFieldEasyDict['countEasy__sum'])*100, 2)
        else:
            percEasy = 0

        print("id: " + str(i) + ", percEasy: " + str(percEasy))
        fieldEasyCorrectList.append(percEasy)

        #Medium
        totalCurrentFieldMediumDict = currentPlayerAllFieldRecords.filter(fieldID_id=fieldIDList[i]).aggregate(Sum('countMedium'))
        totalCurrentFieldMediumCorrectDict = currentPlayerAllFieldRecords.filter(fieldID_id=fieldIDList[i]).aggregate(Sum('countMediumCorrect'))
        
        if totalCurrentFieldMediumCorrectDict['countMediumCorrect__sum'] > 0:
            percMedium = round((totalCurrentFieldMediumCorrectDict['countMediumCorrect__sum']/totalCurrentFieldMediumDict['countMedium__sum'])*100, 2)
        else:
            percMedium = 0

        print("id: " + str(i) + ", percMedium: " + str(percMedium))
        fieldMediumCorrectList.append(percMedium)

        #Hard
        totalCurrentFieldHardDict = currentPlayerAllFieldRecords.filter(fieldID_id=fieldIDList[i]).aggregate(Sum('countHard'))
        totalCurrentFieldHardCorrectDict = currentPlayerAllFieldRecords.filter(fieldID_id=fieldIDList[i]).aggregate(Sum('countHardCorrect'))
        
        if totalCurrentFieldHardCorrectDict['countHardCorrect__sum'] > 0:
            percHard = round((totalCurrentFieldHardCorrectDict['countHardCorrect__sum']/totalCurrentFieldHardDict['countHard__sum'])*100, 2)
        else:
            percHard = 0

        print("id: " + str(i) + ", percHard: " + str(percHard))
        fieldHardCorrectList.append(percHard)

    # Card 9, 10 & 11
    avgSessionScoreByFieldList = []
    avgSessionHintByFieldList = []
    avgSessionTimeTakenByFieldList = []

    for i in range(len(fieldIDList)):
        currentIterFieldRecords = currentPlayerAllFieldRecords.filter(fieldID_id=fieldIDList[i])
        currentFieldSessionCount = currentIterFieldRecords.count()

        totalScoreCurrentFieldDict = currentIterFieldRecords.aggregate(Sum('currentPointsEarned'))
        totalHintCurrentFieldDict = currentIterFieldRecords.aggregate(Sum('hintsUsedCount'))
        timeList = list(currentIterFieldRecords.values_list('timeTaken', flat=True))
        totalTimeTaken = timedelta(seconds=sum(td.total_seconds() for td in timeList))
        avgTimeTaken_unformatted = int(round(totalTimeTaken.total_seconds()/currentFieldSessionCount, 0))

        avgSessionScoreByFieldList.append(int(round(totalScoreCurrentFieldDict['currentPointsEarned__sum']/currentFieldSessionCount, 0)))
        avgSessionHintByFieldList.append(int(round(totalHintCurrentFieldDict['hintsUsedCount__sum']/currentFieldSessionCount, 0)))
        avgSessionTimeTakenByFieldList.append(avgTimeTaken_unformatted)
    
    #For DIV 2: career-rec
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

    # For ALL CHARTS(field colors)
    colors = [
            "rgb(255, 129, 129)", "rgb(71, 91, 191)", "rgb(94, 208, 181)",
            "rgb(178, 143, 249)", "rgb(253, 165, 126)", "rgb(98, 194, 239)",
            "rgb(223, 129, 129)", "rgb(92, 105, 167)", "rgb(102, 188, 168)",
            "rgb(153, 135, 188)", "rgb(222, 156, 126)", "rgb(150, 200, 213)",
            "rgb(191, 128, 128)", "rgb(106, 114, 151)", "rgb(111, 168, 154)",
            "rgb(123, 95, 179)", "rgb(224, 97, 40)", "rgb(93, 194, 218)",
            "rgb(255, 75, 75)", "rgb(155, 172, 255)", "rgb(161, 230, 213)",
            "rgb(109, 79, 172)", "rgb(200, 105, 62)", "rgb(58, 158, 183)",
            "rgb(208, 36, 36)", "rgb(30, 51, 153)", "rgb(19, 134, 106)",
            "rgb(99, 80, 139)", "rgb(222, 110, 16)", "rgb(64, 136, 154)"
        ]

    allGameFieldColorsDict = {}

    for i in range(len(allGameFields)):
        allGameFieldColorsDict[allGameFields[i].name] = colors[i]
    
    playedFieldColorList = colors[:len(fieldNameList)]
    # END color designation

    if request.is_ajax():
        # Card 7
        most_played_field_chart_data = {
            "labels": list(fieldName_CountDict.keys()),
            "datasets":[{
                "label": "Purata Petunjuk Digunakan",
                "data": list(fieldName_CountDict.values()),
                "backgroundColor": playedFieldColorList
            }]
        }

        # Card 8
        dist_correct_answers_chart_data = {
            "labels": list(fieldName_CountDict.keys()),
            "datasets":[{
                "label": "Mudah",
                "data": fieldEasyCorrectList,
                "backgroundColor": "rgb(216, 144, 211)"
            }, {
                "label": "Sederhana",
                "data": fieldMediumCorrectList,
                "backgroundColor": "rgb(179, 97, 173)"
            }, {
                "label": "Sukar",
                "data": fieldHardCorrectList,
                "backgroundColor": "rgb(141, 56, 135)"
            }]
        }
        
        # Card 9
        avg_field_session_score_chart_data = {
            "labels": list(fieldName_CountDict.keys()),
            "datasets":[{ 
                "label": "Purata Markah per Sesi",
                "data": avgSessionScoreByFieldList,
                "backgroundColor": playedFieldColorList
            }]
        }

        # Card 10
        avg_field_session_hints_chart_data = {
            "labels": list(fieldName_CountDict.keys()),
            "datasets":[{ 
                "label": "Purata Petunjuk Digunakan per Sesi",
                "data": avgSessionHintByFieldList,
                "backgroundColor": playedFieldColorList
            }]
        }

        # Card 11
        avg_field_session_time_chart_data = {
            "labels": list(fieldName_CountDict.keys()),
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
            "dist_correct_answers_chart_data": dist_correct_answers_chart_data,
            "avg_field_session_score_chart_data": avg_field_session_score_chart_data,
            "avg_field_session_hints_chart_data": avg_field_session_hints_chart_data,
            "avg_field_session_time_chart_data": avg_field_session_time_chart_data
        }

        return JsonResponse(data=data_dict, safe=False)

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
        'field_id': int(field_id),
        'currentFieldRecord': currentFieldRecord,
        'currentFieldPlayerSession': currentFieldPlayerSession,
        'playCount': playCount,
        'currentPlayerTotalScoreAllField': currentPlayerTotalScoreAllField,
        'avgSessionScore': avgSessionScore,
        'avgHintsUsed': avgHintsUsed,
        'lastPlayedTime': lastPlayedTime,
        'avgSessionTimeTaken': avgSessionTimeTaken,
        'three_highest_fieldName': three_highest_fieldName,
        'three_highest_fieldImage': three_highest_fieldImage,
        'recCnt': len(three_highest_fieldName)
    }

    return render(request, 'quiz/seeStatistic.html', context)