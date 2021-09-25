from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import random



# Create your models here.
class mob(models.Model):
    number = models.PositiveIntegerField()

class contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.PositiveIntegerField()
    message = models.CharField(max_length=1000)

class log(models.Model):
    username = models.CharField(max_length=122)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    password1 = models.CharField(max_length=50)
    mob = models.PositiveIntegerField()
       
DIFF_CHOICES = (
    ('EASY', 'EASY'),
    ('MEDIUM', 'MEDIUM'),
    ('HARD', 'HARD'),
)

class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    difficluty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)



class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

###########################################################################

class Subject(models.Model):
    sub_name = models.CharField(max_length = 30, blank = False)
    sub_img = models.ImageField(null = True, blank = True)
    sub_desp = models.CharField(max_length = 300)

    def __str__(self):
        return self.sub_name

class Assignment(models.Model):
    assign_name = models.CharField(max_length=30)
    assign_ques = models.CharField(max_length=300)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.assign_ques

class Video(models.Model):
    vid_title = models.CharField(max_length=50)
    vid_file = models.FileField(upload_to = "codes/%y")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.vid_title

class AssignmentUpload(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    file = models.FileField()

