from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django import forms
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from functools import reduce
from itertools import chain

import json

from .models import Address, Board, Membership, Person, NeedsReview

def index(request):
    context = {}
    return render(request, 'members/welcome.html', context)

@login_required
def list_all(request):
    all_members = Person.objects.all()
    paginator = Paginator(all_members, 10)
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)
    context = {
        'members': members,
        'view': 'list_all',
    }
    return render(request, 'members/output.html', context)

class ListBoardView(LoginRequiredMixin, View):

    def get(self, request):
        board_members = Board.objects.all()
        paginator = Paginator(board_members, 10)
        page_number = request.GET.get('page')
        members = paginator.get_page(page_number)
        context = {
            'members': members,
            'view': 'list_board',
        }
        return render(request, 'members/output.html', context)

@login_required
def list_active(request):
    active_members = Membership.objects.filter(status='Active')
    paginator = Paginator(active_members, 10)
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)
    context = {
        'members': members,
        'view': 'active_members'
    }
    return render(request, 'members/output.html', context)

@login_required
def list_inactive(request):
    inactive_members = Membership.objects.filter(status='Inactive')
    paginator = Paginator(inactive_members, 10)
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)
    context = {
        'members': members,
        'view': 'inactive_members'
    }
    return render(request, 'members/output.html', context)

@login_required
def needs_review(request):
    tickets = NeedsReview.objects.filter()
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)
    context = {
        'tickets': tickets,
    }
    return render(request, 'members/list_tickets.html', context)

@login_required
def search_results(request):
    querystring = request.GET['q']
    try:
        filter = request.GET['f']
    except:
        pass
    two_names_orig = querystring.split("and")
    two_names = []
    for name in two_names_orig:
        two_names.append(name.strip())

    search_terms = querystring.split()
    search_terms = list(dict.fromkeys(search_terms))
    try:
        search_terms.remove('and')
    except:
        pass

    member_records = Person.objects.all()
    try:
        member_records = member_records.filter(board_member=True)
    except:
        pass
    exact_match = member_records.filter(first_name=querystring)
    members_name1_2n = member_records.filter(reduce(Q.__or__, [Q(first_name__istartswith=word) for word in two_names])) # was icontains
    members_name2_2n = member_records.filter(reduce(Q.__or__, [Q(last_name__istartswith=word) for word in two_names])) # was icontains
    members_name1_swst = member_records.filter(reduce(Q.__or__, [Q(first_name__istartswith=word) for word in search_terms])) # was icontains
    members_name2_swst = member_records.filter(reduce(Q.__or__, [Q(last_name__istartswith=word) for word in search_terms])) # was icontains
    members_name1_ewst = member_records.filter(reduce(Q.__or__, [Q(first_name__iendswith=word) for word in search_terms])) # was icontains
    members_name2_ewst = member_records.filter(reduce(Q.__or__, [Q(last_name__iendswith=word) for word in search_terms])) # was icontains
    members_name1_cst = member_records.filter(reduce(Q.__or__, [Q(first_name__icontains=word) for word in search_terms]))
    members_name2_cst = member_records.filter(reduce(Q.__or__, [Q(last_name__icontains=word) for word in search_terms]))
    # print(exact_match.exists())
    # print(members_name1.exists())
    # print(members_name2.exists())

    if exact_match.exists():
        context = {
            'members': exact_match,
            'querystring': querystring,
            'view': 'search_page',
            'match': '1:exact',
        }
        return render(request, 'members/output.html', context)
    elif members_name1_2n.exists() or members_name2_2n.exists():
        members = list(dict.fromkeys(chain(members_name1_2n, members_name2_2n)))
        context = {
            'members': members,
            'querystring': querystring,
            'view': 'search_page',
            'match': '2:pairs',
        }
        return render(request, 'members/output.html', context)
    elif members_name1_swst.exists() or members_name2_swst.exists():
        members = list(dict.fromkeys(chain(members_name1_swst, members_name2_swst)))
        context = {
            'members': members,
            'querystring': querystring,
            'view': 'search_page',
            'match': '2:swst',
        }
        return render(request, 'members/output.html', context)
    elif members_name1_ewst.exists() or members_name2_ewst.exists():
        members = list(dict.fromkeys(chain(members_name1_ewst, members_name2_ewst)))
        context = {
            'members': members,
            'querystring': querystring,
            'view': 'search_page',
            'match': '2:ewst',
        }
        return render(request, 'members/output.html', context)
    elif members_name1_cst.exists() or members_name2_cst.exists():
        members = list(dict.fromkeys(chain(members_name1_cst, members_name2_cst)))
        context = {
            'members': members,
            'querystring': querystring,
            'view': 'search_page',
            'match': '3:words',
        }
        return render(request, 'members/output.html', context)
    else:
        members = []
        context = {
            'members': members,
            'querystring': querystring,
            'view': 'search_page',
            'match': '3:words',
        }
        return render(request, 'members/output.html', context)

