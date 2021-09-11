from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from functools import reduce
from itertools import chain

import json

from .models import Address, Board, Committee, Membership, Person, NeedsReview

@login_required
def list_all(request):
    all_members = Person.objects.all()
    paginator = Paginator(all_members, 10)
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)
    context = {
        'members': members,
        'view': 'list_all_people',
    }
    return render(request, 'members/output.html', context)

class ListBoardView(LoginRequiredMixin, View):

    def get(self, request):
        executive_members = Board.objects.all()
        # committee_members = Committee.objects.all()

        # role = Committee.get_role(12)
        # print(role)
        # for x in role:
        #     print(x.role)

        roles = Committee.get_cmte_members()
        print("Cmte Roles: {}".format(roles))
        committee_members = []
        for role in roles:
            person = role.cmte_member
            committee_members.append(person)

        # print("Before dedupe: {}".format(committee_members))
        committee_members = list(dict.fromkeys(committee_members))
        # print("{}".format(executive_members))

        board_members = list(chain(executive_members, committee_members))
        # board_members = Q(executive_members) | Q(committee_members)
        # print(board_members)
        all_bm = []
        for m in board_members:
            try:
                em = m.cmte_member.board_member
                all_bm.append(em)
            except:
                pass
            try:
                cm = m.board_member
                all_bm.append(cm)
            except:
                pass
        # print(all_bm)
        all = list(dict.fromkeys(all_bm)) # remove duplicates
        print(all)

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
    # name1.split(' ')[-1]
    # REGEX \b(\w+)$
    active_members = Person.objects.filter(membership__status='Active')
    # members = Member.objects.filter(membership_status='active').order_by('name1')
    # members = Member.objects.filter(membership_status='active').extra(select={'lname1' : "SUBSTR(name1, -1 ,)"}).order_by('lname1')
    # print(members)
    paginator = Paginator(active_members, 10)
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)
    context = {
        'members': members,
        'view': 'list_active_members'
    }
    return render(request, 'members/output.html', context)

@login_required
def list_inactive(request):
    inactive_members = Person.objects.filter(membership__status='Inactive')
    paginator = Paginator(inactive_members, 10)
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)
    context = {
        'members': members,
    }
    return render(request, 'members/output.html', context)

@login_required
def needs_review(request):
    needs_review = Member.objects.filter(needs_review=1)
    paginator = Paginator(needs_review, 10)
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)
    context = {
        'members': members,
    }
    return render(request, 'members/output.html', context)

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

    member_records = Member.objects.all()
    try:
        member_records = member_records.filter(board_member=True)
    except:
        pass
    exact_match = member_records.filter(name1=querystring)
    members_name1_2n = member_records.filter(reduce(Q.__or__, [Q(name1__istartswith=word) for word in two_names])) # was icontains
    members_name2_2n = member_records.filter(reduce(Q.__or__, [Q(name2__istartswith=word) for word in two_names])) # was icontains
    members_name1_swst = member_records.filter(reduce(Q.__or__, [Q(name1__istartswith=word) for word in search_terms])) # was icontains
    members_name2_swst = member_records.filter(reduce(Q.__or__, [Q(name2__istartswith=word) for word in search_terms])) # was icontains
    members_name1_ewst = member_records.filter(reduce(Q.__or__, [Q(name1__iendswith=word) for word in search_terms])) # was icontains
    members_name2_ewst = member_records.filter(reduce(Q.__or__, [Q(name2__iendswith=word) for word in search_terms])) # was icontains
    members_name1_cst = member_records.filter(reduce(Q.__or__, [Q(name1__icontains=word) for word in search_terms]))
    members_name2_cst = member_records.filter(reduce(Q.__or__, [Q(name2__icontains=word) for word in search_terms]))
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
    else:
        members = list(dict.fromkeys(chain(members_name1_cst, members_name2_cst)))
        context = {
            'members': members,
            'querystring': querystring,
            'view': 'search_page',
            'match': '3:words',
        }
        return render(request, 'members/output.html', context)

@login_required
def show_member_info(request, member_id):
    message = request.GET.get('message', '')
    member = Person.objects.filter(id=member_id)
    # print(member)
    context = {
        'members': member,
        'message': message,
        'view': 'show_member_info_page',
    }
    return render(request, 'members/output.html', context)

@login_required
def edit_member_info(request, member_id):
    member = Member.objects.get(id=member_id)
    context = {
        'member': member,
    }
    return render(request, 'members/edit_member_info.html', context)

def save_member_info(request):
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

    return HttpResponseRedirect(reverse('members_app:show_member_info', kwargs={'member_id':member_id})+'?message=changes_saved')
