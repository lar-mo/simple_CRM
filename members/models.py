from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models import Q

from django.utils import timezone
import datetime
import django, platform

from multiselectfield import MultiSelectField

def all_member_count(user):
    number_of_all_members = Person.objects.count()
    return number_of_all_members
User.add_to_class('all_member_count', all_member_count)

def board_member_count(user):
    number_of_board_members = Board.objects.count()
    return number_of_board_members
User.add_to_class('board_member_count', board_member_count)

def committee_member_count(user):
    # number_of_committee_members = '10'
    number_of_committee_members = Board.objects.filter(~Q(committees='')).order_by('person1__last_name').count()
    return number_of_committee_members
User.add_to_class('committee_member_count', committee_member_count)

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

def one_year_from_today():
    return timezone.now() + datetime.timedelta(days=365)

class Address(models.Model):
    AL = 'AL' # key = 'db value'
    AK = 'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'
    STATE_CHOICES = [
            (AL, 'Alabama'), # (key, 'select option text'),
            (AK, 'Alaska'),
            (AZ, 'Arizona'),
            (AR, 'Arkansas'),
            (CA, 'California'),
            (CO, 'Colorado'),
            (CT, 'Connecticut'),
            (DE, 'Delaware'),
            (DC, 'District Of Columbia'),
            (FL, 'Florida'),
            (GA, 'Georgia'),
            (HI, 'Hawaii'),
            (ID, 'Idaho'),
            (IL, 'Illinois'),
            (IN, 'Indiana'),
            (IA, 'Iowa'),
            (KS, 'Kansas'),
            (KY, 'Kentucky'),
            (LA, 'Louisiana'),
            (ME, 'Maine'),
            (MD, 'Maryland'),
            (MA, 'Massachusetts'),
            (MI, 'Michigan'),
            (MN, 'Minnesota'),
            (MS, 'Mississippi'),
            (MO, 'Missouri'),
            (MT, 'Montana'),
            (NE, 'Nebraska'),
            (NV, 'Nevada'),
            (NH, 'New Hampshire'),
            (NJ, 'New Jersey'),
            (NM, 'New Mexico'),
            (NY, 'New York'),
            (NC, 'North Carolina'),
            (ND, 'North Dakota'),
            (OH, 'Ohio'),
            (OK, 'Oklahoma'),
            (OR, 'Oregon'),
            (PA, 'Pennsylvania'),
            (RI, 'Rhode Island'),
            (SC, 'South Carolina'),
            (SD, 'South Dakota'),
            (TN, 'Tennessee'),
            (TX, 'Texas'),
            (UT, 'Utah'),
            (VT, 'Vermont'),
            (VA, 'Virginia'),
            (WA, 'Washington'),
            (WV, 'West Virginia'),
            (WI, 'Wisconsin'),
            (WY, 'Wyoming'),
    ]
    description             = models.CharField(max_length=100, blank=False)
    address_1               = models.CharField(max_length=100, blank=False)
    address_2               = models.CharField(max_length=100, blank=True)
    city                    = models.CharField(max_length=100, blank=False)
    state                   = models.CharField(max_length=20, blank=False, choices=STATE_CHOICES)
    postal_code             = models.CharField(max_length=20, blank=False)
    country                 = models.CharField(max_length=30, blank=False, default="US")

    def __str__(self):
        return "{} - {}".format(self.description, self.address_1)

    class Meta:
        ordering = ['description']

class Person(models.Model):
    first_name              = models.CharField(max_length=100, blank=False)
    last_name               = models.CharField(max_length=100, blank=False)
    byline                  = models.CharField(max_length=100, blank=True)
    nickname                = models.CharField(max_length=100, blank=True)
    phone_number            = models.CharField(max_length=20, blank=True)
    email                   = models.EmailField(blank=True)
    address = models.ForeignKey(
                Address,
                on_delete=models.CASCADE,
                related_name='address',
                blank=True,
                null=True,
    )
    notes                   = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.id)

    class Meta:
        ordering = ['last_name']


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
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    MEMBERSHIP_STATUS_CHOICES = [
            (ACTIVE, 'Active'),
            (INACTIVE, 'Inactive'),
    ]
    person1 = models.OneToOneField(
            Person,
            on_delete=models.CASCADE,
            related_name='person_1',
            null=True,
    )
    person2 = models.OneToOneField(
            Person,
            on_delete=models.CASCADE,
            blank=True,
            related_name='person_2',
            null=True,
    )
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='member_address', null=True)
    level = models.CharField(
            max_length=20,
            choices=MEMBER_LEVEL_CHOICES,
            default=SUPPORTER,
            blank=False,
    )
    expiration              = models.DateField(default=one_year_from_today, null=True, blank=True)
    status = models.CharField(
            max_length=10,
            choices=MEMBERSHIP_STATUS_CHOICES,
            default=ACTIVE,
            blank=True,
    )
    notes                   = models.CharField(max_length=300, blank=True)

    def __str__(self):
        if self.person2:
            return "{} ({}, {})".format(self.level, self.person1, self.person2)
        else:
            return "{} ({})".format(self.level, self.person1)

    class Meta:
        ordering = ['level', 'person1__last_name']

