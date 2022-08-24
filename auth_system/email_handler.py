from django.core.mail import EmailMessage
from django.template.loader import get_template

#send email for new account
def new_account(u_id,email):
        url = f'http://127.0.0.1:8000/activate/{u_id}/'
        ctx = {'link':url}
        body = get_template('auth_system/send.html').render(ctx)
        msg = EmailMessage('Activate your Mento Account',body
                ,'gitspacematrix.com',[email]
            )
        msg.content_subtype = "html"
        msg.send()

#send email for forget password
def forget_password(u_id,email):
    url = f'http://127.0.0.1:8000/user/online/passwordchange/'
    ctx = {'link':url,'code':u_id}
    body = get_template('auth_system/forget_password.html').render(ctx)
    msg = EmailMessage('Activate your Mento Account',body
            ,'gitspacematrix.com',[email]
        )
    msg.content_subtype = "html"
    msg.send()