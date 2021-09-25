from django.contrib import admin
from codes.models import Assignment, AssignmentUpload, Video, mob,contact,log, Quiz, Result, Question, Answer, Subject
# Register your models here.
admin.site.register(mob)
admin.site.register(contact)
admin.site.register(log)


class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

admin.site.register(Result)

admin.site.register(Quiz)

admin.site.register(Subject)

admin.site.register(Assignment)
admin.site.register(Video)
admin.site.register(AssignmentUpload)