from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateQuestForm
from .models import pTest #Question, Questionnaire, Choice, 
from django.template import loader

# path to test page
def test(request):
    pTests = pTest.objects.all() #pulling all soalan in db
    context = {
        'pTests':pTests
    }
    return render(request, 'pTest/test.html', context) #return test template

def create(request):
    form = CreateQuestForm()
    if request.method == 'POST':
        form = CreateQuestForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data['question'])
            form.save()
            return redirect('pTest:test')
    else:
        form = CreateQuestForm()
    context = {
        'form' : form
    }
    return render(request, 'pTest/create.html', context) #return test template

def choice(request, pTest_id):
    pTests = pTest.objects.get(pk=pTest_id)

    if request.method == 'POST':
        selected_option = request.POST['pTest']
        if selected_option == 'option1':
            pTests.option_one_count += 1
        elif selected_option == 'option2':
            pTests.option_two_count += 1
        elif selected_option == 'option3':
            pTests.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        pTests.save()
        return redirect('pTest:result', pTests.id)

    context = {
        'pTests' : pTests
    }
    return render(request, 'pTest/choice.html', context) #return test template

def results(request, pTest_id):
    pTests = pTest.objects.get(pk=pTest_id)
    context = {
        'pTests' : pTests
    }
    return render(request, 'pTest/results.html', context) #return test template

# def test (request):
#     questionnaire_list = Questionnaire.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('pTest/test.html')
#     context = {
#         'latest_questionnaire_list': questionnaire_list
#     }
#     return render(request, 'pTest/test.html', context)

# def questions (request):
#     question_list = Question.objects.all()
#     # template = loader.get_template('pTest/questions.html')
#     context = {
#         'latest_question_list': question_list
#     }
#     return render(request, 'pTest/questions.html', context)

# def results (request):
#     questionnaire_instance = QuestionnaireInstance.objects.get(taker=request.user)
#     answer_instance = Choice.objects.all()

#     if request.method == 'POST':
#        questionnaire_instance.C1_score=+ answer_instance.values_list('C1',flat=True)[selected answer] #No clue how to call on the score of the specifically selected answer here