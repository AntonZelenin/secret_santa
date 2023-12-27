from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        return HttpResponse('register post')
    else:
        return HttpResponse(status=405, reason='Method not allowed')


# get register via email: render register.html
# post register via email:
## get email, validate it, generate code, send email, response with a success/error message
## what about dos attacks? how to prevent sending spam to random emails? by ip?
## minimum time between sending subsequent email with code, expiration time of a code
# get enter code:
## render enter_code.html
# post enter code:
## get code, validate it, redirect or error
# post send code again:
## get email, validate it, check minimum waiting time, generate code, send email, response with a success/error message
# post register via google
# get login: render login.html
# post login: get email, get password, validate it, generate token, response with.. something
