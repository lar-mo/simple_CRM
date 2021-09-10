from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
import datetime
import django, platform

def all_member_count(user):
    number_of_all_members = Person.objects.count()
    return number_of_all_members
User.add_to_class('all_member_count', all_member_count)

def board_member_count(user):
    number_of_board_members = Board.objects.count()
    return number_of_board_members
User.add_to_class('board_member_count', board_member_count)

def active_member_count(user):
    number_of_active_members = Membership.objects.filter(status='Active').count()
    return number_of_active_members
User.add_to_class('active_member_count', active_member_count)

def inactive_member_count(user):
    number_of_inactive_members = Membership.objects.filter(status='Inactive').count()
    return number_of_inactive_members
User.add_to_class('inactive_member_count', inactive_member_count)

def needs_review_count(user):
    number_of_needs_review = NeedsReview.objects.filter().exclude(status='Closed').count()
    return number_of_needs_review
User.add_to_class('needs_review_count', needs_review_count)

class Address(models.Model):
    description                 = models.CharField(max_length=100, blank=False)
    address_1                   = models.CharField(max_length=100, blank=False)
    address_2                   = models.CharField(max_length=100, blank=True)
    city                        = models.CharField(max_length=100, blank=False)
    state                       = models.CharField(max_length=20, blank=False)
    postal_code                 = models.CharField(max_length=20, blank=False)
    country                     = models.CharField(max_length=30, blank=False, default="US")

    def __str__(self):
        return "{} - {}".format(self.description, self.address_1)

    class Meta:
        ordering = ['description']

class Membership(models.Model):
    description                 = models.CharField(max_length=100, blank=False)
    SUPPORTER = 'Supporter'
    CONTRIBUTOR = 'Contributor'
    ADVOCATE = 'Advocate'
    HONORARY = 'Honorary'
    PAM_STAFF = 'PAM staff'
    MEMBER_LEVEL_CHOICES = [
        (SUPPORTER, 'Supporter'),
        (CONTRIBUTOR, 'Contributor'),
        (ADVOCATE, 'Advocate'),
        (HONORARY, 'Honorary'),
        (PAM_STAFF, 'PAM staff'),
    ]
    level                       = models.CharField(
        max_length=20,
        choices=MEMBER_LEVEL_CHOICES,
        default=SUPPORTER,
        blank=False,
    )
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    MEMBERSHIP_STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    status                      = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_STATUS_CHOICES,
        default=ACTIVE,
        blank=True,
    )

    def __str__(self):
        return "{} - {} ({})".format(self.description, self.level, self.status)
        # members = ["{} {}".format(x.first_name, x.last_name) for x in self.member.all().distinct()]
        # members = ', '.join(map(str, members))
        # return "{} - {}".format(self.level, members)

    # class Meta:
        # ordering = ['member__last_name']

class Person(models.Model):
    first_name             = models.CharField(max_length=100)
    last_name              = models.CharField(max_length=100)
    byline                 = models.CharField(max_length=100, blank=True)
    nickname               = models.CharField(max_length=100, blank=True)
    phone_number           = models.CharField(max_length=20, blank=True)
    email                  = models.EmailField(blank=True)
    partner                = models.ForeignKey('self', on_delete=models.CASCADE, related_name='person', blank=True, null=True)
    address                = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address', blank=True, null=True)
    membership             = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='membership', blank=True, null=True)

    def __str__(self):
        ## corresponds with ManyToManyField above
        # address = self.address.values_list('address_1', flat=True)
        # address = [item for item in address]
        return "{} {} ({}), {}".format(self.first_name, self.last_name, self.address, self.membership)

    class Meta:
        ordering = ['last_name']

