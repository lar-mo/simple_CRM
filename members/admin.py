from django.contrib import admin

from .models import Address
from .models import Membership
from .models import Person
from .models import Board
from .models import Committee
from .models import NeedsReview

admin.site.register(Address)
admin.site.register(Membership)
admin.site.register(Person)
admin.site.register(Board)
admin.site.register(Committee)
admin.site.register(NeedsReview)
