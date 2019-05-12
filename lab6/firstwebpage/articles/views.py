from django.shortcuts import render, redirect
from .models import Article
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def registration(request):
    if request.method == 'POST':
        form = {
            'login': request.POST['login'],
            'email': request.POST['email'],
            'password': request.POST['password'],
        }
        validation_login = User.objects.filter(username=form['login'])
        validation_email = User.objects.filter(email=form['email'])
        if validation_login or validation_email:
            form['errors'] = 'Your Login or E-Mail already exists. Try another one.'
            return render(request, 'registration.html', {'form': form})
        if form['login'] and form['email'] and form['email']:
            User.objects.create_user(form['login'], form['email'], form['password'])
            return redirect('auth')
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'registration.html')
    else:
        return render(request, 'registration.html')


def auth(request):
    if request.method == 'POST':
        form = {
            'login': request.POST['login'],
            'password': request.POST['password'],
        }
        validation_login = User.objects.filter(username=form['login'])
        if validation_login and form['login'] and form['password']:
            user = authenticate(username=form['login'], password=form['password'])
            if user:
                login(request, user)
                return redirect('articles')
            else:
                form['errors'] = u'Login or Password was incorrect. Try again'
                return render(request, 'login.html', {'form': form})
        else:
            form['errors'] = u'This user isnt registered yet or you not entered all required fields.'
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html')

def deauth(request):
    logout(request)
    message='You successfully Logged out.'
    return render(request, 'archive.html', {"message": message})


def archive(request):
	return render(request, 'archive.html', {"posts":Article.objects.all()})


def get_article(request, article_id):
	try:
		post = Article.objects.get(id=article_id)
		return render(request, 'article.html', {"post": post})
	except Article.DoesNotExist:
		raise Http404

def create_post(request):
	if request.user != 'AnonymousUser':
		if request.method == "POST":    
			# обработать данные формы, если метод POST 
			form = {
				'text': request.POST["text"], 
				'title': request.POST["title"]
			}
			# в словаре form будет храниться информация, введенная пользователем 
			validation = Article.objects.filter(title=form['title'])
			if validation:
				form['errors'] = u'Такая статья уже существует. Попробуйте снова.'
				return render(request, 'create_post.html', {'form': form})
			#проверка на уникальность заголовка
			if form["text"] and form["title"]:
				# если поля заполнены без ошибок
				Article.objects.create(text=form["text"], title=form["title"], author=request.user) 
				return redirect('articles')
				# перейти на страницу поста
			else:
				#если введеные данные некорректны
				form['errors'] = u"Не все поля заполнены"
				return render(request, 'create_post.html', {'form': form})
		else:
			# просто вернуть страницу с формой, если метод GET
			return render(request, 'create_post.html', {})
	else:        
		raise Http404

