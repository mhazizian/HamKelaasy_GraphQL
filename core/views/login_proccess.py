import json

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

from core.models import User_temp, STUDENT_KEY_WORD, Student, TEACHER_KEY_WORD, Teacher, PARENT_KEY_WORD, Parent
from core.views import Fard_API


def login(request):
    redirect_url = request.GET['redirect_url']
    redirect_url = redirect_url.replace('#', '%23')

    return HttpResponseRedirect(Fard_API().signup_url + "&next=" + redirect_url)


@csrf_exempt
def signup(request):
    res = {}
    try:
        data = json.loads(request.body)

        temp = get_object_or_404(User_temp, pk=int(data['fd_id']))
        username = temp.username
        fard_access_token = temp.fard_access_token

        first_name = data.get('firstName', temp.first_name)
        last_name = data.get('lastName', temp.last_name)
        email = data.get('email', temp.email)
        type = data['type']

        # check later:

        temp.delete()

        if User.objects.filter(username=username).exists():
            res['type'] = "error"
            res['message'] = "username is not available"
            return HttpResponse(json.dumps(res), status=406)
        user = User(username=username)

        if type == STUDENT_KEY_WORD:
            age = int(data['age'])
            nickname = data['nickName']
            gender = int(data.get('gender', temp.gender))

            user.save()
            student = Student(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email, gender=gender,
                fard_access_token=fard_access_token,
                age=age,
                nickname=nickname
            )
            student.save()
        if type == TEACHER_KEY_WORD:
            gender = int(data.get('gender', temp.gender))

            user.save()

            teacher = Teacher(
                user=user,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                email=email,
                fard_access_token=fard_access_token,
            )
            teacher.save()
        if type == PARENT_KEY_WORD:
            user.save()
            parent = Parent(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                fard_access_token=fard_access_token,
            )
            parent.save()

        res['type'] = "success"
        res['token'] = Token.objects.get(user=user).key
        return HttpResponse(json.dumps(res), status=200)
    except:
        res['type'] = "error"
        res['message'] = "bad data input"
        return HttpResponse(json.dumps(res), status=400)


def resolve_fard(request):
    redirect_url = request.GET['next']

    fard_api = Fard_API()
    fard_api.connect(request)
    data = fard_api.get_data()

    username = data.get('username', None)
    access_token = fard_api.access_token

    # if user has already signup and has a Token
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        return HttpResponseRedirect(
            redirect_url \
            + "?state=" + "1" \
            + "&token=" + Token.objects.get(user=user).key \
            + "&type=" + user.person.type
        )

    fname = data.get('firstname', None)
    lname = data.get('lastname', None)
    gender = data.get('gender', None)

    data = fard_api.get_data(1)
    email = data.get('email', None)

    if User_temp.objects.filter(fard_access_token=access_token).exists():
        user_temp = User_temp.objects.get(fard_access_token=access_token)
    else:
        user_temp = User_temp(
            fard_access_token=access_token,
            username=username,
            first_name=fname,
            last_name=lname,
            email=email,
            gender=gender
        )
        user_temp.save()

    return HttpResponseRedirect(
        redirect_url \
        + "?state=" + "0" \
        + "&fd_id=" + str(user_temp.id)
    )


@csrf_exempt
def temp_user_handler(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = int(data.get('fd_id', 0))

        if User_temp.objects.filter(pk=id).exists():
            temp = User_temp.objects.get(pk=id)

            data = {
                'firstName': temp.first_name,
                'lastName': temp.last_name,
                'email': temp.email,
                'gender': temp.gender,
            }
            return HttpResponse(json.dumps(data), status=200)
    return HttpResponse('bad data input', status=400)
