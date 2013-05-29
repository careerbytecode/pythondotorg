# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import UserCreationForm
from .models import User


#TODO: dont show the form if the user is already auth'd.
class SignupView(CreateView):
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        return '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return render(request, 'users/already_a_user.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)
