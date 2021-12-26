from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

class Home(ListView):
    model = Post
    template_name = 'blog/home.html'
    paginate_by = 3
    ordering = ['-date_posted']  


class UserPosts(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    paginate_by = 5 
    

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class Detail(DetailView):
    model = Post
    template_name = 'blog/detail.html'


class Create(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    template_name = 'blog/create.html'
    success_url = '/' 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  

    

class Update(LoginRequiredMixin, UserPassesTestMixin, UpdateView,):
    model = Post
    fields = ['title','content']
    template_name = 'blog/update.html' 
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False       


class Delete(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 
        
def signup(request):
    if request.method == 'POST':
       form = UserRegisterForm(request.POST)
       if form.is_valid():
           form.save()
           username = form.cleaned_data.get('username')
           messages.success(request, f'Your account has been created! You are now able to login')
           return redirect('login')
    else:
       form = UserRegisterForm()
    return render(request, 'blog/signup.html', {'form':form})   
    
@login_required
def profile(request):
    if request.method == 'POST':
      u_form = UserUpdateForm(request.POST,instance=request.user)
      p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)

      if u_form.is_valid() and p_form.is_valid():
          u_form.save()
          p_form.save()
          messages.success(request, f'Your account has been updated!')
          return redirect('profile')
    else: 
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile) 
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile.html', context)