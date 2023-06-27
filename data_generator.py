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
    from core.models import Student, Event, EventFeedback, Attendance, News, Prize, PrizeRedemption, Parent, Group, GroupEvent, GroupMember, GroupAnnouncement, Report, Leaderboard, Rally, Admin, AdminAnnouncement


def create_all():
    # feedbacks must be after attendances
    # leaderboard must come before redemptions because leaderboard calculates balance
    create_functions = [create_admin_announcements, create_students, create_events, create_attendance,
                        create_event_feedbacks, create_news, create_or_update_leaderboard, create_prizes,
                        create_prize_redemptions, create_parents, create_groups, create_or_update_rally,
                        create_reports, create_admin]

    print("Started creating")
    for fun in create_functions:
        fun()
    print("Finished creating")


def delete_all_objects():
    print("Started deleting all objects")
    models = [Student, Event, EventFeedback, Attendance, News, Prize, PrizeRedemption,
              Parent, Group, GroupEvent, GroupMember, GroupAnnouncement, Report, AdminAnnouncement, Admin]
    for model in models:
        model.objects.all().delete()
    print("Finished deleting all objects")


def create_admin_announcements(n=5):
    for _ in range(n):
        AdminAnnouncement(title=f.paragraph(nb_sentences=1, variable_nb_sentences=False), content=f.paragraph(nb_sentences=3, variable_nb_sentences=False), created_on=datetime.datetime.now(
            tz=timezone.utc), expires_on=datetime.datetime.now(
            tz=timezone.utc) + datetime.timedelta(hours=random.randint(1, 96))).save()


def create_students():
    # ids must be in this specific order
    ids = ['OKHufehFqpb0pvkAmlRqA3KWcyF3', 'AQYWFdX0HDXYA2kD1IDjp6Ycr6B3',
           '48Z13hlv0sg5TDoCyuzlA2XHJ9n2', 'IZmJYyIJ3raqSMbSkkWuY6zRVEF2',
           'c9H2ZfvcA2Z2OMqfhZzclx32PuI2',]

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


def create_event_feedbacks():
    for student in Student.objects.all():
        for event in student.events.all():
            if event.attended:
                EventFeedback(student=student, event=event.event, rating=random.randint(
                    1, 5), content=f.paragraph(nb_sentences=3, variable_nb_sentences=False)).save()


def create_attendance(n=5):
    for student in Student.objects.all():
        events = random.sample(
            [e.id for e in Event.objects.all()], random.randint(1, n))
        for event in events:
            event_object = Event.objects.get(id=event)
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


def create_prizes(n=6):
    types = ['School', 'Food', 'Spirit']
    for i in range(n):
        Prize(name=f"Prize {i}",
              type=random.choice(types),
              cost=random.randint(10, 30)).save()


def create_prize_redemptions(n=3):
    for student in Student.objects.all():
        while True:
            prize = random.choice(Prize.objects.all())
            if student.balance < prize.cost:
                break

            student.balance -= prize.cost
            PrizeRedemption(prize=prize, student=student, redeemed_on=datetime.datetime.now(
                tz=timezone.utc) - datetime.timedelta(days=random.randint(1, 4)), is_approved=random.choice([True, False])).save()
            student.save()


def create_parents():
    # ids must be in this order
    ids = ['a3zVrpnuAUbfudBYERveSLNT16R2',
           'XwUDHI0SbscijUNj3fcRLLNr3aL2', 'CwzKpzGeFdMXu1KSaBua9IWjvRW2']
    for i, id in enumerate(ids):
        parent = Parent(id=id, email=f"parent{i}@test.com", first_name=f.first_name(
        ), middle_name=f.first_name(), last_name=f.last_name())
        parent.save()
        for _ in range(random.randint(1, 3)):
            student = random.choice(Student.objects.all())
            if len(student.parents.all()) < 2:
                parent.kids.add(student)


def create_groups(n=3):
    for _ in range(n):
        group = Group(name=f.paragraph(nb_sentences=1, variable_nb_sentences=False), description=f.paragraph(
            nb_sentences=3, variable_nb_sentences=False), is_private=random.choice([True, False]))

        group.save()

        for _ in range(3):
            student = random.choice(Student.objects.all())
            group.members.create(
                member=student, is_admin=random.choice([True, False]))

        for _ in range(5):
            member = random.choice(group.members.all())
            event = random.choice(Event.objects.all())
            if event not in group.events.all():
                group.events.create(event=event, added_by=member.member)

        for _ in range(3):
            group.announcements.create(created_by=random.choice(group.members.all()).member, created_on=datetime.datetime.now(
                tz=timezone.utc), content=f.paragraph(nb_sentences=5))


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
    calculate_balance()
    if len(Leaderboard.objects.all()) == 0:
        print("Created leaderboard")
        Leaderboard().save()

    students = Student.objects.all().order_by('-balance')
    for i, student in enumerate(students, 1):
        student.rank = i
        student.current_points = student.balance
        student.save()


def calculate_balance():
    for student in Student.objects.all():
        for attendance in student.events.all():
            if attendance.attended:
                student.balance += attendance.event.points
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
    print("Created admin")
    Admin(id="9KZ5hyYmkgPl74z1ngclkNhZ1T73").save()


f = Faker('en_US')
delete_all_objects()
create_all()
