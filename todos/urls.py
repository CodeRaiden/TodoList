from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, SigninPage
# As said we do not need to implemet a Logoutview class. so what we can simply do here is import the LogoutView here, and then incllude the path in the urlpatterns
from django.contrib.auth.views import LogoutView
# to import a list view


urlpatterns = [
 path('login/', CustomLoginView.as_view(), name='login'),
 # here for the logoutview we will set the page we want the user to be sent to when the logout is clicked by making use of the parameter " next_page="" " and we will set it's value to the "login.html" in order to send the user to the login page after the user has successfully logged out.
 path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
 path('signup/', SigninPage.as_view(), name='signup'),
 
 path('', TaskList.as_view(), name='tasks'),
 # note the detailView looks for an object as the detail by it's index in the table 
 # here the view will take a primary key in the path which will be the object index
 path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
 path('task-create/', TaskCreate.as_view(), name='task-create'),
 path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
 path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
 ]