"""Models for hogwarts_app application"""
from django.db import models


class Houses(models.Model):
    """Represents one of four Houses of Hogwarts"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    common_room = models.ForeignKey('Locations',
                                    on_delete=models.CASCADE,
                                    related_name='houses')
    password = models.CharField(max_length=60)
    head_of_the_house = models.ForeignKey('Professors',
                                          on_delete=models.CASCADE,
                                          related_name='houses')

    class Meta:
        verbose_name = 'House'
        verbose_name_plural = 'Houses'

    def __str__(self):
        return f"House {self.name}"


class Locations(models.Model):
    """Represents different locations of Hogwarts"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return f"Location {self.name}"


class Professors(models.Model):
    """Represents professors of Hogwarts, connected to taught subjects"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    subject = models.ForeignKey('Subjects',
                                on_delete=models.CASCADE,
                                related_name='professors')

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professors'

    def __str__(self):
        return f"Professor {self.name}"


class Students(models.Model):
    """Represents students of Hogwarts, connected to sorted Houses"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    house = models.ForeignKey('Houses',
                              on_delete=models.CASCADE,
                              related_name='students')

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"Student {self.name}"


class Students_to_subjects(models.Model):
    """Represents courses enrollment for students, many-to-many"""
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Students',
                                on_delete=models.CASCADE,
                                related_name='students_to_subjects')
    subject = models.ForeignKey('Subjects',
                                 on_delete=models.CASCADE,
                                 related_name='students_to_subjects')

    class Meta:
        verbose_name = 'Students_to_subjects'
        verbose_name_plural = 'Students_to_subjects'

    def __str__(self):
        return (f"Student {self.student.name} "
                f"enrolled in {self.subject.name} course.")


class Subjects(models.Model):
    """Represents subjects, taught in Hogwarts,
    connected to classrooms locations"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    location = models.ForeignKey('Locations',
                                 on_delete=models.CASCADE,
                                 related_name='subjects')

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"Subject {self.name}"
