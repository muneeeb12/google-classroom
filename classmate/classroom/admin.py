from django.contrib import admin
from .models import Classroom, Assignment, Lecture, Enrollment
# Register your models here.

admin.site.register(Classroom)
admin.site.register(Assignment)
admin.site.register(Lecture)
admin.site.register(Enrollment)