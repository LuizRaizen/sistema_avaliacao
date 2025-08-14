from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import AvaliacaoForm, CustomUserCreationForm
from .models import Avaliacao

class ViewProtegida(LoginRequiredMixin):
    login_url = reverse_lazy("core:login")
    redirect_field_name = "next"


class ListaAvaliacoesView(ListView):
    model = Avaliacao
    template_name = "lista-avaliacoes.html"
    context_object_name = "avaliacoes"
    paginate_by = 10
    ordering = "-criado_em"


class FazerAvaliacaoView(ViewProtegida, CreateView):

    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = "fazer-avaliacao.html"
    success_url = reverse_lazy("core:lista_avaliacoes")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("core:lista_avaliacoes")  # ajuste se quiser

    # loga o usuário após cadastrar
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
