"""View functions for hogwarts_app application"""
from django.contrib.auth import (authenticate, login as user_login,
                                 logout as user_logout)
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages

import re
import random

from .models import *
from .forms import StudentsForm


def regex_validation(name):
    """Regular expression validation for first or last name of a student"""
    r = re.search(r'^[A-Z][a-z]+$', name)
    if r:
        return True
    else:
        return False


def signup_validation(request, first_name,
                      last_name, username, password, password_repeat):
    """Set of validations for User registration"""

    # first_name and last_name check
    name_check = regex_validation(first_name) and regex_validation(last_name)
    if not name_check:
        messages.error(request, "You should provide a name using only "
                                "Latin letters! "
                                "Name and Surname should start with a capital "
                                "letter.")
        return redirect('signup_website')

    # username validation
    if len(username) < 1 or len(username) > 150:
        messages.error(request, "Username must be "
                                "between 1 and 150 characters long.")
        return redirect('signup_website')

    username_validator = re.search(r"^[\w.@+-]+$", username)
    if not username_validator:
        messages.error(request, "The username can only contain letters,"
                                " numbers and the symbols @/./+/-/_.")

    # password validation
    try:
        validate_password(password)
    except ValidationError as e:
        error_messages = ""
        for message in e.messages:
            error_messages += message
        messages.error(request, error_messages)
        return redirect('signup_website')

    if password != password_repeat:
        messages.error(request, "Entered passwords do not match!")
        return redirect('signup_website')

    # unique user check
    if User.objects.filter(username=username).exists():
        messages.error(request, "Such username already is taken!")
        return redirect('signup_website')

    return True


def login_website(request):
    """Log in view function"""
    if request.method == "POST":
        login = request.POST.get('login')
        password = request.POST.get('password')
        usr = authenticate(request, username=login, password=password)
        if usr is not None:
            user_login(request, usr)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Invalid username or password. "
                                    "Please try again.")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout_website(request):
    """Log out view function"""
    user_logout(request)
    return redirect('index')


def signup_website(request):
    """Registration view function.
    Only Students group accounts can be registered through this view.
    To create Professor account you need to ask administrator.
    With creating Student account also commits Student object creation and
    Student sorting into the House"""
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_name = first_name + ' ' + last_name
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

        if signup_validation(request,
                             first_name,
                             last_name,
                             username,
                             password,
                             password_repeat):
            user = User.objects.create_user(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name)
            user.groups.add('Students')
            houselist = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']
            house = random.choice(houselist)
            house_instance = Houses.objects.filter(name=house).first()
            student = Students(name=student_name, house=house_instance)
            student.save()
            user.save()
            messages.success(request,
                             f"Congratulations! "
                             f"You've been enrolled in {house}!")
            return redirect('login_website')
    else:
        return render(request, 'signup.html')


def index(request):
    """Home page view function"""
    return render(request, 'index.html')


def houses(request):
    """Houses list view function"""
    houses_data = Houses.objects.all()
    context = {
        'houses': houses_data
    }
    return render(request, 'houses.html', context=context)


def locations(request):
    """Locations list view function"""
    locations_data = Locations.objects.all()
    context = {
        'locations': locations_data
    }
    return render(request, 'locations.html', context=context)


def professors(request):
    """Professors list view function"""
    professors_data = Professors.objects.all()
    context = {
        'professors': professors_data
    }
    return render(request, 'professors.html', context=context)


def subjects(request):
    """Subjects list view function"""
    subjects_data = Subjects.objects.all()
    context = {
        'subjects': subjects_data
    }
    return render(request, 'subjects.html', context=context)


def students(request):
    """Students list view function.
    From this page are available: Student info view (for all users),
    Student info Edit view and Student Delete view (for Professors group)."""
    students_data = Students.objects.all()
    context = {
        'students': students_data
    }
    return render(request, 'students.html', context=context)


def house_info(request, house_id):
    """House detail view function. Passwords information requires
    authorisation on the website."""
    house_data = Houses.objects.get(pk=house_id)
    students_data = Students.objects.filter(house=house_id)
    context = {
        'house': house_data,
        'students': students_data
    }
    return render(request, 'house_info.html', context=context)


def subject_info(request, subject_id):
    """Subject detailed view function."""
    subject_data = Subjects.objects.get(pk=subject_id)
    students_data = Students_to_subjects.objects.filter(subject=subject_id)
    professor_data = Professors.objects.filter(subject=subject_id)
    context = {
        'subject': subject_data,
        'students': students_data,
        'professor': professor_data
    }
    return render(request, 'subject_info.html', context=context)


