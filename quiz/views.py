from datetime import datetime
import dashboard.models
import quiz.models
import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import AvatarForm, AddFieldForm, AddQuestionForm, AddAnswerForm, AddHintForm, ChangeIconForm, CustomAnswerFormSet, CustomAnswerInlineFormSet, CustomHintFormSet, EditQuestionForm, EditHintForm
from django.forms import formset_factory, inlineformset_factory
from django.db import IntegrityError, transaction
from django.contrib import messages

# Create your views here.
def quizMainAdmin(request, user_id):
    currentUserRecord = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    if user_id == 'A1':
        urlTest = 'dashboard:index-admin'
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
        urlTest = 'dashboard:index-nonadmin'
        urlBlog = 'blog:index-nonadmin'
        urlQuiz = 'quiz:index-student'
        urlSearch = 'dashboard:index-nonadmin'
        urlDashboard = 'dashboard:index-nonadmin'
        urlLogout = 'dashboard:logout-confirm'
        username = currentUserRecord.username
        title = "Future Cruise: Permainan Kuiz Penerokaan Kerjaya"
        response = "Anda tidak dibenarkan untuk mengakses halaman ini."
        context = {'title': title, 'dashboardNav': dashboardNav, 'username': username, 'response': response,
        'user_id': user_id, 'user_type': user_type, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz,
        'search': urlSearch, 'dashboard': urlDashboard, 'logout': urlLogout}
        return render(request, 'quiz\noAccessError.html', context)
        #return HttpResponse(response)

def quizMain(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = 'dashboard:index-nonadmin'
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
    #else: #is a student
    #response = ""
    request.session['student_id'] = user_id

    currentStudentDetails = dashboard.models.Student.objects.get(ID=user_id)

    #check whether the user id has a Player record already or not
    #create new Player object for that user if no Player record yet
    currentPlayerUsername = ""
    try:
        currentPlayerRecord = quiz.models.Player.objects.get(ID=user_id)
        currentPlayerUsername = currentPlayerRecord.ID.ID.username #give username from User model
    except quiz.models.Player.DoesNotExist:
        p = quiz.models.Player(ID=currentStudentDetails) #Player.ID should be an instance of Student model with default avatar
        p.save(force_insert=True)
        currentPlayerUsername = p.ID.ID.username

    response = "Anda berada di muka utama permainan kuiz."
    context = {'dashboardNav': dashboardNav, 'response': response, 'username': currentPlayerUsername, 'user_type': user_type, 'user_id': user_id,
    'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard':urlDashboard, 'logout': urlLogout}
    #context = {'response': response, 'currentPlayerUsername': currentPlayerUsername, 'student_id': student_id}
    #return HttpResponse(response % currentPlayerUsername)
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
    urlTest = 'dashboard:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'dashboard:index-nonadmin'
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
    urlTest = 'dashboard:index-nonadmin'
    urlBlog = 'blog:index-nonadmin'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'dashboard:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = ' Pelajar'
    user_type = 'pelajar'
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
            successMessage = "Avatar berjaya dikemaskini!"
            context = {'title': title, 'dashboardNav': dashboardNav, 'username': currentPlayerUsername, 'successMessage': successMessage,
            'user_type': user_type, 'user_id': user_id, 'test': urlTest, 'blog': urlBlog, 'quiz': urlQuiz, 'search': urlSearch,
            'dashboard':urlDashboard, 'logout': urlLogout}
            #return redirect('quiz:show-avatar', student_id)
            return render(request, 'quiz/successUpdate.html', context)
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
    'dashboard':urlDashboard, 'logout': urlLogout, 'form': form}
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
        urlTest = 'dashboard:index-admin'
        urlBlog = 'blog:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'dashboard:index-admin'
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
        urlTest = 'dashboard:index-nonadmin'
        urlBlog = 'blog:index-nonadmin'
        urlQuiz = 'quiz:index-student'
        urlSearch = 'dashboard:index-nonadmin'
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

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'dashboard:index-admin'
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

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'dashboard:index-admin'
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

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'dashboard:index-admin'
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

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'dashboard:index-admin'
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

    urlTest = 'dashboard:index-admin'
    urlBlog = 'blog:index-admin'
    urlQuiz = 'quiz:index-admin'
    urlSearch = 'dashboard:index-admin'
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

def play(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    response = "%s, "
    return HttpResponse(response % user_id)