class Board(models.Model):
    PRESIDENT = 'President'
    VICE_PRESIDENT = 'Vice President'
    SECRETARY = 'Secretary'
    TREASURER = 'Treasurer'
    PAST_PRESIDENT = 'Past President'
    COMMITTEE = 'Committee'
    BOARD_TITLE_CHOICES = [
        (PRESIDENT, 'President'),
        (VICE_PRESIDENT, 'Vice President'),
        (SECRETARY, 'Secretary'),
        (TREASURER, 'Treasurer'),
        (PAST_PRESIDENT, 'Past President'),
        (COMMITTEE, 'Committee'),
    ]

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
    HOSPITALITY_BEVERAGES = 'Hopitality: Beverages'
    HOSPITALITY_FOOD = 'Hopitality: Food'
    HOSPITALITY_GREETER = 'Hopitality: Greeter'
    HOSPITALITY_RSVPS_NAMETAGS = 'Hopitality: RSVPs/Name Tags'
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
        (HOSPITALITY_BEVERAGES, 'Hopitality: Beverages'),
        (HOSPITALITY_FOOD, 'Hopitality: Food'),
        (HOSPITALITY_GREETER, 'Hopitality: Greeter'),
        (HOSPITALITY_RSVPS_NAMETAGS, 'Hopitality: RSVPs/Name Tags'),
        (TRAVEL, 'Travel'),
        (BOT_COUNCIL_LIAISON, 'Board of Trustees Council Liaison'),
        (COUNCIL_COORDINATOR, 'Council Coordinator'),
    ]

    person1     = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True, related_name='board_member')
    title       = models.CharField(max_length=20,choices=BOARD_TITLE_CHOICES)
    committees  = MultiSelectField(max_length=50, choices=COMMITTEE_ROLE_CHOICES, blank=True)

    def __str__(self):
        if len(self.committees) == 0:
            return "{} - {} {}".format(self.title, self.person1.first_name, self.person1.last_name)
        else:
            return "{} - {} {} (Cmtes: {})".format(self.title, self.person1.first_name, self.person1.last_name, self.committees)

    class Meta:
        ordering = ['id']

class NeedsReview(models.Model):
    NAME = 'Name'
    ADDRESS = 'Address'
    EMAIL = 'Email'
    PHONE_NUMBER = 'Phone Number'
    PARTNER = 'Partner'
    MEMBERSHIP = 'Council Membership'
    BOARD = 'Board Membership'
    COMMITTEE = 'Committee Membership'
    REASON_CHOICES = [
        (NAME, 'Name'),
        (ADDRESS, 'Address'),
        (EMAIL, 'Email'),
        (PHONE_NUMBER, 'Phone Number'),
        (PARTNER, 'Partner'),
        (MEMBERSHIP, 'Council Membership'),
        (BOARD, 'Board Membership'),
        (COMMITTEE, 'Committee Membership'),
    ]
    OPEN = 'Open'
    ASSIGNED = 'Assigned'
    CLOSED = 'Closed'
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('ASSIGNED', 'Assigned'),
        ('CLOSED', 'Closed'),
    ]

    summary             = models.CharField(max_length=100, null=True)
    description         = models.TextField(null=True)
    component           = models.CharField(max_length=30, choices=REASON_CHOICES)
    person              = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True, related_name='nr_person')
    member              = models.ForeignKey(Membership, on_delete=models.CASCADE, blank=True, null=True, related_name='nr_member')
    status              = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPEN',
    )
    assignee                = models.ForeignKey(
        Board,
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
