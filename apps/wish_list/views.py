from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import User, Wish

# Create your views here.
def index(request):
	return render(request, 'wish_list/index.html')

def register(request):
	if request.method == 'POST':
		name = request.POST['name']
		username = request.POST['username']
		password = request.POST['password'].encode('utf-8')
		confirm_password = request.POST['confirm_password'].encode('utf-8')

		validation = User.userManager.validation(name, username, password, confirm_password)
		if validation[0]:
			pwhash = bcrypt.hashpw(password, bcrypt.gensalt())
			user = User.userManager.create(name=name, username=username, password=pwhash)
			messages.info(request, 'Susscessfully registered! Please login')
			return redirect('/')
		else:
			for msg in validation[1]:
				messages.warning(request, msg)

			return redirect('/')
	else:
		return redirect('/')

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password'].encode('utf-8')

		user = User.userManager.filter(username=username)
		if len(user) == 1:
			user = user[0]
			hashed = user.password.encode('utf-8')

			if bcrypt.hashpw(password, hashed) == hashed:
				request.session['userid'] = user.id
				request.session['user'] = user.name
				return redirect('/dashboard')
			else:
				messages.warning(request, 'Unknown email/password combination')
				return redirect('/')
		else:
			messages.warning(request, 'Unknown email/password combination')
			return redirect('/')

def dashboard(request):
	user = User.userManager.get(id=request.session['userid'])
	wishes = Wish.objects.filter(users=user).order_by('created_at')
	other_wishes = Wish.objects.exclude(users=user).order_by('created_at')
	context = {
		'wishes': wishes,
		'others': other_wishes
	}
	return render(request, 'wish_list/dashboard.html', context)

def create(request):
	if request.method == 'POST':
		item = request.POST['item']
		if len(item) < 3:
			messages.warning(request, 'Item name should be at least 3 characters!')
			return redirect('/')

		user = User.userManager.get(id=request.session['userid'])
		# if Wish.objects.filter(item=item):
		# 	messages.warning(request, 'Item already exists')
		item = Wish.objects.create(item=item, created_by=user)
		result = item.users.add(user)

		return redirect('/dashboard')
	else:
		return render(request, 'wish_list/create.html')

def display_item(request, id):
	wish = Wish.objects.get(id=id)
	users = User.userManager.filter(wishes__id=id)
	context = {
		'wish': wish,
		'users': users
	}

	return render(request, 'wish_list/wish_item.html', context)

def add(request, id):
	user = User.userManager.get(id=request.session['userid'])
	wish = Wish.objects.get(id=id)
	wish.users.add(user)
	return redirect('/dashboard')

def remove(request, id):
	user = User.userManager.get(id=request.session['userid'])
	wish = Wish.objects.get(id=id)
	wish.users.remove(user)
	return redirect('/dashboard')

def delete(request, id):
	Wish.objects.get(id=id).delete()
	return redirect('/dashboard')

def logout(request):
	request.session['user'] = ''
	request.session['userid'] = ''

	return redirect('/')