class Committee(models.Model):
    ADVISORY = 'Advisory'
    ARCHIVES = 'Archives'
    BOOK_CLUB = 'Book Club'
    COMMUNICATION = 'Communication'
    DAY_TRIPS = 'Day Trips'
    MEMBERSHIPS = 'Memberships'
    MEMBERSHIP_DEV = 'Membership Development'
    DIRECTORY = 'Directory'
    PHOTOGRAPHER = 'Photographer'
    PROGRAMS = 'Programs'
    SPECIAL_EVENTS = 'Special Events'
    HOSPITALITY = 'Hospitality'
    # HOSPITALITY_BEVERAGES = 'Hopitality: Beverages'
    # HOSPITALITY_FOOD = 'Hopitality: Food'
    # HOSPITALITY_GREETER = 'Hopitality: Greeter'
    # HOSPITALITY_RSVPS_NAMETAGS = 'Hopitality: RSVPs/Name Tags'
    # HOSPITALITY = [
    #         ('beverages', 'Beverages'),
    #         ('food', 'Food'),
    #         ('greeter', 'Greeter'),
    #         ('rsvp_name_tags', 'aRSVPs/Name Tags'),
    # ]
    TRAVEL = 'Travel'
    BOT_COUNCIL_LIAISON = 'Board of Trustees Council Liaison'
    COUNCIL_COORDINATOR = 'Council Coordinator'
    COMMITTEE_ROLE_CHOICES = [
        (ADVISORY, 'Advisory'),
        (ARCHIVES, 'Archives'),
        (BOOK_CLUB, 'Book Club'),
        (COMMUNICATION, 'Communications'),
        (DAY_TRIPS, 'Day Trips'),
        (MEMBERSHIPS, 'Memberships'),
        (MEMBERSHIP_DEV, 'Membership Development'),
        (DIRECTORY, 'Directory'),
        (PHOTOGRAPHER, 'Photographer'),
        (PROGRAMS, 'Programs'),
        (SPECIAL_EVENTS, 'Special Events'),
        # (HOSPITALITY_BEVERAGES, 'Hopitality: Beverages'),
        # (HOSPITALITY_FOOD, 'Hopitality: Food'),
        # (HOSPITALITY_GREETER, 'Hopitality: Greeter'),
        # (HOSPITALITY_RSVPS_NAMETAGS, 'Hopitality: RSVPs/Name Tags'),
        (HOSPITALITY, [
                    ('Hopitality: Beverages', 'Beverages'),
                    ('Hopitality: Food', 'Food'),
                    ('Hopitality: Greeter', 'Greeter'),
                    ('Hopitality: RSVP and Name Tags', 'RSVPs/Name Tags'),
        ]),
        (TRAVEL, 'Travel'),
        (BOT_COUNCIL_LIAISON, 'Board of Trustees Council Liaison'),
        (COUNCIL_COORDINATOR, 'Council Coordinator'),
    ]
    role                        = models.CharField(
        max_length=40,
        choices=COMMITTEE_ROLE_CHOICES,
        blank=True,
    )
    person                      = models.ManyToManyField(Person, blank=True)

    def __str__(self):
        person_list = ["{} {}".format(x.first_name, x.last_name) for x in self.person.all()]
        people = ''
        for i in range(len(person_list)):
            if i == len(person_list)-1 and len(person_list) > 1:
                people += ", and {}".format(person_list[i])
            elif i == 0:
                people+= "- {}".format(person_list[i])
            else:
                people += ", {}".format(person_list[i])
        # people = list(zip(people_fn, people_ln))
        return "{} {}".format(self.role, people)

    @classmethod
    def get_cmte_members(cls):
        roles_with_people = cls.objects.exclude(person__isnull=True)
        role_list = [x for x in roles_with_people.all().order_by('role')]
        return role_list

    # class Meta:
    #     ordering = ['person']

class Board(models.Model):
    PRESIDENT = 'President'
    VICE_PRESIDENT = 'Vice President'
    SECRETARY = 'Secretary'
    TREASURER = 'Treasurer'
    PAST_PRESIDENT = 'Past President'
    BOARD_TITLE_CHOICES = [
        (PRESIDENT, 'President'),
        (VICE_PRESIDENT, 'Vice President'),
        (SECRETARY, 'Secretary'),
        (TREASURER, 'Treasurer'),
        (PAST_PRESIDENT, 'Past President'),
    ]
    title                       = models.CharField(
        max_length=20,
        choices=BOARD_TITLE_CHOICES,
        unique=True,
    )
    person                      = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='board_member')

    def __str__(self):
        return "{} - {} {}".format(self.title, self.person.first_name, self.person.last_name)

    class Meta:
        ordering = ['person']

class NeedsReview(models.Model):
    summary                     = models.CharField(max_length=100, null=True)
    description                 = models.TextField(null=True)
    NAME = 'Name'
    ADDRESS = 'Address'
    EMAIL = 'Email'
    PHONE_NUMBER = 'Phone Number'
    PARTNER = 'Partner'
    MEMBERSHIP = 'Council Membership'
    BOARD = 'Board Membership'
    COMMITTEE = 'Committee Membeship'
    REASON_CHOICES = [
        (NAME, 'Name'),
        (ADDRESS, 'Address'),
        (EMAIL, 'Email'),
        (PHONE_NUMBER, 'Phone Number'),
        (PARTNER, 'Partner'),
        (MEMBERSHIP, 'Council Membership'),
        (BOARD, 'Board Membership'),
        (COMMITTEE, 'Committee Membeship'),
    ]
    component                       = models.CharField(
        max_length=30,
        choices=REASON_CHOICES,
    )
    OPEN = 'Open'
    ASSIGNED = 'Assigned'
    CLOSED = 'Closed'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (ASSIGNED, 'Assigned'),
        (CLOSED, 'Closed'),
    ]
    status                       = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=OPEN,
    )
    assignee                    = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        related_name='assignee',
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.assignee == None:
            assignee = "unassigned"
        else:
            assignee = self.assignee
        return "{} ({})".format(self.summary, assignee)
