from django.urls.base import set_script_prefix
import dashboard.models
import pTest.models
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .forms import TestForm


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
            'logout': urlLogout
        }
        return render(request, 'pTest\pTestNonStudent.html', context)

def getQuestion(cnt_quest, allQuestionsPerPersonality, remainingQuestions):

    while True:
        if cnt_quest == '1':
            # chosenQuestionRecord = allQuestionsPerPersonality.filter(id=randomID).first()
            chosenQuestionRecord = allQuestionsPerPersonality.first()
        else:
            # chosenQuestionRecord = remainingQuestions.filter(id=randomID).first()
            chosenQuestionRecord = remainingQuestions
        
        if chosenQuestionRecord:
            return chosenQuestionRecord

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

    #if student
    if user_type == 'pelajar' and 'S' in user_id:
        #edit------------------------------------
        cnt_quest=1 #test
        currentTestStudent = pTest.models.Student.objects.get(ID=user_id)
        currentPlayerUsername = currentTestStudent.ID.ID.username #give username from User model
        # sectionQuestion = pTest.models.Personality.objects.all()
        # allQuestions = pTest.models.Questions.objects.all()
        # allQuestionsPerSection = pTest.models.Questions.objects.filter(section_id = section_id)
        allQuestionsPerPersonality = pTest.models.Questions.objects.all()
        #------------------------------------

        # Ajax step
        # real one step (kiv)

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

        # required_keys = frozenset(('attendedQuestions','cntQuesList','user_id','field_id','cnt_ques','hasSubmittedList',
        # 'hasAnsweredList', 'isCorrectList', 'hintsUsedList', 'randomHintID')) <- min's reference
        required_keys = frozenset(('answeredQuestions','cntQuestList','user_id','cnt_quest')) #frozenset makes the values interchangable (values can be iterable, in this case: list)

        if cnt_quest == '1' and request.method == 'GET':
            if required_keys <= request.session.keys():
                request.session['answeredQuestions'] = []
                request.session['cntQuestList'] = []
                request.session['user_id'] = user_id
                request.session['cnt_quest'] = cnt_quest 
            else:
                request.session['answeredQuestions'] = []
                request.session['cntQuestList'] = []
                request.session['user_id'] = user_id
                request.session['cnt_quest'] = cnt_quest

        answeredQuestionsIDsList = request.session['answeredQuestions']
        remainingQuestions = allQuestionsPerPersonality #for getRandomQuestion condition cnt_ques = 1
        remainingQuestionsIDs = [] #[TEST] for display in template; if cnt_ques=1 - [], else - take from ifelse below

        #if cntQuestList > 1 (not the first quest)
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

        questionText = nextQuestionRecord.questionText #kiv
        # indices = []
        # questionTextOpt = []
        # questionTextOnly = ""

        isCorrect = False
        isClicked = 'False'
        hasSubmitted = False
        hasAnswered = False
        ANSWER_CHOICES = ['Ya','Tidak']

        #from -real one part (just test rn)
        currentStudentPersonalitySession = pTest.models.StudentPersonalitySession.objects.create(
                fieldPlayerID_id=user_id,
                # fieldID_id=field_id
        )

        #test
        if request.method == 'POST':
            if 'requestType' in request.POST:
                if request.POST['requestType'] == 'Next':
                    isClicked = 'True'
                    # currentFieldPlayerSession.dateLastPlayed = datetime.now
                    # duration = 0
                    # if request.POST['timeLimit'] == '10':
                    #     duration = int(request.POST['endWidth'])/10
                    # elif request.POST['timeLimit'] == '20':
                    #     duration = int(request.POST['endWidth'])/5
                    # elif request.POST['timeLimit'] == '30':
                    #     duration = float(request.POST['endWidth'])/3.33
                    # currentFieldPlayerSession.timeTaken = currentFieldPlayerSession.timeTaken + timedelta(seconds=duration)
                    # currentFieldPlayerSession.save()

                    result = {
                        'isClicked': isClicked,
                        # 'duration': duration
                        #test untuk tengok if for case pilih answer + click next, dia update duration ni je ke (BETUL),
                        #or update +timeLimit sekali (SALAH)
                    }
                    return JsonResponse(result)
                
                elif request.POST['requestType'] == 'updateStatusSessionRecord':
                    currentStudentPersonalitySession.isFinish = True
                    currentStudentPersonalitySession.save()

                    return HttpResponse("Success")
            else:
                print("Hi")
                hasSubmitted = True
                #import from form.py
                form = TestForm(data=request.POST, answers=ANSWER_CHOICES)
                #validate the data (smua data ada in each field)
                if form.is_valid():
                    #cleaned_data = returns a dictionary of validated form input fields and their values
                    filledList = form.cleaned_data

                    # difficulty = nextQuestionRecord.difficulty
                    
                    # if difficulty == 'Mudah':
                    #     currentFieldPlayerSession.countEasy += 1
                    # elif difficulty == 'Sederhana':
                    #     currentFieldPlayerSession.countMedium += 1
                    # elif difficulty == 'Sukar':
                    #     currentFieldPlayerSession.countHard += 1

                    if filledList['isClicked'] == 'True':
                        # if filledList['answer_choices'] != "":
                        #     hasAnswered = True
                            #filledList['answer_choices'] is string, not Boolean

                            # for index, choice in enumerate(ANSWER_CHOICES):
                                #choice[0] (value 'True'/'False_1'/'False_2'/'False_3') is string
                                #choice[1] (questionText) is a string

                                #since choice[0] and choice[1] are strings, and all the values (choice[0]) are unique,
                                #we can just find match of choice[0] and the filled value
                                #and assign choice[1] to chosenAnswerText right away
                                # if filledList['answer_choices'] == choice[0]:
                                #     chosenAnswerText = choice[1]

                            if filledList['answer_choices'] == 'True':
                                isCorrect = True
                                currentStudentPersonalitySession.score += 1

                                # if difficulty == 'Mudah':
                                #     currentFieldPlayerSession.countEasyCorrect += 1
                                #     currentFieldPlayerSession.currentPointsEarned += 6
                                #     currentPlayerTotalScoreAllField += 6
                                # elif difficulty == 'Sederhana':
                                #     currentFieldPlayerSession.countMediumCorrect += 1
                                #     currentFieldPlayerSession.currentPointsEarned += 8
                                #     currentPlayerTotalScoreAllField += 8
                                # elif difficulty == 'Sukar':
                                #     currentFieldPlayerSession.countHardCorrect += 1
                                #     currentFieldPlayerSession.currentPointsEarned += 10
                                #     currentPlayerTotalScoreAllField += 10
                    
                    #if didn't click "Semak Jawapan", no matter clicked on any answer/not, add timeLimit to timeTaken (consider never submit on time)
                    # else:
                    #     currentFieldPlayerSession.timeTaken = currentFieldPlayerSession.timeTaken + timedelta(seconds=int(nextQuestionRecord.timeLimit))

                    # if filledList['answer_choices'] is None, means time's up & tak jawab OR mmg tak jawab (tertekan next without click answer)
                    # so hasAnswered remains False
                    # but still save dateLastPlayed to current time
                    # or maybe change the name to "dateFinished"???
                    # note: everytime save() ni automatic yg dateLastPlayed updated to current time
                    currentStudentPersonalitySession.save()

                    # TEST
                    request.session['hasSubmittedList'].append(hasSubmitted)
                    request.session['hasAnsweredList'].append(hasAnswered)
                    request.session['isCorrectList'].append(isCorrect)

                    context = {
                        'user_id': user_id,
                        'form': form,
                        'currentStudentPersonalitySession': currentStudentPersonalitySession,
                        # 'currentPlayerTotalScoreAllField': currentPlayerTotalScoreAllField,
                        'nextQuestionRecord': nextQuestionRecord,
                        # 'nextAnswerRecords': nextAnswerRecords,
                        # 'nextHintRecords': nextHintRecords,
                        'cnt_quest': int(cnt_quest),
                        'isCorrect': isCorrect,
                        # 'field_id': field_id,
                        # 'questionTextOpt': questionTextOpt,
                        # 'questionTextOnly': questionTextOnly,
                        # 'chosenAnswerText': chosenAnswerText,
                        'hasAnswered': hasAnswered,
                        'hasSubmitted': hasSubmitted,
                        'sessionList': str(request.session['answeredQuestions']), #test
                        'cntQuestList': str(request.session['cntQuestList']), #test
                        # 'next_cnt_ques': next_cnt_ques,
                        'hasSubmittedList': str(request.session['hasSubmittedList']), #test
                        'hasAnsweredList': str(request.session['hasAnsweredList']), #test
                        'isCorrectList': str(request.session['isCorrectList']), #test
                        'questionsExceptAttendedIDs': remainingQuestionsIDs, #test
                        # 'cntHint': cntHint,
                        # 'randomHint': randomHint,
                        # 'hintsUsedList': str(request.session['hintsUsedList']), test
                        'isClicked': filledList['isClicked']
                    }

                    # return render(request, 'quiz/quizPlay2.html', context)
                    return render(request, 'pTest/testPlay2.html', context)
        else:
            form = TestForm(answers=ANSWER_CHOICES)
            if request.is_ajax():
                context = {
                    'user_id': user_id,
                    'form': form,
                    'currentStudentPersonalitySession': currentStudentPersonalitySession,
                    # 'currentPlayerTotalScoreAllField': currentPlayerTotalScoreAllField,
                    'nextQuestionRecord': nextQuestionRecord,
                    # 'nextAnswerRecords': nextAnswerRecords,
                    # 'nextHintRecords': nextHintRecords,
                    'cnt_quest': int(cnt_quest),
                    'isCorrect': isCorrect,
                    # 'field_id': field_id,
                    # 'questionTextOpt': questionTextOpt,
                    # 'questionTextOnly': questionTextOnly,
                    # 'chosenAnswerText': chosenAnswerText,
                    'hasAnswered': hasAnswered,
                    'hasSubmitted': hasSubmitted,
                    'sessionList': str(request.session['attendedQuestions']), #test
                    # 'cntQuesList': str(request.session['cntQuesList']),
                    # 'next_cnt_ques': next_cnt_ques,
                    'hasSubmittedList': str(request.session['hasSubmittedList']), #test
                    'hasAnsweredList': str(request.session['hasAnsweredList']), #test
                    'isCorrectList': str(request.session['isCorrectList']), #test
                    'questionsExceptAttendedIDs': remainingQuestionsIDs, #test
                    # 'cntHint': cntHint,
                    # 'randomHint': randomHint,
                    # 'hintsUsedList': str(request.session['hintsUsedList']), #test
                    'isClicked': isClicked
                }
                # return render(request, 'quiz/quizPlay2.html', context)
                return render(request, 'pTest/testPlay2.html', context)
            else: 
                context = {
                    'dashboardNav': userid(user_id),
                    'username': currentPlayerUsername,
                    # 'currentAvatarDetailsObject': currentAvatarDetailsObject,
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
                    # 'currentPlayerTotalScoreAllField': currentPlayerTotalScoreAllField,
                    'nextQuestionRecord': nextQuestionRecord,
                    # 'nextAnswerRecords': nextAnswerRecords,
                    # 'nextHintRecords': nextHintRecords,
                    'cnt_quest': int(cnt_quest),
                    'isCorrect': isCorrect,
                    # 'field_id': field_id,
                    # 'questionTextOpt': questionTextOpt,
                    # 'questionTextOnly': questionTextOnly,
                    # 'chosenAnswerText': chosenAnswerText,
                    'hasAnswered': hasAnswered,
                    'hasSubmitted': hasSubmitted,
                    'sessionList': str(request.session['attendedQuestions']), #test
                    # 'cntQuesList': str(request.session['cntQuesList']),
                    # 'next_cnt_ques': next_cnt_ques,
                    'hasSubmittedList': str(request.session['hasSubmittedList']), #test
                    'hasAnsweredList': str(request.session['hasAnsweredList']), #test
                    'isCorrectList': str(request.session['isCorrectList']), #test
                    'questionsExceptAttendedIDs': remainingQuestionsIDs, #test
                    # 'cntHint': cntHint,
                    # 'randomHint': randomHint,
                    # 'hintsUsedList': str(request.session['hintsUsedList']), #test
                    'isClicked': isClicked
                }
                # return render(request, 'quiz/quizPlay.html', context)
                return render(request, 'pTest/testPlay.html', context)
                # return render(request, 'pTest\studentTest.html', context)
        
    #parent and teacher
    else:
        context = {
            'dashboardNav': userid(user_id), 
            'user_id': user_id, 
            'username': username,
            # 'sectionQuestion': sectionQuestion,
            # 'allQuestions': allQuestions,
            'test': urlTest, 
            'blog': urlBlog, 
            'quiz': urlQuiz, 
            'search': urlSearch, 
            'dashboard':urlDashboard, 
            'logout': urlLogout
        }
        return render(request, 'pTest\pTestNonStudent.html', context)

def testAdmin(request, user_id):
    context = {
        'dashboardNav': user_id,
        'user_id': user_id, 
    }
    return render(request, 'pTest\pTestAdmin.html', context)