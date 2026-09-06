from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import logging

from .models import CarModel
from .restapis import (
    get_request,
    post_review,
    analyze_review_sentiments,
)


logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]

    user = authenticate(username=username, password=password)
    data = {"userName": username}

    if user is not None:
        login(request, user)
        data = {
            "userName": username,
            "status": "Authenticated",
        }

    return JsonResponse(data)


def logout_request(request):
    logout(request)

    data = {
        "userName": "",
    }

    return JsonResponse(data)


@csrf_exempt
def registration(request):
    data = json.loads(request.body)

    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]

    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except Exception:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )

        login(request, user)

        data = {
            "userName": username,
            "status": "Authenticated",
        }

        return JsonResponse(data)

    data = {
        "userName": username,
        "error": "Already Registered",
    }

    return JsonResponse(data)


def get_dealerships(request, state="All"):
    if request.method == "GET":
        if state == "All":
            dealerships = get_request("/fetchDealers")
        else:
            dealerships = get_request("/fetchDealers/" + state)

        return JsonResponse({
            "status": 200,
            "dealers": dealerships,
        })


def get_dealer_reviews(request, dealer_id):
    if request.method == "GET":
        reviews = get_request(
            "/fetchReviews/dealer/" + str(dealer_id)
        )

        return JsonResponse({
            "status": 200,
            "reviews": reviews,
        })


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        dealer = get_request(
            "/fetchDealer/" + str(dealer_id)
        )

        return JsonResponse({
            "status": 200,
            "dealer": dealer,
        })


def get_cars(request):
    if request.method == "GET":
        car_models = CarModel.objects.select_related(
            "car_make"
        ).all()

        cars = []

        for car in car_models:
            cars.append({
                "CarMake": car.car_make.name,
                "CarModel": car.name,
            })

        return JsonResponse({
            "status": 200,
            "CarModels": cars,
        })


@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)

        sentiment_response = analyze_review_sentiments(
            data["review"]
        )

        if (
            sentiment_response
            and "sentiment" in sentiment_response
        ):
            data["sentiment"] = sentiment_response["sentiment"]
        else:
            data["sentiment"] = "neutral"

        response = post_review(data)

        if response is not None:
            return JsonResponse({
                "status": 200,
                "review": response,
            })

        return JsonResponse({
            "status": 500,
            "error": "Unable to add review",
        })
