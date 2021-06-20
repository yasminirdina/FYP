from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def blogMain(request, user_type, user_id):
    response = "Hello, %s %s! You're at the NONADMIN blog main page!"
    context = {'response': response, 'user_id': user_id}
    return HttpResponse(response % (user_type, user_id))
    #return render(request, 'blog\blogIndex.html', context)

def blogMainAdmin(request, user_id):
    response = "Hello, %s! You're at the ADMIN blog main page!"
    context = {'response': response, 'user_id': user_id}
    return HttpResponse(response % user_id)
    #return render(request, 'blog\blogIndex.html', context)