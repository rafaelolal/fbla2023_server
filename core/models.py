from django.db.models import Model, ForeignKey, CASCADE
from django.db.models.fields import BooleanField, CharField, TextField, DateField, PositiveSmallIntegerField, DateTimeField


class Admin(Model):
    id = CharField(max_length=28, primary_key=True)

    def __str__(self):
        return f"{self.pk}"


class Student(Model):
    id = CharField(max_length=28, primary_key=True)
    email = CharField(max_length=320, unique=True)
    first_name = CharField(max_length=30, blank=True, null=True)
    middle_name = CharField(max_length=30, blank=True, null=True)
    last_name = CharField(max_length=30, blank=True, null=True)
    biography = TextField(max_length=280, blank=True, null=True)
    grade = PositiveSmallIntegerField(
        choices=[(5, 5), (6, 6), (7, 7), (8, 8)],
        blank=True, null=True)
    image = CharField(
        max_length=512, default='https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')
    live_points = PositiveSmallIntegerField(default=0)

    points = PositiveSmallIntegerField(default=0)
    rank = PositiveSmallIntegerField(blank=True, null=True, unique=True)

    def get_name(self):
        if all([self.first_name, self.middle_name, self.last_name]):
            return f"{self.first_name[0]}. {self.middle_name[0]}. {self.last_name}"
        else:
            return f"{self.email}"

    def __str__(self):
        return f"{self.pk}: {self.get_name()}"


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
    image = CharField(max_length=36)
    points = PositiveSmallIntegerField()
    cancelation_reason = TextField(max_length=1024, blank=True, null=True)

    def __str__(self):
        s = f"{self.pk}: "
        s += 'Canceled' if self.cancelation_reason else ''
        s += f"{self.title[:15]}..."
        return s


class Attendance(Model):
    student = ForeignKey(Student, related_name="events", on_delete=CASCADE)
    event = ForeignKey(Event, related_name="participants", on_delete=CASCADE)
    attended = BooleanField(blank=True, null=True)
    final = BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}: {self.student.get_name()} on {self.event.title[:15]}..."


class News(Model):
    title = CharField(max_length=256)
    content = TextField(max_length=16384)
    created_on = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}: {self.title[:15]}..."


class Report(Model):
    created_on = DateField(auto_now_add=True)
    first_name = CharField(max_length=30)
    middle_name = CharField(max_length=30, null=True)
    last_name = CharField(max_length=30, null=True)
    points = PositiveSmallIntegerField()
    grade = PositiveSmallIntegerField(
        choices=[(5, 5), (6, 6), (7, 7), (8, 8)],
        blank=True, null=True)

    def __str__(self):
        return f"{self.pk}: {self.first_name[0]}. {self.middle_name[0]}. {self.last_name} on {self.created_on}"


class Rally(Model):
    starts_on = DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.pk}: {self.starts_on}"


class Leaderboard(Model):
    created_on = DateField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.created_on}"


class Prize(Model):
    type = CharField(choices=[("School", "School"),
                     ("Food", "Food"), ("Spirit", "Spirit")], max_length=6)
    student = ForeignKey(Student, related_name="prizes", on_delete=CASCADE)

    def __str__(self):
        return f"{self.pk}: {self.student.get_name()}, {self.type}"
