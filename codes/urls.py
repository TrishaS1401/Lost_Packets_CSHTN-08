
from django.contrib import admin
from django.urls import path
from codes import views
from django.conf import settings
from codes import views
from django.conf.urls.static import static

from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view
)
#tuple
app_name = 'quizes'

urlpatterns = [
    path("veri",views.veri, name="veri"),
    path("otp",views.otp, name="otp"),
    path("verifyotp",views.verifyotp, name="verifyotp"),
    path("contacts",views.contacts, name="contacts"),
    path("cont",views.cont, name="cont"),
    path("reg",views.registration, name="registration"),
    path("registration",views.reg, name="reg"),
    path("log",views.login, name="login"),
    path("logout",views.logout, name="logout"),
    path("land",views.land, name="land"),
    path("forgotpass",views.forgotpass, name="forgotpass"),
    path("fp",views.fp, name="fp"),
    path("home",views.home, name="home"),
    path("hello",views.hello, name="hello"),

    path('', QuizListView.as_view(), name='main-view'),
    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/save/', save_quiz_view, name='save-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),

]   

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)