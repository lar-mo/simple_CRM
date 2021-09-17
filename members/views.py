from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
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
    querystring = request.GET['q'].strip()
    # try:
    #     filter = request.GET['f']
    # except:
    #     pass

    search_terms = querystring.split()
    search_terms = list(dict.fromkeys(search_terms))
    try:
        search_terms.remove('and')
    except:
        pass
    print(search_terms)

    person_records = Person.objects.all()
    member_records = Membership.objects.all()
    board_records = Board.objects.all()

    # try:
    #     member_records = member_records.filter(board_member=True)
    # except:
    #     pass
    # print(search_terms[0])
    # print(search_terms[1])
    exact_match_p = person_records.filter(Q(first_name=search_terms[0], last_name=search_terms[1]))
    exact_match_mp1 = member_records.filter(Q(person1__first_name=search_terms[0], person1__last_name=search_terms[1]))
    exact_match_mp2 = member_records.filter(Q(person2__first_name=search_terms[0], person2__last_name=search_terms[1]))

    # (2)(n)ames
    # members_name1_2n = member_records.filter(reduce(Q.__or__, [Q(first_name__istartswith=word) for word in two_names])) # was icontains
    # members_name2_2n = member_records.filter(reduce(Q.__or__, [Q(last_name__istartswith=word) for word in two_names])) # was icontains
    # two_names_orig = querystring.split("and")
    # print(two_names_orig)
    # second_name_split = two_names_orig[1].strip().split(" ")
    # two_names = [x for x in second_name_split]
    # two_names.append(two_names_orig[0].strip())
    members_person1_2nfn = member_records.filter(person1__first_name=search_terms[0])
    members_person1_2nln = member_records.filter(person1__last_name=search_terms[1])
    # members_person2_2nfn = member_records.filter(person2__first_name=search_terms[2])
    # print(members_person1_2nfn.exists())
    # print(members_person1_2nln.exists())
    # print(members_person2_2nfn.exists())

    # (s)tarts (w)ith (s)earch (t)erms
    # members_name1_swst = member_records.filter(reduce(Q.__or__, [Q(first_name__istartswith=word) for word in search_terms])) # was icontains
    # members_name2_swst = member_records.filter(reduce(Q.__or__, [Q(last_name__istartswith=word) for word in search_terms])) # was icontains
    members_name1_swst = person_records.filter(first_name='')
    members_name2_swst = person_records.filter(first_name='')

    # (e)nds (w)ith (s)earch (t)erms
    # members_name1_ewst = member_records.filter(reduce(Q.__or__, [Q(first_name__iendswith=word) for word in search_terms])) # was icontains
    # members_name2_ewst = member_records.filter(reduce(Q.__or__, [Q(last_name__iendswith=word) for word in search_terms])) # was icontains
    members_name1_ewst = person_records.filter(first_name='')
    members_name2_ewst = person_records.filter(first_name='')

    # (c)ontains (s)earch (t)erms
    person_name1_cst = person_records.filter(reduce(Q.__or__, [Q(first_name__icontains=word) for word in search_terms]))
    person_name2_cst = person_records.filter(reduce(Q.__or__, [Q(last_name__icontains=word) for word in search_terms]))
    member_name1fn_cst = member_records.filter(reduce(Q.__or__, [Q(person1__first_name__icontains=word) for word in search_terms]))
    member_name1ln_cst = member_records.filter(reduce(Q.__or__, [Q(person1__last_name__icontains=word) for word in search_terms]))
    member_name2fn_cst = member_records.filter(reduce(Q.__or__, [Q(person2__first_name__icontains=word) for word in search_terms]))
    member_name2ln_cst = member_records.filter(reduce(Q.__or__, [Q(person2__last_name__icontains=word) for word in search_terms]))
    # # print(exact_match.exists())
    # # print(members_name1.exists())
    # # print(members_name2.exists())
    # print(member_name1_cst)
    # print(member_name2_cst)

    if exact_match_p.exists() or exact_match_mp1.exists() or exact_match_mp2.exists():
        members = list(dict.fromkeys(chain(exact_match_p, exact_match_mp1, exact_match_mp2)))
        print(members)
        context = {
            'members': members,
            'querystring': querystring,
            'view': 'search_results',
            'match': '1:exact',
        }
        return render(request, 'members/output.html', context)

    # second_name_split = two_names_orig[1].strip().split(" ")
    # two_names = [x for x in second_name_split]
    # two_names.append(two_names_orig[0].strip())
    # members_person1_2nfn = member_records.filter(person1__first_name=two_names[0])
    # members_person1_2nln = member_records.filter(person1__last_name=two_names[1])
    # members_person2_2nfn = member_records.filter(person2__first_name=two_names[2])

    # if members_person1_2nfn.exists() or members_person1_2nfn.exists() or members_person2_2nfn.exists():
    #     members = list(dict.fromkeys(chain(members_person1_2nfn, members_person1_2nfn, members_person2_2nfn)))
    #     context = {
    #         'members': members,
    #         'querystring': querystring,
    #         'view': 'search_results',
    #         'match': '2:pairs',
    #     }
    #     return render(request, 'members/output.html', context)

    if members_name1_swst.exists() or members_name2_swst.exists():
        members = list(dict.fromkeys(chain(members_name1_swst, members_name2_swst)))
        context = {
            'members': members,
            'querystring': querystring,
            'view': 'search_results',
            'match': '3:swst',
        }
        return render(request, 'members/output.html', context)

    if members_name1_ewst.exists() or members_name2_ewst.exists():
        members = list(dict.fromkeys(chain(members_name1_ewst, members_name2_ewst)))
        context = {
            'members': members,
            'querystring': querystring,
            'view': 'search_results',
            'match': '4:ewst',
        }
        return render(request, 'members/output.html', context)

    if member_name1fn_cst.exists() or member_name1ln_cst.exists() or member_name2fn_cst.exists() or member_name2ln_cst.exists() or person_name1_cst.exists() or person_name2_cst.exists():
        people = list(dict.fromkeys(chain(
                        member_name1fn_cst,
                        member_name1ln_cst,
                        member_name2fn_cst,
                        member_name2ln_cst,
                        person_name1_cst,
                        person_name2_cst
                        )
                ))
        context = {
            'members': people,
            'querystring': querystring,
            'view': 'search_results',
            'match': '5:words',
        }
        return render(request, 'members/output.html', context)
    else:
        members = []
        context = {
            'members': members,
            'querystring': querystring,
            'view': 'search_results',
            'match': '6:else',
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
    membership = Membership.objects.filter(person1__id=person_id, person2__id=person_id)
    form = AddressForm(instance=address)
    try:
        querystring = request.GET['from']
    except:
        querystring = ''
    context = {
        'person': person,
        'people': people,
        'address_id': address.id,
        'membership': membership,
        'form': form,
        'querystring': querystring,
        'view': 'edit_person',
    }
    return render(request, 'members/edit_person.html', context)

# @login_required
# def edit_address(request, address_id):
#     address = get_object_or_404(Address, id=address_id)
#     print(address)
#     form = AddressForm(instance=address)
#     print(form)
#     return render(request, 'members/edit_address.html', {'form': form})

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
    return render(request, 'members/show_member.html', context)

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
        'address_id': address.id,
        'form': form,
        'querystring': querystring,
        'view': 'edit_member',
    }
    return render(request, 'members/edit_member.html', context)

def save_member(request):
    member_id = request.POST['member_id']
    member_info = Member.objects.get(id=member_id)
    member_info.person1 = request.POST['person1']
    member_info.person2 = request.POST['person2']
    member_info.address = request.POST['address']
    member_info.level = request.POST['level']
    member_info.expiration = request.POST['expiration']
    member_info.status = request.POST['status']
    member_info.notes = request.POST['notes']
    member_info.save()

    return HttpResponseRedirect(reverse('members_app:show_member', kwargs={'member_id':member_id})+'?message=changes_saved')
