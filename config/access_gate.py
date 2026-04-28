from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


def access_gate(request):
    if not settings.SITE_GATE_IS_ACTIVE:
        return redirect("landing")

    next_url = request.GET.get("next") or request.POST.get("next") or "/"

    if request.method == "POST":
        submitted_password = request.POST.get("password", "")

        if submitted_password == settings.SITE_GATE_PASSWORD:
            request.session[settings.SITE_GATE_SESSION_KEY] = True
            return redirect(next_url)

        messages.error(request, "Incorrect password.")

    return render(request, "access_gate.html", {"next_url": next_url})


def clear_access_gate(request):
    request.session.pop(settings.SITE_GATE_SESSION_KEY, None)
    return redirect("access_gate")


class SiteAccessGateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.SITE_GATE_IS_ACTIVE:
            return self.get_response(request)

        request_path = request.path_info
        allowed_prefixes = settings.SITE_GATE_PUBLIC_PATH_PREFIXES
        access_gate_path = reverse("access_gate")

        if request_path == access_gate_path or request_path.startswith(allowed_prefixes):
            return self.get_response(request)

        if request.session.get(settings.SITE_GATE_SESSION_KEY):
            return self.get_response(request)

        query = urlencode({"next": request.get_full_path()})
        return HttpResponseRedirect(f"{access_gate_path}?{query}")
