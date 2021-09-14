from django.http import HttpResponse, HttpRequest
from django.urls import reverse
import quiz.urls

def check_url(request, **kwargs):
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


#[KIV] this file 