from django.db.models import Model, ForeignKey, ImageField, CASCADE
from django.db.models.fields import BooleanField, CharField, TextField, DateField, PositiveSmallIntegerField, DateTimeField


class Admin(Model):
    id = CharField(max_length=20, primary_key=True)


class Student(Model):
    id = CharField(max_length=20, primary_key=True)
    email = CharField(max_length=320, unique=True)
    first_name = CharField(max_length=30, blank=True, null=True)
    middle_name = CharField(max_length=30, blank=True, null=True)
    last_name = CharField(max_length=30, blank=True, null=True)
    biography = TextField(max_length=280, blank=True, null=True)
    grade = PositiveSmallIntegerField(
        choices=[(5, 5), (6, 6), (7, 7), (8, 8)],
        blank=True, null=True)
    image = ImageField(upload_to='images/students/',
                       default='/images/students/default.jpg', null=True)
    live_points = PositiveSmallIntegerField(default=0)

    points = PositiveSmallIntegerField(default=0)
    rank = PositiveSmallIntegerField(blank=True, null=True, unique=True)


class Event(Model):
    title = CharField(max_length=256)
    description = TextField(max_length=1024)
    type = CharField(choices=[("Competition", "Competition"),
                              ("Show", "Show"), ("Fundraiser", "Fundraiser"),
                              ("Trip", "Trip"), ("Fair", "Fair")],
                     max_length=11)
    location = CharField(max_length=64)
    starts_on = DateTimeField(auto_now=False, auto_now_add=False)
    finishes_on = DateTimeField(auto_now=False, auto_now_add=False)
    image = ImageField(upload_to='images/events/')
    points = PositiveSmallIntegerField()
    is_canceled = BooleanField(default=False)
    cancellation_reason = TextField(max_length=1024, blank=True, null=True)


class Attendance(Model):
    student = ForeignKey(Student, related_name="events", on_delete=CASCADE)
    event = ForeignKey(Event, related_name="participants", on_delete=CASCADE)
    attended = BooleanField(blank=True, null=True)
    final = BooleanField(default=False)


class News(Model):
    title = CharField(max_length=256)
    content = TextField(max_length=16384)
    created_on = DateTimeField(auto_now_add=True)


class Report(Model):
    created_on = DateField(auto_now_add=True)
    first_name = CharField(max_length=30)
    middle_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    points = PositiveSmallIntegerField()
    grade = PositiveSmallIntegerField(
        choices=[(5, 5), (6, 6), (7, 7), (8, 8)],
        blank=True, null=True)


class Leaderboard(Model):
    created_on = DateField(auto_now=False, auto_now_add=False)


class Rally(Model):
    starts_on = DateTimeField(auto_now=False, auto_now_add=False)


class Prize(Model):
    type = CharField(choices=[("School", "School"),
                     ("Food", "Food"), ("Spirit", "Spirit")], max_length=6)
    student = ForeignKey(Student, related_name="prizes", on_delete=CASCADE)
