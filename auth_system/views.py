from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from auth_system.serializers import UserSeralizer
from uuid import uuid4
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from auth_system.email_handler import forget_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token


#For actavating the account
def activate_account(request,uuid):
    try:
        obj = get_user_model().objects.get(u_id=uuid)
        obj.is_active = True
        obj.u_id = uuid4()
        obj.save()
        return HttpResponse("Account Activated")
    except:
        return HttpResponse("Bad Request")

class Register(generics.CreateAPIView):
    serializer_class = UserSeralizer


#to send the password for reseting
@api_view(['POST'])
def forget_passowrd(request):
    data = request.data.get('email',None)
    try:
        user_data = get_user_model().objects.get(email=data)
        forget_password(user_data.u_id,user_data.email)
        return Response({"email":"sent"})
    except ObjectDoesNotExist:
        return Response({'email':'not-sent'})

#chaning the password via online method
def change_password_online(request):
    if request.method == "POST":
        token = request.POST.get('token',None)
        password = request.POST.get('password',None)
        try:
            data = get_user_model().objects.get(u_id = token)
            data.set_password(password)
            data.u_id = uuid4()
            data.save()
            return HttpResponse("""
                <div style="margin-top:40px"><center><h2>Password Changed Successfully</h2></center></div>
            """)
        except ObjectDoesNotExist:
            return HttpResponse("Unable to change the password")
    return render(request,'auth_system/reset_onlie_password.html',{})



#for reseting password
@api_view(['POST'])
def password_reset(request):

    token = request.data.get('token',None)
    new_password = request.data.get('password',None)

    try:
        user_id = Token.objects.get(key=token).user_id
        account = get_user_model().objects.get(pk=user_id)
        account.set_password(new_password)
        account.save()
        return Response({"password":"true"})
    except:
        return Response({"password":"false"})

