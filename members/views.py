from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required, permission_required
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
        'view': 'list_people',
        'title': 'All People' + ' ({})'.format(all_members.count()),
    }
    return render(request, 'members/listing.html', context)

class ListBoardView(LoginRequiredMixin, View):

    def get(self, request):
        board_members = Board.objects.all()
        paginator = Paginator(board_members, 10)
        page_number = request.GET.get('page')
        members = paginator.get_page(page_number)
        context = {
            'members': members,
            'view': 'list_board',
            'title': 'Board Members' + ' ({})'.format(board_members.count()),
        }
        return render(request, 'members/listing.html', context)

@login_required
def list_committees(request):
    choices = Board._meta.get_field('committees').choices #get committee choices from model(Board)
    committee_roles = [x[0] for x in choices] #create list from list of tuples
    committee_roles_dict = dict.fromkeys(committee_roles, []) #create dictionary with value=[]
    board = Board.objects.filter(~Q(committees='')).order_by('person1__last_name') #get only board members with committee role(s)

    # loop through each board member with committee role(s) and add to committee_roles_dict
    for x in board:
        for i in range(len(x.committees)):
            if x.committees[i] in committee_roles_dict.keys(): #this is probably unnecessary
                if len(committee_roles_dict[x.committees[i]]) == 0:
                    committee_roles_dict[x.committees[i]] = [x.person1]
                else:
                    committee_roles_dict[x.committees[i]].append(x.person1)
    context = {
        'choices': committee_roles_dict,
        'view': 'list_board',
        'title': "Committees" + ' ({})'.format(board.count()),
    }
    return render(request, 'members/show_committees.html', context)

@login_required
def list_active(request):
    active_members = Membership.objects.filter(status='Active')
    paginator = Paginator(active_members, 10)
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)
    context = {
        'members': members,
        'view': 'list_active',
        'title': 'Active Members' + ' ({})'.format(active_members.count()),
    }
    return render(request, 'members/listing.html', context)

@login_required
def list_inactive(request):
    inactive_members = Membership.objects.filter(status='Inactive')
    paginator = Paginator(inactive_members, 10)
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)
    context = {
        'members': members,
        'view': 'list_inactive',
        'title': 'Inactive Members' + ' ({})'.format(inactive_members.count()),
    }
    return render(request, 'members/listing.html', context)

@login_required
def search_results(request):

    ### Get the Data

    # Get the value of the 'q' and strip leading & trailing chars (no arg = spaces)
    querystring = request.GET['q'].strip()

    # check if 'f' (board filter) and 'get' it (checkbox value)
    # checked form box returns 'on'/true, unchecked form box returns None
    try:
        board_only = request.GET['board_only']
        filter_by_board = True
    except:
        filter_by_board = False
    # print(filter_by_board)

    ###
    ### Clean up input
    ###

    # split words into list
    search_terms = querystring.split()

    # convert to dict to remove duplicates
    search_terms = list(dict.fromkeys(search_terms))

    # remove common join word (from Jim and Susan Jones); maybe add ampersand
    try:
        search_terms.remove('and')
    except:
        pass

    ###
    ### Get records from database
    ###

    # Rather than made a bunch of filtered calls to the database later, retrieve everything at the beginning
    person_records = Person.objects.all()
    member_records = Membership.objects.all()
    board_records = Board.objects.all()
    board_ids = [x.person1.id for x in board_records]

    if len(search_terms) == 2:
    # Check if there is are exactly 2 items in the cleaned up data (optimal: first and last name)
    # Then, query Person, Member/Person1, Member/Person2
    # Using "filter" to get a QuerySet (instead of an single object) so I can use .exists()
    # * The logic assumes that each Person is a unique fn+ln combo.
    # ** It also expects the search query to be "first name last name"
        exact_match_p = person_records.filter(Q(first_name__iexact=search_terms[0], last_name__iexact=search_terms[1]))
        try:
            exact_match_p_board_info = board_records.get(person1__id=exact_match_p[0].id)
        except:
            exact_match_p_board_info = None
        print("Matched: {}".format(exact_match_p_board_info))
        exact_match_mp1 = member_records.filter(Q(person1__first_name__iexact=search_terms[0], person1__last_name__iexact=search_terms[1]))
        exact_match_mp2 = member_records.filter(Q(person2__first_name__iexact=search_terms[0], person2__last_name__iexact=search_terms[1]))

        if exact_match_p.exists() or exact_match_mp1.exists() and exact_match_mp2.exists():
            members = list(dict.fromkeys(chain(exact_match_p, exact_match_mp1, exact_match_mp2)))
            print(members)
            context = {
                'members': members,
                'querystring': querystring,
                'board_record': exact_match_p_board_info,
                'view': 'search_results',
                    'match': '1:exact',
            }
            return render(request, 'members/listing.html', context)

    # (c)ontains (s)earch (t)erms (reduce(Q.__or__, []) is probably unnecessary)
    person_fn_cst = person_records.filter(reduce(Q.__or__, [Q(first_name__iexact=word) for word in search_terms]))
    person_ln_cst = person_records.filter(reduce(Q.__or__, [Q(last_name__iexact=word) for word in search_terms]))
    member_person1fn_cst = member_records.filter(reduce(Q.__or__, [Q(person1__first_name__iexact=word) for word in search_terms]))
    member_person1ln_cst = member_records.filter(reduce(Q.__or__, [Q(person1__last_name__iexact=word) for word in search_terms]))
    member_person2fn_cst = member_records.filter(reduce(Q.__or__, [Q(person2__first_name__iexact=word) for word in search_terms]))
    member_person2ln_cst = member_records.filter(reduce(Q.__or__, [Q(person2__last_name__iexact=word) for word in search_terms]))

    # check pairs (fn+ln) in Person, Membership/Person1, Membeship/Person2
    if (person_fn_cst.exists() and person_ln_cst.exists()) or (member_person1fn_cst.exists() and member_person1ln_cst.exists()) or (member_person2fn_cst.exists() and member_person2ln_cst.exists()):
        people = list(dict.fromkeys(chain(
                        person_fn_cst,
                        person_ln_cst,
                        member_person1fn_cst,
                        member_person1ln_cst,
                        member_person2fn_cst,
                        member_person2ln_cst,
                        )
                ))
        if filter_by_board:
            for person in people:
                print(person.id)
                if person.id not in board_ids:
                    people.remove(person)
                    print("yep: {}".format(person.id))
        context = {
            'members': people,
            'querystring': querystring,
            'board_records': board_records,
            'view': 'search_results',
            'match': '2:words',
        }
        return render(request, 'members/listing.html', context)
    if person_fn_cst.exists() or person_ln_cst.exists() or member_person1fn_cst.exists() or member_person1ln_cst.exists() or member_person2fn_cst.exists() or member_person2ln_cst.exists():
        people = list(dict.fromkeys(chain(
                        person_fn_cst,
                        person_ln_cst,
                        member_person1fn_cst,
                        member_person1ln_cst,
                        member_person2fn_cst,
                        member_person2ln_cst,
                        )
                ))
        if filter_by_board:
            for person in people:
                print(person.id)
                if person.id not in board_ids:
                    people.remove(person)
                    print("yep: {}".format(person.id))
        context = {
            'members': people,
            'querystring': querystring,
            'board_records': board_records,
            'view': 'search_results',
            'match': '3:single_match',
        }
        return render(request, 'members/listing.html', context)
    else:
        # This catch-all needs work; doesn't really do anything
        # Perhaps if other fields are searchable (TBD)
        # e.g. "asdf" returns nothing becauase an empty list is passed to "members" (just to silently errors on FE)
        members = []
        context = {
            'members': members,
            'querystring': querystring,
            'board_records': board_records,
            'view': 'search_results',
            'match': '4:else',
        }
        return render(request, 'members/listing.html', context)

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
    membership = Membership.objects.filter(person1__id=person_id, person2__id=person_id)
    addr_form = AddressForm(instance=address)
    try:
        querystring = request.GET['from']
    except:
        querystring = ''
    context = {
        'person': person,
        'people': people,
        'address_id': address.id,
        'membership': membership,
        'addr_form': addr_form,
        'querystring': querystring,
        'view': 'edit_person',
    }
    return render(request, 'members/edit_person.html', context)

