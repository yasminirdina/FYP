from django.urls.base import set_script_prefix
import dashboard.models
import pTest.models
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .forms import TestForm
import pandas as pd

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

    #check logged in or not
    if currentUserRecord.isActive == False:
        return redirect('home:login')

    username = currentUserRecord.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'
   
    #if student
    if user_type == 'pelajar' and 'S' in user_id:
        context = {
            'dashboardNav': userid(user_id),
            'user_type': user_type, 
            'user_id': user_id, 
            'username': username,
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz, 
            'search': urlSearch, 
            'dashboard':urlDashboard, 
            'logout': urlLogout 
        }
        return render(request, 'pTest\pTstudentMain.html', context)

    #parent
    elif user_type == 'penjaga' and 'P' in user_id:
        # parent = dashboard.models.Parent.objects.get(ID_id=user_id)
        studentList = dashboard.models.Student.objects.filter(parentID_id = user_id).order_by('name')
        studentTakenTest = pTest.models.StudentTester.objects.all()
        # studentTakenTest = studentTakenTest.exists()
        # print(classRoom.homeroomClass)
        # print(studentList)
        print(studentTakenTest)

        context = {
            'dashboardNav': userid(user_id), 
            'user_type': user_type,
            'user_id': user_id, 
            'username': username,
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz, 
            'search': urlSearch, 
            'dashboard':urlDashboard, 
            'logout': urlLogout,
            # 'parent': parent,
            'studentList' : list(studentList),
            'studentTakenTest' : list(studentTakenTest)
        }
        return render(request, 'pTest\pTparentMain.html', context)

    #teacher
    else:
        classRoom = dashboard.models.Teacher.objects.get(ID_id=user_id)
        studentList = dashboard.models.Student.objects.filter(studentClass_id = classRoom.homeroomClass).order_by('name')
        studentTakenTest = pTest.models.StudentTester.objects.all()
        # studentTakenTest = studentTakenTest.exists()
        # print(classRoom.homeroomClass)
        # print(studentList)
        # print(studentTakenTest)

        context = {
            'dashboardNav': userid(user_id), 
            'user_type': user_type,
            'user_id': user_id, 
            'username': username,
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz, 
            'search': urlSearch, 
            'dashboard':urlDashboard, 
            'logout': urlLogout,
            'classRoom': classRoom,
            'studentList' : list(studentList),
            'studentTakenTest' : list(studentTakenTest)
        }
        return render(request, 'pTest\pTteacherMain.html', context)

def getQuestion(cnt_quest, allQuestionsPerPersonality, remainingQuestions):

    while True:
        if cnt_quest == '1':
            # chosenQuestionRecord = allQuestionsPerPersonality.filter(id=randomID).first()
            chosenQuestionRecord = allQuestionsPerPersonality.first()
        else:
            # chosenQuestionRecord = remainingQuestions.filter(id=randomID).first()
            chosenQuestionRecord = remainingQuestions.first()
        
        if chosenQuestionRecord:
            return chosenQuestionRecord

personality_id = '1'
sect_cnt_quest = '1'

