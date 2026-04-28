import json
import logging

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import redirect, render
from django.middleware.csrf import get_token

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def get_csrf_token(request):
        """Endpoint to get a CSRF token for embed iframes."""
        return JsonResponse({"csrfToken": get_token(request)})


@require_POST
def signup_embed(request):
        """
            Handles signup from the embedded iframe form.
                CSRF is enforced (no @csrf_exempt).
                    """
        try:
                    data = json.loads(request.body)
except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()

    if not email or not password:
                return JsonResponse({"error": "Email and password are required."}, status=400)

    if len(password) < 8:
                return JsonResponse({"error": "Password must be at least 8 characters."}, status=400)

    if User.objects.filter(username=email).exists():
                return JsonResponse({"error": "An account with this email already exists."}, status=409)

    try:
                user = User.objects.create_user(
                                username=email,
                                email=email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name,
                )
except Exception as exc:
            logger.exception("Failed to create user: %s", exc)
            return JsonResponse({"error": "Account creation failed. Please try again."}, status=500)

    # Log the user in immediately after signup
        user = authenticate(request, username=email, password=password)
    if user is not None:
                login(request, user)

    return JsonResponse({"success": True, "message": "Account created successfully."})


def logout_view(request):
        from django.contrib.auth import logout
        logout(request)
        return redirect("landing")
