from rest_framework import serializers
# from graphene_django.rest_framework import SerializerMutation
import graphene
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
from .models import Admin, AdminAnnouncement, Student, Event, Attendance, News, Report, Rally, Leaderboard, Prize
from .serializers.admin import AdminAnnouncementSerializer


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        field = ('id', 'email', 'first_name', 'middle_name', 'last_name',
                 'biography', 'grade', 'image', 'balance', 'current_points', 'rank')


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        field = ('id', 'title', 'description', 'type', 'location', 'starts_on',
                 'finishes_on', 'image', 'points', 'cancelation_reason')


class AttendanceType(DjangoObjectType):
    class Meta:
        model = Attendance
        field = ('id', 'student', 'event', 'attended', 'final')


class NewsType(DjangoObjectType):
    class Meta:
        model = News
        field = ('id', 'title', 'content', 'created_on')


class ReportType(DjangoObjectType):
    class Meta:
        model = Report
        field = ('id', 'created_on', 'first_name', 'middle_name',
                 'last_name', 'points', 'grade')


class RallyType(DjangoObjectType):
    class Meta:
        model = Rally
        field = ('id', 'starts_on')


class LeaderboardType(DjangoObjectType):
    class Meta:
        model = Leaderboard
        field = ('id', 'created_on')


class PrizeType(DjangoObjectType):
    class Meta:
        model = Prize
        field = ('id', "type", 'student')


class AdminType(DjangoObjectType):
    class Meta:
        model = Admin
        field = ("id")


#############################

class AdminAnnouncementType(DjangoObjectType):
    class Meta:
        model = AdminAnnouncement
        field = ("title", "content", "created_on", "expires_on")


class CreateAdminAnnouncementMutation(SerializerMutation):
    class Meta:
        serializer_class = AdminAnnouncementSerializer
        return_field_name = 'adminAnnouncement'

#####################################


class Query(graphene.ObjectType):
    retrieve_admin = graphene.Field(AdminType, id=graphene.String())
    list_admin_announcement = graphene.List(AdminAnnouncementType)
    list_events_by_type = graphene.List(
        EventType, type=graphene.String(), count=graphene.Int())

    def resolve_retrieve_admin(root, info, id):
        return Admin.objects.get(id=id)

    def resolve_list_admin_announcement(root, info):
        return AdminAnnouncement.objects.all()

    def resolve_list_events_by_type(root, info, type, count):
        return Event.objects.all().filter(
            type=type).order_by('starts_on')[:count or None]


class Mutation(graphene.ObjectType):
    create_admin_announcement = CreateAdminAnnouncementMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
