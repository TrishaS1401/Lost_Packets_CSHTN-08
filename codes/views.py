from django.shortcuts import render,redirect
import os,math,random,re
from twilio.rest import Client
from django.contrib import messages
from codes.models import Subject, mob,contact,log,Quiz,Question, Answer, Result, Assignment, AssignmentUpload, Video
from django.views.generic import ListView
from django.http.response import HttpResponse
from django.http import JsonResponse

# Create your views here.
def veri(request):
    return render(request, 'veri.html')

def home(request):
    user=log.objects.all()
    subject = Subject.objects.all()
    return render(request, 'home.html',{'users' : user, 'subject' : subject})

def hello(request):
    video = Video.objects.all()
    assignment = Assignment.objects.all()
    return render(request, 'course.html', {'video' : video, 'assignment' : assignment})


def otp(request):
    if request.method == "POST":
        number = request.POST.get('mob')
        #user1 = mob(number=m)
        #user1.save()
        a = mob.objects.filter(number=number).values('number')
        if a: 
            account_sid = 'account_sid'
            auth_token = 'auth_token'
            client = Client(account_sid, auth_token)
        
            string = "0123456789"
            otpnum = ""
            l = len(string)
            for i in range(6):
                otpnum += string[math.floor(random.random() * l)]

            message = client.messages.create(
                              body='The one time password(OTP) to verify your phone number is '+otpnum,
                              from_='+13133273616',
                              to='+91'+number
                          )

            print(message.sid)
            return render(request, 'otpveri.html',{'otpnum': otpnum,})
        else:
            messages.error(request, 'Your number is not registered!')
            return render(request, 'index.html')


def verifyotp(request):
    if request.method == "POST":
        o = request.POST.get('otp')
        o1 = request.POST.get('def')
        if o == o1:
            return render(request, 'fpass.html')
        else:
            return render(request, 'veri.html')

def contacts(request):
     user=log.objects.all()
     return render(request, 'contact.html',{'users' : user,})

def land(request):
     return render(request, 'land.html')

def cont(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        mes = request.POST.get('message')
        if(name and email and phone and mes):
            u = contact(name=name,email=email,phone=phone,message=mes)
            u.save()
            messages.success(request, 'Your message was sent successfully!')
        else:
            messages.error(request, 'Please fill all the details!')
        return redirect('/contacts')

def reg(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        mob1 = request.POST.get('mob')
        def ispresent(str):
            regex = ("^(?=.*[a-z])(?=." +
            "*[A-Z])(?=.*\\d)" +
            "(?=.*[-+_!@#$%^&*., ?]).+$")
            p = re.compile(regex)
            if(re.search(p, str) and len(str) >= 8):
                return True
            else:
                return False
        a = log.objects.filter(email=email).values('email')
        if a:
            messages.error(request, 'This email already exists!')
            return render(request, 'index.html')
        elif (ispresent(password) and (password == password1)):
            user = log(username=name, email=email, password=password, mob=mob1, password1=password1)
            user1 = mob(number=mob1)
            user1.save()
            user.save()
        else:
            messages.error(request, 'Password error!')
            return render(request, 'index.html')
    return render(request, 'index.html')



def logout(request):
     del request.session['email']
     return redirect("/land")

def forgotpass(request):
     return render(request, 'fpass.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        user=log.objects.all()
        a = log.objects.filter(email=email,password=password).values('email','password')
        print(a)
        if a:
            user1=log.objects.get(email=email)
            request.session['email'] = user1.email
            return render(request, 'home.html', {'users' : user,})
        else:
            messages.error(request, 'Invalid Credentials!')
            return redirect("/registration")
    else:
        return redirect("/registration")

def fp(request):
     if request.method == "POST":
        email = request.POST.get('email1')
        password = request.POST.get('password')
        npass = request.POST.get('password1')
        a = log.objects.filter(email=email).values('email')
        print(a)
        if a and (password==npass):
            b = log.objects.get(email=email)
            b.password = npass
            b.save()
            return render(request, 'index.html')
        else:
            messages.error(request, 'Password and Confirm Password should be same!')
            return render(request, 'fpass.html')
     else:
        return render(request, 'fpass.html')


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'obj': quiz})


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})

