from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from auth_system.serializers import UserSeralizer
from uuid import uuid4
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from auth_system.email_handler import forget_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

def send_email(reqeust):
    url = 'http://127.0.0.1:8000/activate/4a0ca757-4ddf-4cc1-8774-47e1b4f5d3c7/'
    ctx = {
        'link':url
    }
    body = get_template('auth_system/send.html').render(ctx)
    msg_body = """
    <center><h2>Welcome to Mento! </h2></center>
    <br><br>
    <h3>Kindl click on the below link to activate the Account <h3>
    <a href="{}">Activate Account </a>
    """.format(url)

    msg = EmailMessage('Activate your Mento Account',body
    ,'gitspacematrix.com',['md.rehbar@outlook.com']
    )
    msg.content_subtype = "html"
    msg.send()

    return HttpResponse("Mail Send Successfully")

def activate_account(request,uuid):
    try:
        obj = get_user_model().objects.get(u_id=uuid)
        obj.is_active = True
        obj.u_id = uuid4()
        obj.save()
        return HttpResponse("Account Activated")
    except:
        return HttpResponse("Bad Request")

def home(request):
    return render(request,'auth_system/send.html',{})


class Register(generics.CreateAPIView):
    serializer_class = UserSeralizer


@api_view(['POST'])
def forget_passowrd(request):
    data = request.data.get('email',None)
    try:
        user_data = get_user_model().objects.get(email=data)
        forget_password(user_data.u_id,user_data.email)
        return Response({"email":"sent"})
    except ObjectDoesNotExist:
        return Response({'email':'not-sent'})

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

