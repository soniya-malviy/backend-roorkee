from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render


class AnalyticsLoginView(LoginView):
    template_name = "analytics/login.html"
    redirect_authenticated_user = (
        True  # If already logged in, redirect them to the dashboard
    )


@login_required(login_url="/analytics/login/")
@user_passes_test(lambda u: u.is_superuser)
def analytics_dashboard(request):
    return render(request, "analytics/dashboard.html")
