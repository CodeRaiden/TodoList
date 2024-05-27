from django.shortcuts import render, redirect
# To make use of ListView
from django.views.generic.list import ListView
# To make use of detailView
from django.views.generic.detail import DetailView
# To make use of the createview, updateview, deleteview and the formview
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# To make sure that when the createview form is submitted we are able to redirect the user successfully to a different page, for this we also need to import the "reverse_laszy" from django.urls. after importing this we need to get back to the createview and set the value for the "success_url" which will be where the reverse_lazy will be used
from django.urls import reverse_lazy

# To make use of the inbuild django auth table loginview
from django.contrib.auth.views import LoginView
# To prevent a user from accessing a page such as the tasklist without loggingin, this is where the LoginRequiredMixin comes in
from django.contrib.auth.mixins import LoginRequiredMixin
# Importing the UserCreatedForm for the signup page to create a user for us when the form is submitted
from django.contrib.auth.forms import UserCreationForm
# and along with the user being registered(signin), we also want the user to be logged in. for this we will need the 'Login' method
from django.contrib.auth import login

from.models import Task

# Create your views here.

# THE LOGIN VIEW will be at the top here since it's kind of like the gate keeper
# typically we would want to place the code for this view inside a different app,
# but for this example we will leave it here for now
class CustomLoginView(LoginView):
 template_name = 'todos/login.html'
 fields = '__all__'
 # here we want to redirect an authenticated user
 redirect_authenticated_user = True

 # here we will override the parent class success url to send the user to the tasks page when he has successfully loggedin
 def get_success_url(self):
  return reverse_lazy('tasks')
# For the logoutview we do not need to provide the implementation, all we need to do is navigate to the urls and provide the path


# The signin page
class SigninPage(FormView):
 template_name = 'todos/signup.html'
 # we will set the form class to be used, we will set this to the imported django form class
 form_class = UserCreationForm
 # here we also want to redirect an authenticated user
 # redirect_authenticated_user = True
 # we want the page redirected to the tasks page on success
 # success_url = reverse_lazy('tasks')
 # since the allow redirection of authenticated user code above does't work then we will need to manually write a redirection function code where we will need to import the redirect function. we will do this later shortly.
 

 # for now, to login the user as soon as the the user registers i.e as soon as the form is posted, we will override the form valid
 def form_valid(self, form):
  # so what we want to do here is that once the form is valid we want the user to be loggedin. so then we will save the form and this action will also return the saved user, and we will store this in a variable "user"
  user = form.save()
  # now with the above we can state that if the user is not none ie. if the user is created then we want the imported django login function to be used
  if user is not None:
   # the imported django login function will take in two parmeters; the instance's/object's request and the user information returned in the variable 'user'
   login(self.request, user)
   return super(SigninPage, self).form_valid(form)
  
 # for the manual redirect code
 # after importing the redirect function, we will need to get the instance/object and all it's arguments and keyword arguments
 def get(self, *args, **kwargs):
  if self.request.user.is_authenticated:
   return redirect('tasks')
  # else we return the object/instance args and kwargs
  return super(SigninPage, self).get(*args, **kwargs)



# to make use of the ListView we will use a class instead of a function here
# the class TaskList will inherit from the LIstView
# note as for the temlate to be used, this will search the templates for the template with the prefix task followed by "_" and then "list" i.e "task_list"
# to prevent a user from accessing the tasklist without first loggingin we will use the logginRequiredMixin inside the inheritance parenthesis and it must be the first parameter.
# note that we will need to override the default django redirection for the loginRequiredMixin. To do this we will have to navigate to our projects "settings" file and then just below the "USE_TZ = True" line code we will place the code to override the code " LOGIN_URL = 'login' " to direct the user to the login page.
# so we can add the LoginRequiredMixin where ever we want to restrict access to an unregistered user
class TaskList(LoginRequiredMixin, ListView):
 # the object/instance whos information we would like to use
 model = Task
 # the instance/object context name. By default this would be set to 'object_list'
 context_object_name = 'tasks'
 

 # in order to make sure that the logged in user can only view, have access and interract with his own data in the database, we will need to override the classes default "get_context_data()", which is what is responsible for returning all the context data that we pass to the view. So we will need to override the context_data() to return only context data belonging to the current user
 def get_context_data(self, **kwargs: reverse_lazy):
  # first here we will get all the context of the Listview class
  # note that the keyword args is for the context data type e.g {nam}
  context = super().get_context_data(**kwargs)
  # here we can add a new context, for example we can create a new context with key "color" and assign it a string value "red" and then we can check this out by adding the variable to our template
  # context['color'] = 'red'
  # but for this, we will select the already existing context 'task' and then we will filter all the tasklist of the object/instance to get all the task belonging to the current user 
  context['tasks'] = context['tasks'].filter(user = self.request.user)
  # we can also return the count of all incomplete items/tasks by filtering the users task for tasks where 'complete' value is equal to False and store this a new context variable key 'count'
  context['count'] = context['tasks'].filter(complete = False).count()
  # and then we will return the context containing only the taskslist of the current user to the view

  # To write the function logic for the GET method "search form", we will need to get the from input from the sent request or empty string if nothing is passed in and store it in a variable as seen below
  search_input = self.request.GET.get('search-area') or ''
  # now if the search_input is not null, then we want to filter the task context list for item where the item's title contains the search_input i.e "title__icontains = search_input" and return it in the tasks context instead.
  # note that if we want to return to the user items where the title starts with the searh_input we will use "title__startswith = search_input"
  if search_input:
   context['tasks'] = context['tasks'].filter(title__icontains = search_input)
  # here also we want to also return the search_input in the 'context kwargs' in the variable search_input when the context is returned to the frontend. we will use this to set the value of the search input
  context['search_input'] = search_input
  return context

# note as for the temlate to be used, the DetailView will search the templates for the template with the prefix with the Model name "Task" followed by "_" and then "detail" i.e "task_detail"
# this is useful for getting nformation on a specific item
class TaskDetail(LoginRequiredMixin, DetailView):
 model = Task
 context_object_name = 'task'
 # if we want to change the template name to be searched for by the DetailView, we will set the customized template name as seen below where we set the templatefolder/the_custom_name.html
 # template_name = 'todos/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
 model = Task
 # here we can list out the particular fields we want in the form by settng the fields attribute as seen below
 # fields = ['title', 'description']
 # but for this we will list out all the fields of the class instance using the code below
 # fields = '__all__'
 # now that the create form is exclusive to the current user,  we do not want the capability of switching between users when we want to create tasks, so for this instead of the above "__all__", we will set the fields as below
 fields = ['title', 'description', 'complete']
 success_url = reverse_lazy('tasks')
 # FORM_VALID
 # Also in order to make sure that the current user can create items that are only accessible by him, for this we will need to
 # navigate to the createoview and there we verride the default object/instance form_valid function. we will override this so that 
 # when this method is triggered by default in the post request we are going to make the form create item that are only accessible by
 # the current item.
 def form_valid(self, form):
  # here we will set the form object/instance user field to be the current user "self.request.user"
  form.instance.user = self.request.user
  # and now we will return this as the default TaskCreate class form to be triggered for the instance/object by the post request
  return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
 model = Task
 fields = ['title', 'description', 'complete']
 success_url = reverse_lazy('tasks')

# note that the delete will look out for a template with "_" followed by "confirm_delete.html" i.e "task_confirm_delete.html"
class TaskDelete(LoginRequiredMixin, DeleteView):
 model = Task
 # the context object name is also going to be object here, so we will have to change that into 'task'
 context_object_name = 'task'
 success_url = reverse_lazy('tasks')