from django.shortcuts import redirect, reverse


def redirect_view(request):
    response = redirect(reverse("home"))
    return response
