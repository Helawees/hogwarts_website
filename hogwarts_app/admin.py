from django.contrib import admin
from .models import (Houses, Locations, Professors, Students, Subjects,
                     Students_to_subjects)

# Register your models here.
admin.site.register(Houses)
admin.site.register(Locations)
admin.site.register(Professors)
admin.site.register(Students)
admin.site.register(Subjects)
admin.site.register(Students_to_subjects)
