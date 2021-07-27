from django.shortcuts import render, redirect
from django.http import HttpResponse
import dashboard.models

# Create your views here.
def blogMain(request, user_type, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    response = "Hello, %s %s! You're at the NONADMIN blog main page!"
    context = {'response': response, 'user_id': user_id}
    return HttpResponse(response % (user_type, user_id))
    #return render(request, 'blog\blogIndex.html', context)

def blogMainAdmin(request, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')
        
    response = "Hello, %s! You're at the ADMIN blog main page!"
    context = {'response': response, 'user_id': user_id}
    return HttpResponse(response % user_id)
    #return render(request, 'blog\blogIndex.html', context)