def testStart(request, user_type, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    username = currentUserDetail.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'

    # currentTestStudent = pTest.models.StudentTester.objects.get(ID=user_id)
    
    #test---
    #check if the id is already exist in the student tester model or not(first time; create)
    if pTest.models.StudentTester.objects.filter(ID=user_id).exists():
        currentTestStudent = pTest.models.StudentTester.objects.get(ID=user_id)
    else:
        currentTestStudent = pTest.models.StudentTester.objects.create(
            ID_id=user_id
        )
    currentPlayerUsername = currentTestStudent.ID.ID.username #give username from User model

    # AJAX:
    #   if click "Seterusnya" and go through ajax request to this url with next cnt ques for new question
    #   or
    #       if go through form submit ajax request but taking in cnt_ques from quizPlay2.html (dynamic)
    #       if click "Semak Jawapan" OR using hints
    # NOT AJAX:
    #   initial page reload (GET) ques 1
    if request.is_ajax():
        if request.method == 'GET': #when load (GET) ques 2 and above only
            cnt_quest = request.GET.get('cnt_quest')
        elif request.method == 'POST':
            if 'requestType' not in request.POST: #after finished ajax request for when clicked "semak jawapan" (POST 1) = submit (POST 2)
                # print("???") #TEST
                cnt_quest = request.POST['cnt_quest']
            else: #for ajax post request Next and hint update stuffs
                # print("~~~") #TEST
                cnt_quest = request.session['cnt_quest']
    else:
        cnt_quest = '1' #when load (GET) ques 1
    
    global personality_id
    global sect_cnt_quest

    allPersonality = pTest.models.Personality.objects.get(id=int(personality_id))
    allCurrStudentPersonalitySession = pTest.models.StudentPersonalitySession.objects.filter(studentID_id = user_id).order_by('id')
    cntStudentPersonalitySession = allCurrStudentPersonalitySession.count()
    allQuestionsPerPersonality = pTest.models.Questions.objects.filter(section_id=int(personality_id))
    allQuestPersonalityList = len(list(allQuestionsPerPersonality))
    next_personality_id = str(int(personality_id) + 1) #test
    next_sect_cnt_quest = str(int(sect_cnt_quest) + 1) #test
    next_cnt_quest = str(int(cnt_quest) + 1)

    if int(cnt_quest) > allQuestPersonalityList:
            personality_id = next_personality_id
            cnt_quest = '1'
            sect_cnt_quest = next_sect_cnt_quest
            allPersonality = pTest.models.Personality.objects.get(id=int(personality_id))
            allQuestionsPerPersonality = pTest.models.Questions.objects.filter(section_id=int(personality_id))
            allQuestPersonalityList = len(list(allQuestionsPerPersonality))
            next_cnt_quest = str(int(cnt_quest) + 1)
            next_personality_id = str(int(personality_id) + 1) #test
            # print('dah')
            # print('personality id ' + str(personality_id))

    # Nak buat session dlm db
    if cntStudentPersonalitySession > 0:
        #if cnt_ques = 1 for GET request je (initial load), bukannya create waktu refresh page after submit first ques gak
        #note: if refresh page at first ques, still create a new record (redundancy? but the old one has default values)
        if cnt_quest == '1' and request.method != 'POST':
            if sect_cnt_quest == '1':
                currentStudentPersonalitySession = pTest.models.StudentPersonalitySession.objects.create(
                    studentID_id=user_id
                )
            else:
                currentStudentPersonalitySession = allCurrStudentPersonalitySession.last()
        else:
            currentStudentPersonalitySession = allCurrStudentPersonalitySession.last()
    else:
        currentStudentPersonalitySession = pTest.models.StudentPersonalitySession.objects.create(
            studentID_id=user_id
        )

    currentStudentAllPersonalityIDList = list(pTest.models.StudentPersonalitySession.objects.filter(studentID_id=user_id).values_list('id', flat=True).order_by('id'))
    currentStudentAllPersonalityIDList.append(currentStudentPersonalitySession.id)
    currentStudentAllPersonalityRecords = pTest.models.StudentPersonalitySession.objects.filter(id__in=currentStudentAllPersonalityIDList)
    
    #First quest:
    #If bru first soalan (initial load page for first quest) / refresh initial page tanpa jawab lagi
    #   If the essential keys exists (subset) in current session keys:
    #   else if the essential keys do not exists:
    #       give default values to request session keys to avoid guna data yg sama as prev session 
    #       for the same user AND same/diff personality
    #
    #   **So whoever starts the test, will get default keys values initially
    #     Note: opening two different tabs with same browsers with different/same user, will result in
    #           both tabs having same request.session values (combined both tabs' actions)
    #           bcs of cookies in browser.
    #     Solution: use diff browser if user want to take the test simultaneously on the same device bc of the different cookies

    required_keys = frozenset(('answeredQuestions','cntQuestList','user_id','cnt_quest','personality_id','sect_cnt_quest','hasSubmittedList','hasAnsweredList','isCorrectList')) #frozenset makes the values interchangable (values can be iterable, in this case: list)

    if cnt_quest == '1' and request.method == 'GET':
        # if sect_cnt_quest == 1:
            if required_keys <= request.session.keys():
                request.session['answeredQuestions'] = []
                request.session['cntQuestList'] = []
                request.session['user_id'] = user_id
                request.session['personality_id'] = personality_id #test
                request.session['cnt_quest'] = cnt_quest
                request.session['sect_cnt_quest'] = sect_cnt_quest #test 
                request.session['hasSubmittedList'] = []
                request.session['hasAnsweredList'] = []
                request.session['isCorrectList'] = []
                request.session['cntQuestSectList'] = [] #test
            else:
                request.session['answeredQuestions'] = []
                request.session['cntQuestList'] = []
                request.session['user_id'] = user_id
                request.session['personality_id'] = personality_id #test
                request.session['cnt_quest'] = cnt_quest
                request.session['sect_cnt_quest'] = sect_cnt_quest #test
                request.session['hasSubmittedList'] = []
                request.session['hasAnsweredList'] = []
                request.session['isCorrectList'] = []
                request.session['cntQuestSectList'] = [] #test

    answeredQuestionsIDsList = request.session['answeredQuestions']
    remainingQuestions = allQuestionsPerPersonality #for getRandomQuestion condition cnt_ques = 1
    remainingQuestionsIDs = [] #[TEST] for display in template; if cnt_ques=1 - [], else - take from ifelse below

    if len(request.session['cntQuestList']) > 0:
        #if current cnt_quest same as the latest cnt_quest in list ((GET) page refreshed by user OR (POST) after submit while displaying answers)
        #display same quest
        if cnt_quest == request.session['cntQuestList'][-1]:
            nextQuestionRecord = pTest.models.Questions.objects.get(id=request.session['answeredQuestions'][-1])
        #if cnt_quest dah the next one, now not at page after submit, but moved on to new quest page
        #fetch new quest excluding prev question(s)
        else:
            request.session['cnt_quest'] = cnt_quest
            request.session['cntQuestList'].append(cnt_quest)

            remainingQuestions = allQuestionsPerPersonality.exclude(id__in=answeredQuestionsIDsList).order_by('id')
            remainingQuestionsIDs = list(remainingQuestions.values_list('id', flat=True).order_by('id')) #test
            nextQuestionRecord = getQuestion(cnt_quest, allQuestionsPerPersonality, remainingQuestions)
            request.session['answeredQuestions'].append(nextQuestionRecord.id)
            answeredQuestionsIDsList = request.session['answeredQuestions']
    #if no cnt_quest in list (this is first ques)
    #fetch first quest
    else:
        request.session['cnt_quest'] = cnt_quest
        request.session['cntQuestList'].append(cnt_quest)

        nextQuestionRecord = getQuestion(cnt_quest, allQuestionsPerPersonality, remainingQuestions)
        request.session['answeredQuestions'].append(nextQuestionRecord.id)
        answeredQuestionsIDsList = request.session['answeredQuestions']
        
    isCorrect = False
    isClicked = 'False'
    hasSubmitted = False
    hasAnswered = False
    ANSWER_CHOICES = [('1','Ya'),('2','Tidak')]

    #test
    #Utk method post(hantar data ke db)
    if request.method == 'POST':
        if 'requestType' in request.POST:
            #utk btn semak jawapan
            if request.POST['requestType'] == 'Next':
                isClicked = 'True' #dah tekan
                # currentFieldPlayerSession.save()

                result = {
                    'isClicked': isClicked,
                    # 'duration': duration
                    #test untuk tengok if for case pilih answer + click next, dia update duration ni je ke (BETUL),
                    #or update +timeLimit sekali (SALAH)
                }
                return JsonResponse(result)

            # ni utk show result (semak jawapan) button 
            elif request.POST['requestType'] == 'updateStatusSessionRecord':
                currentStudentPersonalitySession.isFinish = True
                currentStudentPersonalitySession.save()

                return HttpResponse("Success")
        else:
            # klu x hantar request type data in ajax
            # print("Hi")
            hasSubmitted = True
            #import from form.py
            form = TestForm(data=request.POST, answers=ANSWER_CHOICES)
            #validate the data (smua data ada in each field)
            if form.is_valid():
                #cleaned_data = returns a dictionary of validated form input fields and their values
                filledList = form.cleaned_data

                # if tekan jawapan/pilihan
                if filledList['isClicked'] == 'True':
                    hasAnswered = True
                    if filledList['answer_choices'] == '1':
                        isCorrect = True
                        if int(personality_id) == 1:
                            currentStudentPersonalitySession.rSecScore += 1
                            # print('r')
                        elif int(personality_id) == 2:
                            currentStudentPersonalitySession.aSecScore += 1
                            # print('a')
                        elif int(personality_id) == 3:
                            currentStudentPersonalitySession.iSecScore += 1
                            # print('i')
                        elif int(personality_id) == 4:
                            currentStudentPersonalitySession.sSecScore += 1
                            # print('s')
                        elif int(personality_id) == 5:
                            currentStudentPersonalitySession.eSecScore += 1
                            # print('e')
                        elif int(personality_id) == 6:
                            currentStudentPersonalitySession.cSecScore += 1
                            # print('c')
                # if filledList['answer_choices'] is None, tak jawab OR mmg tak jawab (tertekan next without click answer)
                # so hasAnswered remains False and x dpt markah
                currentStudentPersonalitySession.save()

                # TEST
                request.session['hasSubmittedList'].append(hasSubmitted)
                request.session['hasAnsweredList'].append(hasAnswered)
                request.session['isCorrectList'].append(isCorrect)

                context = {
                    'user_type': user_type,
                    'user_id': user_id,
                    'form': form,
                    'currentStudentPersonalitySession': currentStudentPersonalitySession,
                    'nextQuestionRecord': nextQuestionRecord,
                    'cnt_quest': int(cnt_quest),
                    'isCorrect': isCorrect,
                    'personality_id' : int(personality_id), #test
                    'sect_cnt_quest' : int(sect_cnt_quest), #test
                    'hasAnswered': hasAnswered,
                    'hasSubmitted': hasSubmitted,
                    'sessionList': str(request.session['answeredQuestions']), #test
                    'cntQuestList': str(request.session['cntQuestList']), #test
                    'next_cnt_quest': next_cnt_quest,
                    'hasSubmittedList': str(request.session['hasSubmittedList']), #test
                    'hasAnsweredList': str(request.session['hasAnsweredList']), #test
                    'isCorrectList': str(request.session['isCorrectList']), #test
                    'remainingQuestionsIDs': remainingQuestionsIDs, #test
                    'isClicked': filledList['isClicked'],
                    'allpersonality':allPersonality,
                    'allQuestionPerPersonality': len(allQuestionsPerPersonality),
                    'next_personality_id':next_personality_id, #test
                    'next_sect_cnt_quest':next_sect_cnt_quest #test
                }
                return render(request, 'pTest/testPlay2.html', context)
    else:
        # method GET(display)/initial/other than POST/
        form = TestForm(answers=ANSWER_CHOICES)
        if request.is_ajax():
            context = {
                'user_type': user_type,
                'user_id': user_id,
                'form': form,
                'currentStudentPersonalitySession': currentStudentPersonalitySession,
                'nextQuestionRecord': nextQuestionRecord,
                'cnt_quest': int(cnt_quest),
                'isCorrect': isCorrect,
                'personality_id' : int(personality_id), #test
                'sect_cnt_quest' : int(sect_cnt_quest), #test
                'hasAnswered': hasAnswered,
                'hasSubmitted': hasSubmitted,
                'sessionList': str(request.session['answeredQuestions']), #test
                'cntQuestList': str(request.session['cntQuestList']),
                'next_cnt_quest': next_cnt_quest,
                'hasSubmittedList': str(request.session['hasSubmittedList']), #test
                'hasAnsweredList': str(request.session['hasAnsweredList']), #test
                'isCorrectList': str(request.session['isCorrectList']), #test
                'remainingQuestionsIDs': remainingQuestionsIDs, #test
                'isClicked': isClicked,
                'allPersonality': allPersonality,
                'allQuestionPerPersonality': len(allQuestionsPerPersonality),
                'next_personality_id':next_personality_id, #test
                'next_sect_cnt_quest':next_sect_cnt_quest #test
            }
            return render(request, 'pTest/testPlay2.html', context)
        else: 
            context = {
                'dashboardNav': userid(user_id),
                'username': currentPlayerUsername,
                'user_type': user_type,
                'user_id': user_id,
                'test': urlTest,
                'blog': urlBlog,
                'quiz': urlQuiz,
                'search': urlSearch,
                'dashboard': urlDashboard,
                'logout': urlLogout,
                'form': form,
                'currentStudentPersonalitySession': currentStudentPersonalitySession,
                'nextQuestionRecord': nextQuestionRecord,
                'cnt_quest': int(cnt_quest),
                'isCorrect': isCorrect,
                'personality_id' : int(personality_id), #test
                'sect_cnt_quest' : int(sect_cnt_quest), #test
                'hasAnswered': hasAnswered,
                'hasSubmitted': hasSubmitted,
                'sessionList': str(request.session['answeredQuestions']), #test
                'cntQuestList': str(request.session['cntQuestList']),
                'next_cnt_quest': next_cnt_quest,
                'hasSubmittedList': str(request.session['hasSubmittedList']), #test
                'hasAnsweredList': str(request.session['hasAnsweredList']), #test
                'isCorrectList': str(request.session['isCorrectList']), #test
                'remainingQuestionsIDs': remainingQuestionsIDs, #test
                'isClicked': isClicked,
                'allPersonality': allPersonality,
                'allQuestionPerPersonality': len(allQuestionsPerPersonality),
                'next_personality_id':next_personality_id, #test
                'next_sect_cnt_quest':next_sect_cnt_quest #test
            }
            return render(request, 'pTest/testPlay.html', context)

def testResult (request, user_type, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    username = currentUserDetail.username
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'

    #personality name
    codeName = []
    codeDesc = []
    for x in range(1,7):
        allPersonality = pTest.models.Personality.objects.get(id=x)
        codeName.append(allPersonality.personality)
        codeDesc.append(allPersonality.description)
    # print(codeName)

    #personality score
    allAttempts = pTest.models.StudentPersonalitySession.objects.filter(studentID_id = user_id).order_by('id')
    latestResult = allAttempts.last()
    allCodeResult = [
        latestResult.rSecScore,
        latestResult.aSecScore,
        latestResult.iSecScore,
        latestResult.sSecScore,
        latestResult.eSecScore,
        latestResult.cSecScore
    ]
    # print(allCodeResult)
    
    #top3 code
    listCode = {codeName[i]: allCodeResult[i] for i in range(len(codeName))}
    topCode = sorted(listCode.items(), key=lambda x: x[1], reverse=True)[:3]
    
    topName=[]
    topScore=[]
    for i in topCode:
        topName.append(i[0]),
        topScore.append(i[1])

    hollCode={
        'topName': topName,
        'topScore':topScore
    }
    # print(hollCode)

    #desc all code
    # codeName = []
    # codeDesc = []
    # for x in range(1,7):
    #     allPersonality = pTest.models.Personality.objects.get(id=x)
    #     codeName.append(allPersonality.personality)
    #     codeDesc.append(allPersonality.description)

    # # questionText = nextQuestionRecord.questionText #codeName
    # indices = []
    # questionTextOpt = []
    # questionTextOnly = ""

    # for desc in codeDesc:
    #     for len(desc):
    #         if '.' in x:
    #             indices.append(x.find('.'))
            
    #             questionTextOnly = questionText[:indices[0]]

    #             for i in range(len(indices)):
    #                 if i != len(indices)-1:
    #                     questionTextOpt.append(questionText[indices[i]:indices[i+1]])
    #                 else:
    #                     questionTextOpt.append(questionText[indices[i]:])

    context = {
        'dashboardNav': userid(user_id), 
        'user_id': user_id,
        'user_type':user_type, 
        'username': username,
        'test': urlTest, 
        'blog': urlBlog, 
        'quiz': urlQuiz, 
        'search': urlSearch, 
        'dashboard':urlDashboard, 
        'logout': urlLogout,
        'codeName':codeName,
        'codeDesc':codeDesc,
        'latestResult' : latestResult,
        'allCodeResult' : allCodeResult,
        'topCode' : topCode,
        'hollCode' : hollCode
    }
    return render(request, 'pTest\studentResult.html', context)

def nonStudentTestResult (request, user_type, user_id, student, student_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)
    currentStudentDetail = dashboard.models.Student.objects.get(ID=student_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    studentName = currentStudentDetail.name
    urlTest = 'test:index-nonadmin'
    urlBlog = 'blog:index'
    urlQuiz = 'quiz:index-student'
    urlSearch = 'search:index-nonadmin'
    urlDashboard = 'dashboard:index-nonadmin'
    urlLogout = 'dashboard:logout-confirm'

    #personality name
    codeName = []
    for x in range(1,7):
        allPersonality = pTest.models.Personality.objects.get(id=x)
        codeName.append(allPersonality.personality)
    # print(codeName)

    #personality score
    allAttempts = pTest.models.StudentPersonalitySession.objects.filter(studentID_id = student_id).order_by('id')
    latestResult = allAttempts.last()
    allCodeResult = [
        latestResult.rSecScore,
        latestResult.aSecScore,
        latestResult.iSecScore,
        latestResult.sSecScore,
        latestResult.eSecScore,
        latestResult.cSecScore
    ]
    # print(allCodeResult)
    
    #top3 code
    listCode = {codeName[i]: allCodeResult[i] for i in range(len(codeName))}
    topCode = sorted(listCode.items(), key=lambda x: x[1], reverse=True)[:3]
    
    topName=[]
    topScore=[]
    for i in topCode:
        topName.append(i[0]),
        topScore.append(i[1])

    hollCode={
        'topName': topName,
        'topScore':topScore
    }
    # print(hollCode)

    context = {
        'dashboardNav': userid(user_id), 
        'user_id': user_id,
        'user_type':user_type,
        'student_id': student_id, #test
        'student':student, #test
        'studentName': studentName,
        'test': urlTest, 
        'blog': urlBlog, 
        'quiz': urlQuiz, 
        'search': urlSearch, 
        'dashboard':urlDashboard, 
        'logout': urlLogout,
        'codeName':codeName,
        'latestResult' : latestResult,
        'allCodeResult' : allCodeResult,
        'topCode' : topCode,
        'hollCode' : hollCode
    }
    return render(request, 'pTest\pTNonStudentResult.html', context)

def testAdmin(request, user_id):
    context = {
        'dashboardNav': user_id,
        'user_id': user_id, 
    }
    return render(request, 'pTest\pTestAdmin.html', context)