from django.views.generic import ListView,UpdateView, CreateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from .models import Task
from .forms import TaskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/task_list.html'  # ensure this matches your template filename
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/add_task.html'  # Ensure this template exists
    success_url = reverse_lazy('index')  # Redirect to task list after add

    def form_valid(self, form):
        form.instance.user = self.request.user  # assign current user
        return super().form_valid(form)


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})


class CustomLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))


def custom_login_view(request):
    form = CustomLoginForm()

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password')

    return render(request, 'todo/custom_login.html', {'form': form})

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title']
    template_name = 'todo/task_form.html'  # Create this form template
    success_url = reverse_lazy('index')

class TaskCompleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = True  # mark complete
        task.save()
        return redirect('index')


class TaskIncompleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = False  # mark incomplete
        task.save()
        return redirect('index')

