"""url patterns for hogwarts_app application"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # home page

    path('signup', views.signup_website, name='signup_website'),  # register
    # registration is available only for students group. Professors accounts
    # can only be created in admin mode
    path('login', views.login_website, name='login_website'),  # login
    path('logout', views.logout_website, name='logout_website'),  # logout

    path('locations', views.locations, name='locations'),  # locations list
    path('professors', views.professors, name='professors'),  # professors list
    path('houses', views.houses, name='houses'),  # houses list
    path('subjects', views.subjects, name='subjects'),  # subjects list
    path('students', views.students, name='students'),  # students list with
    # access to info, edit and delete options for students
    # (edit and delete options are only available for professors group of users

    path('house_info/<int:house_id>', views.house_info, name='house_info'),
    # houses detailed view
    path('subject_info/<int:subject_id>', views.subject_info,
         name='subject_info'),
    # subjects detailed view
    path('student_info/<int:student_id>', views.student_info,
         name='student_info'),
    # student/id detailed view
    path('add_student', views.add_student, name='add_student'),
    # enroll a student to Hogwarts, only available for Professors accounts
    path('edit_student/<int:student_id>',
         views.edit_student, name='edit_student'),
    # edit student info, from students list page,
    # only available for Professors accounts
    path('delete_student_confirmation/<int:student_id>',
         views.delete_student_confirmation,
         name='delete_student_confirmation'),
    # delete student confirmation, from students list page,
    # only available for Professors accounts
    path('delete_student/<int:student_id>',
         views.delete_student, name='delete_student'),
    # delete student, from delete student confirmation page,
    # only available for Professors accounts
    path('course_enrollment', views.course_enrollment,
         name='course_enrollment')
    # assigning students to subjects, only available for students accounts
]
