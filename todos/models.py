from django.db import models
# including the builtin django user model similar to the Identity user in .net
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
 # we will set a many to one relationship where in this case one user can have many items
 # we will do this using the "ForeignKey" which we will set to be the "User" model and with the on_delete parameter we will set this to "CASCADE" which means that the items will also be deleted when the user is deleted. we will also make the field nullable, and we will also make it possible for a blank form to be submitted when submitting a form.
 user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
 title = models.CharField(max_length=200, null=True, blank=True)
 description = models.TextField(null=True, blank=True)
 complete = models.BooleanField(default=False)
 # for the created field we will use the "models.DateTimeField" and make sure that this field is automatically incremented when the entry is created instead of being typed-in by the user
 created = models.DateTimeField(auto_now_add=True)

 def __str__(self):
  return self.title
 
 # we can also set the default ordering by settng the metedata
 class Meta:
 # here we will set the ordering of a queryset to begin with the "complete" field, i.e have the gotten completed "complete" field at the bottom of the set since it has been completed we won't be needing it anymore
  ordering = ['complete']