@login_required
def show_person(request, person_id):
    message = request.GET.get('message', '')
    person = Person.objects.get(id=person_id)
    membership = Membership.objects.get(Q(person1__id=person_id) | Q(person2__id=person_id))
    try:
        board = Board.objects.get(person1__id=person_id)
    except:
        board = False
    context = {
        'person': person,
        'board': board,
        'membership': membership,
        'message': message,
        'view': 'show_person',
    }
    return render(request, 'members/show_person.html', context)

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

@login_required
def edit_person(request, person_id):
    people = Person.objects.all()
    person = people.get(id=person_id)
    address = get_object_or_404(Address, id=person.address.id)
    membership = get_object_or_404(Membership, person1=person_id)
    form = AddressForm(instance=address)
    try:
        querystring = request.GET['from']
    except:
        querystring = ''
    context = {
        'person': person,
        'people': people,
        'membership': membership,
        'form': form,
        'querystring': querystring,
        'view': 'edit_person',
    }
    return render(request, 'members/edit_person.html', context)

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    print(address)
    form = AddressForm(instance=address)
    print(form)
    return render(request, 'members/edit_address.html', {'form': form})

@login_required
def save_person(request):
    return HttpResponse("Hello world!")

@login_required
def show_member(request, member_id):
    message = request.GET.get('message', '')
    membership = get_object_or_404(Membership, id=member_id)
    try:
        querystring = request.GET['from']
    except:
        querystring = ''
    context = {
        'membership': membership,
        'message': message,
        'querystring': querystring,
        'view': 'show_member',
    }
    return render(request, 'members/show_membership.html', context)

@login_required
def edit_member(request, member_id):
    member = Membership.objects.get(id=member_id)
    address = get_object_or_404(Address, id=member.address.id)
    form = AddressForm(instance=address)
    people = Person.objects.all()
    try:
        querystring = request.GET['from']
    except:
        querystring = ''
    context = {
        'member': member,
        'people': people,
        'form': form,
        'querystring': querystring,
        'view': 'edit_member',
    }
    return render(request, 'members/edit_member.html', context)

def save_member(request):
    member_id = request.POST['member_id']
    member_info = Member.objects.get(id=member_id)
    member_info.name1 = request.POST['name1'].strip()
    member_info.sort_by = request.POST['sort_by'].strip()
    member_info.byline = request.POST['byline'].strip()
    member_info.name2 = request.POST['name2'].strip()
    member_info.note = request.POST['note'].strip()
    member_info.address1 = request.POST['address1'].strip()
    member_info.address2 = request.POST['address2'].strip()
    member_info.city = request.POST['city'].strip()
    member_info.state = request.POST['state'].strip()
    member_info.postal_code = request.POST['postal_code'].strip()
    member_info.email1 = request.POST['email1'].strip()
    member_info.email2 = request.POST['email2'].strip()
    member_info.phone_number1 = request.POST['phone_number1'].strip()
    member_info.phone_number2 = request.POST['phone_number2'].strip()
    member_info.membership_status = request.POST['membership_status']
    member_info.membership_type = request.POST['membership_type']

    try:
        board_member = request.POST['board_member']
        if board_member == 'on':
            member_info.board_member = True
    except:
        member_info.board_member = False

    member_info.role = request.POST['role'].strip()

    try:
        directory_optout = request.POST['directory_optout']
        if directory_optout == 'on':
            member_info.directory_optout = True
    except:
        member_info.directory_optout = False

    try:
        needs_review = request.POST['needs_review']
        if needs_review == 'on':
            member_info.needs_review = True
    except:
        member_info.needs_review = False

    member_info.reason_for_review = request.POST['reason_for_review'].strip()
    member_info.save()

    return HttpResponseRedirect(reverse('members_app:show_member', kwargs={'member_id':member_id})+'?message=changes_saved')
