from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.urls import path, include
from core.views import SignUpView
from .forms import LoginForm
from . import views

app_name = "core"

urlpatterns = [
    path('', views.ListaAvaliacoesView.as_view(), name='lista_avaliacoes'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path('login/', LoginView.as_view(
            template_name='login.html',
            authentication_form=LoginForm
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(
        next_page=reverse_lazy("core:lista_avaliacoes")),
        name='logout'
    ),
    path('fazer-avaliacao/', views.FazerAvaliacaoView.as_view(), name='fazer_avaliacao'),
]