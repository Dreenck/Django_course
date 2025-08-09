from django.shortcuts import render
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

# from django.template.loader import render_to_string (Too common, so we already have faster solution for it, django.shortcuts import render)

# Create your views here.

monthly_challenges = {
    "january": "Do 200 squats every day!",
    "february": "Do 100 pushups every day!",
    "march": "Stop your sugar intake every day!",
    "april": "Meditate for 10-15 minutes!",
    "may": "Get eight hours of sleep each night!",
    "june": "Read a book for 30 minutes!",
    "july": "Try a no spend month!",
    "august": "Quit a bad habit that bothers you!",
    "september": "Create a morning routine!",
    "october": "Give up caffeine!",
    "november": "Give meaningful compliments!",
    "december": None
}


def index(request):
    months = list(monthly_challenges.keys())

    return render(request, "challenges/index.html", {
        "months": months
    })


def monthly_challenge_by_number(request, month):
    months = list(monthly_challenges.keys())

    if month > len(months):
        return HttpResponseNotFound("<h1>Invalid month!</h1>")

    forward_month = months[month - 1]
    forward_url = reverse("month-challenge", args=[forward_month])
    return HttpResponseRedirect(forward_url)


def monthly_challenge(request, month):
    try:
        challenges_text = monthly_challenges[month]
        return render(request, "challenges/challenge.html", {
            "challenge_text": challenges_text,
            "month": month
        })
    except:
        raise Http404()
