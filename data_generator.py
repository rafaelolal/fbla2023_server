"""Generates fake data for the database"""

import random
import datetime
from faker import Faker

# if I do not do it like this, my auto formatter changes
# the order of the lines, which matters
if True:
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fbla2023_server.settings")
    from django import setup
    setup()
    from django.utils import timezone
    from core.models import Student, Event, Attendance, News, Prize, Leaderboard, Rally, Report, Admin


def create_all():
    create_functions = [create_students, create_events, create_attendance,
                        create_news, create_prizes, create_or_update_leaderboard,
                        create_or_update_rally, create_reports, create_admin]

    print("Started creating")
    for fun in create_functions:
        fun()
    print("Finished creating")


def delete_all_objects():
    print("Started deleting all objects")
    models = [Student, Event, Attendance, News, Prize, Report]
    for model in models:
        model.objects.all().delete()
    print("Finished deleting all objects")


def create_students():
    # ids must be in this specific order
    ids = ['oGPpPEUloOQRgC5c93H7u3dlwBw2', 'EPJsyOiPOMPJH7uy90BFUWfICCB2',
           'P3g0EkZZfiR6dfW7aMnxV4blQ8s2', 'wODmBVP1OuUATwyhzdwk5Xtjt9K2',
           'vr5et02dk2STp0J6zpE30cPUFkV2', 'mklzxlsecIcdxmAHSXcndSsCy213',
           'J4JMWTKwS9dmM2ulDlYmn0o9gJN2', 'h8z5G0FgnyX6Zn2sMQNv7IgczI92',
           'YYW0xRkaT3QC3Ex550kpuuwlj5b2', '51moiXQZjAXp7mHpnUGzopnVI1Y2', ]

    for i, id in enumerate(ids):
        if i == 0:
            Student(id=id, email=f"student{i}@test.com").save()

        else:
            Student(id=id, email=f"student{i}@test.com", first_name=f.first_name(), middle_name=f.first_name(
            ), last_name=f.last_name(), grade=random.randint(5, 8), biography=f.paragraph(nb_sentences=3, variable_nb_sentences=False),
            ).save()


def create_events(n=30):
    types = ['Competition', 'Show', 'Fundraiser', 'Trip', 'Fair']
    locations = ['Auditorium', 'Gymnasium',
                 'Outdoor Court', 'Cafeteria', 'Main Field']

    for i in range(n):
        if i % 2 == 0:
            start_delta = datetime.timedelta(hours=random.randint(0, 24*7))
        else:
            start_delta = datetime.timedelta(hours=random.randint(-24*7, -3))

        starts_on = datetime.datetime.now(tz=timezone.utc) + start_delta
        Event(title=f.paragraph(nb_sentences=1, variable_nb_sentences=False)[:-1],
              description=f.paragraph(
                  nb_sentences=3, variable_nb_sentences=False),
              type=random.choice(types),
              location=random.choice(locations),
              starts_on=starts_on,
              finishes_on=starts_on +
              datetime.timedelta(hours=random.randint(1, 3)),
              image=f.image_url(
                  placeholder_url=f"https://picsum.photos/seed/{random.randint(10000, 99999)}/300"),
              points=random.randint(50, 100)).save()


def create_attendance(n=5):
    for student in Student.objects.all():
        events = random.sample(
            [e.pk for e in Event.objects.all()], random.randint(1, n))
        for event in events:
            event_object = Event.objects.get(pk=event)
            attended = random.choice(
                (True, False)) if event_object.finishes_on < datetime.datetime.now(tz=timezone.utc) else None
            Attendance(student=student, event=event_object,
                       attended=attended).save()


def create_news(n=5):
    for _ in range(n):
        content = ""
        for _ in range(random.randint(1, 5)):
            content += f"### {f.paragraph(nb_sentences=1, variable_nb_sentences=False)[:-1]}\n\n"
            for i in range(random.randint(2, 5)):
                content += f"{f.paragraph(nb_sentences=5)}\n\n"
                content += random.choice(
                    ["", "", "", "", f"![image{i}](https://picsum.photos/seed/{random.randint(10000, 99999)}/300)"]) + "\n\n"
        news = News(title=f.paragraph(nb_sentences=1,
                                      variable_nb_sentences=False)[:-1], content=content)
        news.save()
        news.created_on = datetime.datetime.now(tz=timezone.utc
                                                ) - datetime.timedelta(days=random.randint(1, 7))
        news.save()


def create_prizes(n=5):
    types = ['School', 'Food', 'Spirit']
    for student in Student.objects.all():
        for _ in range(random.randint(1, n)):
            Prize(type=random.choice(types), student=student).save()


def create_or_update_rally():
    starts_on = datetime.datetime.now(
        tz=timezone.utc) + datetime.timedelta(days=30)
    if len(Rally.objects.all()) == 0:
        print("Created rally")
        Rally(starts_on=starts_on).save()
    else:
        print("Updated rally")
        rally = Rally.objects.get()
        rally.starts_on = starts_on
        rally.save()


def create_or_update_leaderboard():
    calculate_live_points()
    if len(Leaderboard.objects.all()) == 0:
        print("Created leaderboard")
        Leaderboard().save()

    students = Student.objects.all().order_by('-live_points')
    for i, student in enumerate(students, 1):
        student.rank = i
        student.points = student.live_points
        student.save()


def calculate_live_points():
    for student in Student.objects.all():
        for attendance in student.events.all():
            if attendance.attended:
                student.live_points += attendance.event.points
        student.save()


def create_reports(n=5):
    for d in range(n):
        created_on = datetime.date.today() - datetime.timedelta(days=d*5)
        for student in Student.objects.all():
            report = Report(first_name=student.first_name or student.email,
                            middle_name=student.middle_name or None,
                            last_name=student.last_name or None,
                            grade=student.grade or None,
                            points=random.randint(0, 100))
            report.save()
            report.created_on = created_on
            report.save()


def create_admin():
    if len(Admin.objects.all()) == 0:
        print("Created admin")
        Admin(pk="ubdAzZeNbHca1S1Gaeq0iKOGwuv1")


f = Faker('en_US')
delete_all_objects()
create_all()
