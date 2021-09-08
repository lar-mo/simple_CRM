from django.db import models
from django.contrib.auth.models import User
# from multiselectfield import MultiSelectField

class Address(models.Model):
    description                 = models.CharField(max_length=100, blank=False)
    address_1                   = models.CharField(max_length=100, blank=False)
    address_2                   = models.CharField(max_length=100, blank=True)
    city                        = models.CharField(max_length=100, blank=False)
    state                       = models.CharField(max_length=20, blank=False)
    postal_code                 = models.CharField(max_length=20, blank=False)
    country                     = models.CharField(max_length=30, blank=False, default="US")
    PRIMARY = 'Primary'
    SECONDARY = 'Secondary'
    ADDRESS_TYPE_CHOICES = [
        (PRIMARY, 'Primary'),
        (SECONDARY, 'Secondary'),
    ]
    type                        = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE_CHOICES,
        default=PRIMARY,
        blank=False,
    )

    def __str__(self):
        return "{} ({})".format(self.address_1, self.description)

class Person(models.Model):
    first_name             = models.CharField(max_length=100)
    last_name              = models.CharField(max_length=100)
    byline                 = models.CharField(max_length=100, blank=True)
    nickname               = models.CharField(max_length=100, blank=True)
    phone_number           = models.CharField(max_length=20, blank=True)
    email                  = models.EmailField()
    partner                = models.ForeignKey('self', on_delete=models.CASCADE, related_name='person', blank=True, null=True)
    address                = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address', blank=True, null=True)
    # membership             = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='membership', blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

class Membership(models.Model):
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
    member                      = models.ManyToManyField(Person)

    def __str__(self):
        # return "{}".format(self.level)
        members = ["{} {}".format(x.first_name, x.last_name) for x in self.member.all()]
        members = ', '.join(map(str, members))
        return "{} - {}".format(self.level, members)

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
    # COMMITTEE_MEMBERS = [("Larry Moiola", "Larry"),("Susan Jones", "Sue"),("Paul Virzi","Paul")]
    person                      = models.ManyToManyField(Person, blank=True)
    # person                      = MultiSelectField(choices=COMMITTEE_MEMBERS, blank=True, null=True)

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
        blank=True,
    )
    person                      = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='board_member')

    def __str__(self):
        return "{}: {} {}".format(self.title, self.person.first_name, self.person.last_name)
