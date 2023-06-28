from rest_framework import serializers
# from graphene_django.rest_framework import SerializerMutation
import graphene
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
from .models import PrizeRedemption, Admin, AdminAnnouncement, Group, GroupMember, GroupEvent, GroupAnnouncement, Student, Event, EventFeedback, Attendance, News, Report, Rally, Leaderboard, Prize
from .serializers.admin import AdminAnnouncementSerializer
from .serializers.event_feedback import EventFeedbackSerializer
from datetime import datetime
from django.utils import timezone


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


class AdminType(DjangoObjectType):
    class Meta:
        model = Admin
        field = ("id")

################################


class PrizeType(DjangoObjectType):
    class Meta:
        model = Prize
        field = ('id', 'name', 'type', 'cost')


class PrizeRedemptionType(DjangoObjectType):
    class Meta:
        model = PrizeRedemption
        field = ('id', 'prize', 'student', 'redeemed_on', 'is_approved')

##############################


class GroupMemberType(DjangoObjectType):
    class Meta:
        model = GroupMember
        field = ("member", 'is_admin', 'group')


class GroupAnnouncementType(DjangoObjectType):
    class Meta:
        model = GroupAnnouncement
        field = ('group', 'created_by', 'created_on', 'content')


class GroupEventType(DjangoObjectType):
    class Meta:
        model = GroupEvent
        field = ('group', 'event', 'added_by')


class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        field = ("id", 'name', 'description', 'is_private',
                 'key', 'members', 'events', 'announcements')

#############################


class EventFeedbackType(DjangoObjectType):
    class Meta:
        model = EventFeedback
        field = ('student', 'event', 'rating', 'content')


class CreateEventFeedbackMutation(SerializerMutation):
    class Meta:
        serializer_class = EventFeedbackSerializer
        return_field_name = 'eventFeedback'


#############################


class AdminAnnouncementType(DjangoObjectType):
    class Meta:
        model = AdminAnnouncement
        field = ('title', 'content', 'created_on', 'expires_on')


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
    retrieve_group = graphene.Field(GroupType, id=graphene.String())
    list_groups = graphene.List(GroupType)
    list_prize_redemptions = graphene.List(PrizeRedemptionType)

    def resolve_retrieve_admin(root, info, id):
        return Admin.objects.get(id=id)

    def resolve_list_admin_announcement(root, info):
        return AdminAnnouncement.objects.all()

    def resolve_list_events_by_type(root, info, type, count):
        return Event.objects.all().filter(starts_on__gte=datetime.now(tz=timezone.utc)).filter(type=type).order_by('-starts_on')[:count or None]

    def resolve_retrieve_group(root, info, id):
        return Group.objects.get(id=id)

    def resolve_list_groups(root, info):
        return Group.objects.all().filter(is_private=False)

    def resolve_list_prize_redemptions(root, info):
        return PrizeRedemption.objects.all().filter(is_approved=False)


class Mutation(graphene.ObjectType):
    create_admin_announcement = CreateAdminAnnouncementMutation.Field()
    create_event_feedback = CreateEventFeedbackMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
