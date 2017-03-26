from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
	def validation(self, name, username, password, confirm_password):
		email_regex = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
		messages = []
		valid = True
		if len(name) < 3:
			valid = False
			messages.append('Name should be at least 3 characters!')
		if len(username) < 3:
			valid = False
			messages.append('Username should be at least 3 characters!')
		if password == '' or len(password) < 3:
			valid = False
			messages.append('Password must be longer than 5 characters')
		if password != confirm_password:
			valid = False
			messages.append("Passwords don't match")
		if len(User.userManager.filter(username=username)) != 0:
			valid = False
			messages.append("Email already exists")
		if valid:
			return (True, 'valid')
		else:
			return (False, messages)


class User(models.Model):
	name = models.CharField(max_length=30)
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=255)
	userManager = UserManager()

class Wish(models.Model):
	item = models.CharField(max_length=45)
	users = models.ManyToManyField(User, related_name="wishes")
	created_by = models.ForeignKey(User, related_name="created")
	created_at = models.DateTimeField(auto_now_add=True)