def student_info(request, student_id):
    """Student detailed view function."""
    student_data = Students.objects.get(pk=student_id)
    subjects_info = Students_to_subjects.objects.filter(student=student_id)
    context = {
        'student': student_data,
        'subjects': subjects_info
    }
    return render(request, 'student_info.html', context=context)


def add_student(request):
    """Student enrollment in Hogwarts view function with sorting into one
    of the houses. Only available for Professors accounts."""
    if request.method == "POST":
        form = StudentsForm(request.POST)

        if form.is_valid():  # form validation
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            if not regex_validation(first_name) and regex_validation(last_name):
                messages.error(request,
                               "You should provide a name using "
                               "only Latin letters! "
                               "Name and Surname should start "
                               "with a capital letter.")
                return redirect('add_student')

            checked_name = first_name + ' ' + last_name

            signed_students = Students.objects.filter(name=checked_name).first()
            if signed_students:  # check for student uniqueness in the system
                messages.error(request, "Name already exists!")
                return redirect('add_student')

            houselist = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']
            house = random.choice(houselist)  # house sorting
            house_instance = Houses.objects.filter(name=house).first()
            if not house_instance:
                messages.error(request, "Selected house does not exist!")
                return redirect('add_student')

            new_student = Students(name=checked_name, house=house_instance)
            new_student.save()
            messages.success(request,
                             f"Congratulations! {new_student.name} "
                             f"has been enrolled in {house}!")
            return redirect('students')
    else:  # if smth went wrong, going back to the enrollment form
        form = StudentsForm()
        context = {
            "form": form
        }
        return render(request, "add_student.html", context=context)


def edit_student(request, student_id):
    """Edit student info view function.
     Only available for Professors accounts."""
    if request.method == "POST":
        new_name = request.POST.get('student_name')
        r = re.search(r'^[A-Z][a-z]+ [A-Z][a-z]+$', new_name)
        if r:
            check_list = request.POST.getlist("checkbox")
            connections_list = (Students_to_subjects.objects.
                                filter(student=student_id))
            for connection in connections_list:
                if str(connection.subject.id) in check_list:
                    pass
                else:
                    connection.delete()
            student = Students.objects.get(pk=student_id)
            student.name = new_name
            student.save()
            return redirect(reverse('student_info', args=[student_id]))
        else:
            messages.error(request,
                           "You should provide a name using "
                           "only Latin letters! "
                           "Name and Surname should start "
                           "with a capital letter.")
            return redirect(reverse('edit_student', args=[student_id]))

    else:
        student_data = Students.objects.get(pk=student_id)
        subjects_info = Students_to_subjects.objects.filter(student=student_id)
        context = {
            'student': student_data,
            'subjects': subjects_info
        }
        return render(request, 'edit_student.html', context=context)


def delete_student_confirmation(request, student_id):
    """Student delete confirmation view function.
    Only available for Professors accounts."""
    if request.method == "GET":
        student = Students.objects.get(pk=student_id)
        context = {
            'student': student
        }
        return render(request, 'delete_student_confirmation.html',
                      context=context)


def delete_student(request, student_id):
    """Delete Student view function. Only available for Professors accounts."""
    if request.method == "POST":
        student = Students.objects.get(pk=student_id)
        student.delete()
        return redirect('students')


def course_enrollment(request):
    """Assigning students to subjects, only available for students accounts"""
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        subject_id = request.POST.get("subject_id")

        if not student_id or not subject_id:
            messages.error(request,
                           f"Please ensure that both Student name "
                           f"and Subject have been provided.")
            return redirect('course_enrollment')

        student = Students.objects.get(pk=student_id)
        subject = Subjects.objects.get(pk=subject_id)
        assigned_subjects = (Students_to_subjects.
                             objects.filter
                             (student=student, subject=subject).first())

        if assigned_subjects:
            messages.error(request,
                           f"Please ensure that provided Subject "
                           f"is not already in your Subject list.")
            return redirect('course_enrollment')

        new_assignment = Students_to_subjects(student=student, subject=subject)
        new_assignment.save()
        messages.success(request,
                         f"Congratulations! You've been enrolled "
                         f"in a new course! Full list of your courses "
                         f"you may see on your student page.")
        return redirect('student_info', student_id=student_id)

    else:
        students_data = Students.objects.all()
        subjects_data = Subjects.objects.all()
        context = {
            'students': students_data,
            'subjects': subjects_data
        }
        return render(request, 'course_enrollment.html', context=context)

