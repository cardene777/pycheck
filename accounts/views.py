from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from . import forms
from skill.models import SkillCheckData, Result
from django.shortcuts import render


class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     messages.add_message(self.request, messages.INFO, 'ログインできました。')
    #     return context


class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"


class SignUpView(CreateView):
    form_class = forms.SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")


def profile(request, username):
    result = "no"
    if Result.objects.filter(username=username).exists():
        result = Result.objects.filter(username=username).last()

    if not SkillCheckData.objects.filter(username=username).exists():
        params = {
            "username": username,
            "message": "No",
            "result": result
        }
        return render(request, "accounts/profile.html", params)
    user_datas = SkillCheckData.objects.filter(username=username)
    username = user_datas.values_list("username", flat=True)[0]
    socores = [int(user_score) for user_score in user_datas.values_list("score", flat=True)]
    average_current = sum(socores) // len(socores)

    params = {
        "user_datas": user_datas,
        "username": username,
        "average_current": average_current,
        "result": result
    }

    return render(request, "accounts/profile.html", params)


# def aggregation(requests):
#     if requests.method == "POST":
#
#
#         params = {
#             "user_datas": user_datas,
#             "username": username,
#         }
#
#         return render(requests, "accounts/profile.html", params)