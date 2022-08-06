from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from account.models import User 
from django.db.models import Q
from .models import Chat , Thread
from django.http import JsonResponse
import json
from django.db.models import Count

# Create your views here.
@login_required(login_url='/account/login/')
def index(request):
    ctx={}
    id=request.user.id
    users=User.objects.filter(~Q(id=id))
    users = users.values('id','first_name','last_name','mobile')
    ctx['users']=users
    ctx['username'] = request.user.first_name + request.user.last_name
    ctx['userid'] = request.user.id
    return render(request,'index.html',ctx)


def loadchat(request,receiver):
    data={}
    msg_list = Chat.objects.filter(thread=receiver)
    messages = msg_list.values()
    message_queue = []
    for item in messages:
        message_queue.append(item)
    data["messages"]=message_queue
    data['username'] = request.user.first_name + request.user.last_name
    return JsonResponse(data , safe=False)
    
def getroom(request,number):
    data = {}
    me = request.user.id
    other_user=User.objects.get(mobile=number)
    threads = Thread.objects.all()
    threads=threads.filter(users__in=[me, other_user.id]).distinct()
    threads = threads.annotate(u_count=Count('users')).filter(u_count=2)
    data["room_name"]= threads.first().id
    return JsonResponse(data , safe=False)    



    
    
    
    
    