import json
from datetime import date
from decimal import *
from functools import cmp_to_key

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Wallet, Card
from django.http import JsonResponse, HttpResponse


# Create your views here.
@login_required
@require_http_methods(["GET"])
def get_wallet_info(request):
    try:
        wallet = Wallet.objects.get(owner=request.user)
        response_data = {
            'owner': wallet.owner.username,
            'max_limit': str(wallet.get_max_limit()),
            'user_limit': str(wallet.userLimit) if wallet.userLimit else '',
            'balance': str(wallet.get_balance()),
            'available_credit': str(wallet.get_available_credit())
        }
    except Exception as err:
        raise err
    else:
        return JsonResponse(response_data, status=200)


@login_required
@require_http_methods(["GET"])
def get_cards(request):
    try:
        wallet = Wallet.objects.get(owner=request.user)
        cards = sorted(wallet.get_cards(), key=cmp_to_key(Card.compare))
        response_data = dict()
        for card in cards:
            response_data[card.number] = {
                'dueDate': card.dueDate.strftime('%d'),
                'validThru': card.validThru.strftime('%m/%y'),
                'name': card.name,
                'secureCode': card.secureCode,
                'creditLimit': str(card.creditLimit),
                'balance': str(card.balance),
                'available_credit': str(card.get_available_credit())
            }
    except Exception as err:
        raise err
    else:
        return JsonResponse(response_data, status=200)


@login_required
@require_http_methods(["POST"])
def add_card(request):
    try:
        wallet = Wallet.objects.get(owner=request.user)
        wallet.add_card(
            number=request.POST.get('number'),
            duedate=date(1900, 1, int(request.POST.get('duedateday'))),
            validthru=date(int(request.POST.get('validthruyear')), int(request.POST.get('validthrumonth')), 1),
            name=request.POST.get('name'),
            securecode=request.POST.get('securecode'),
            creditlimit=Decimal(request.POST.get('creditlimit')),
            balance=Decimal(request.POST.get('balance'))
        )
    except Exception as err:
        raise err
    else:
        return HttpResponse(status=200)


@login_required
@require_http_methods(["POST"])
def rm_card(request):
    try:
        wallet = Wallet.objects.get(owner=request.user)
        wallet.rm_card(Card.objects.get(number=request.POST.get('number')))
    except Exception as err:
        raise err
    else:
        return HttpResponse(status=200)


@login_required
@require_http_methods(["POST"])
def add_purchase(request):
    try:
        wallet = Wallet.objects.get(owner=request.user)
        wallet.add_purchase(Decimal(request.POST.get('value')))
    except Exception as err:
        raise err
    else:
        return HttpResponse(status=200)


@login_required
@require_http_methods(["POST"])
def set_limit(request):
    try:
        wallet = Wallet.objects.get(owner=request.user)
        wallet.set_user_limit(Decimal(request.POST.get('userlimit')) if request.POST.get('userlimit') else None)
    except Exception as err:
        raise err
    else:
        return HttpResponse(status=200)


@login_required
@require_http_methods(["POST"])
def release_credit(request):
    try:
        card = Card.objects.get(number=request.POST.get('cardnumber'))
        card.release_credit(Decimal(request.POST.get('value')))
    except Exception as err:
        raise err
    else:
        return HttpResponse(status=200)