@permission_required('members.change_address')
@login_required
def save_address(request):
    # print(request.POST)
    addr_id = request.POST['address_id']
    member_id = request.POST['member_id']
    refresh_url = request.POST['refresh_url']
    address_obj = get_object_or_404(Address, id=addr_id)
    address_obj.description = request.POST['description'].strip()
    address_obj.address_1 = request.POST['address_1'].strip()
    address_obj.address_2 = request.POST['address_2'].strip()
    address_obj.city = request.POST['city'].strip()
    address_obj.state = request.POST['state']
    address_obj.postal_code = request.POST['postal_code'].strip()
    address_obj.country = request.POST['country'].strip()
    address_obj.save()
    context = {}
    return HttpResponse()
    # return redirect(refresh_url)
    # return HttpResponseRedirect(reverse('members_app:edit_member', kwargs={'member_id':member_id})+'?message=changes_saved')

@permission_required('members.change_person')
@login_required
def save_person(request):
    person_id = request.POST['person_id']
    address_id = request.POST['address']
    person = get_object_or_404(Person, id=person_id)
    address = get_object_or_404(Address, id=address_id)
    person.first_name = request.POST['first_name']
    person.last_name = request.POST['last_name']
    person.byline = request.POST['byline']
    person.nickname = request.POST['nickname']
    person.phone_number = request.POST['phone_number']
    person.email = request.POST['email']
    person.notes = request.POST['notes']
    person.address = address
    person.save()
    return HttpResponseRedirect(reverse('members_app:show_person', kwargs={'person_id':person_id})+'?message=changes_saved')

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
    return render(request, 'members/show_member.html', context)

@login_required
def edit_member(request, member_id):
    member = Membership.objects.get(id=member_id)
    address = get_object_or_404(Address, id=member.address.id)
    addr_form = AddressForm(instance=address)
    people = Person.objects.all()
    try:
        querystring = request.GET['from']
    except:
        querystring = ''
    context = {
        'member': member,
        'people': people,
        'address_id': address.id,
        'addr_form': addr_form,
        'querystring': querystring,
        'view': 'edit_member',
    }
    return render(request, 'members/edit_member.html', context)

@permission_required('members.change_membership')
@login_required
def save_member(request):
    member_id = request.POST['memberid']
    person1 = request.POST['person1']
    person2 = request.POST['person2']
    address = request.POST['address']
    member = Membership.objects.get(id=member_id)
    person1 = get_object_or_404(Person, id=person1)
    person2 = get_object_or_404(Person, id=person2)
    address = get_object_or_404(Address, id=address)
    member.person1 = person1
    member.person2 = person2
    member.address = address
    member.level = request.POST['level']
    if request.POST['expiration']:
        member.expiration = request.POST['expiration']
    member.status = request.POST['status']
    member.notes = request.POST['notes']
    member.save()

    return HttpResponseRedirect(reverse('members_app:show_member', kwargs={'member_id':member_id})+'?message=changes_saved')

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
