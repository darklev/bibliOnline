# -*- coding: utf-8 -*-#

# Create your views here.
from biblio.models import Book, Author, Subject, Comment, MemberUser, Demander
from django.shortcuts import render_to_response, render

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser

from biblio.form import *

from tutoriel.shortcuts import render


from django.contrib.auth.decorators import permission_required



import datetime



"""

class AddAuthorForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField()
"""



def show_main(request):
    con = {}
    con.update(csrf(request))
    return render(
		request,
        "biblio/main.html",
        con)

def show_authors(request):
	return render(
		request,
		"biblio/authors.html",
		{"authors" : Author.objects.order_by("lastname")})

def show_books(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    if user is not None:
        own = user.books
        pass
    else:
        own = ""

    return render(
		request,
		"biblio/books.html",
		{"books" : Book.objects.order_by("title"),
        "user" : user,
        "own" : own} )

def show_author(request, idAuthor):
	return render(
		request,
		"biblio/author.html",
		{"author" : Author.objects.get(pk=idAuthor)})

def show_book(request, idBook):
	return render(
		request,
		"biblio/book.html",
		{"book" : Book.objects.get(pk=idBook)})


def show_subjects(request):
	return render(
		request,
		"biblio/subjects.html",
		{ "subjects" : Subject.objects.order_by("label")} )


def delete_author(request, idAuthor):
	Author.objects.get(pk=idAuthor).delete()
	return HttpResponseRedirect("/authors/")

"""
def show_addAuthorForm(request):
	form = AddAuthorForm()
	con = {"addAuthor" : form}
	con.update(csrf(request))

	if request.method == 'POST':
			form = AddAuthorForm(request.POST)
			if form.is_valid():
				a = Author(firstname=form["firstname"].value(),lastname=form["lastname"].value())
				a.save()
			return HttpResponseRedirect(
				"authors/")


	return render_to_response(
			"biblio/addAuthor.html" , con , context_instance=RequestContext(request))
"""

@permission_required("biblio.can_edit_database")
def show_addAuthorForm(request):
    form = AuthorForm()
    con={'form':form}
    con.update(csrf(request))
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        con = {"form" : form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
				"authors/")
        else:
            return render_to_response("biblio/addAuthor.html", con, context_instance=RequestContext(request))
    return render_to_response("biblio/addAuthor.html", con, context_instance=RequestContext(request))

@permission_required("biblio.can_edit_database")
def show_addBookForm(request):
    form = BookForm()
    con={'form':form}
    con.update(csrf(request))
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        con = {"form" : form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
				"books/")
        else:
            return render_to_response("biblio/addBook.html", con, context_instance=RequestContext(request))
    return render_to_response("biblio/addBook.html", con, context_instance=RequestContext(request))

@permission_required("biblio.can_edit_database")
def show_addSubjectForm(request):
    form = SubjectForm()
    con={'form':form}
    con.update(csrf(request))
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        con = {"form" : form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
				"subjects/")
        else:
            return render_to_response("biblio/addSubject.html", con, context_instance=RequestContext(request))
    return render_to_response("biblio/addSubject.html", con, context_instance=RequestContext(request))



def login_page(request):
	con = {}
	con.update(csrf(request))
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = authenticate(username=username,password=password)
			if user is None:
				con["message"] = "Echec de l'authentification."
			elif not user.is_active:
				con["message"] = "Le compte n'est plus actif."
			else:
				login(request, user)
				url = request.GET.get("next","/")
				return HttpResponseRedirect(url)
		else:
			con["message"] = "Paramètres non valides."

	else:
		form = LoginForm()
	con["form"] = form
	return render(request, "biblio/authentification.html", con)

def logout_action(request):
	if request.user.is_authenticated():
		logout(request)
	return HttpResponseRedirect("/authentification")



#@permission_required("biblio.can_borrow")
def askfor_action(request, to, book):
    """
    Action qui permet à un utilisateur authentifié de faire une
    demande d'emprunt à un autre utilisateur.
    """
    book = Book.objects.get(pk=book)
    cible = MemberUser.objects.get(username=to)
    demandeur = request.user
    message = ""
    
    if(demandeur == cible):
        message = "You can't borrow your own book!"

    elif(book not in cible.books.all()):
        message = cible.username + " doesn't own this book."
    elif len(Demander.objects.filter(book=book, demandeur=demandeur, to=cible)) > 0:
        message = "You've already asked this book to this user!"	
    else:
        message = "You asked " + cible.username + " if you can borrow his book, " + book.title + "."
        d = Demander.objects.create(demandeur=request.user, to=MemberUser.objects.get(username=to), book=book, statut = "d")

    return render(
		request,
		"biblio/ask.html",
		{"message" : message})

def show_users(request):
    """
    Montrer les users.
    """
    return render(
		request,
		"biblio/users.html",
		{"users" : MemberUser.objects.all()})


def i_own_these_books(request):
    """
    Action qui met à jour les livres posséder par un MemberUser
    """
    user = request.user
    books = Book.objects.all()
    form = request.POST
    if request.method == "POST":
        for book in books:
            pk = str(book.pk)
            if(form.get(pk,False)):
                user.books.add(book)
            else:
                user.books.remove(book)
    return HttpResponseRedirect("books/")


def show_mybooks(request):
    """
    Montre les books de l'utilisateur
    """
    return render(
		request,
		"biblio/mybooks.html",
		{"books" : request.user.books.all()})


def who_own_this_book(request, book):
    """
    Montre les MembersUser qui pssédent le book dont le pk
    est passé en paramètre
    """
    return render(
		request,
		"biblio/heowns.html",
		{"book" : Book.objects.get(pk=book)})

def my_requests(request):
    """
    Montre les livres que l'utilisateur a demandé.
    """
    demandes = Demander.objects.filter(demandeur=request.user)
    pourmoi = Demander.objects.filter(to=request.user)
    return render(
		request,
		"biblio/my_requests.html",
		{"demandes" : demandes,
		 "pourmoi" : pourmoi})

def comment(request, idbook):
	"""
	Action qui permet d'ajouter un commentaire à un livre
	"""
	user = request.user
	book = Book.objects.get(pk=idbook)

	now = datetime.datetime.now()

	form = request.POST
	if request.method == "POST":
		content = request.POST.get("content","")
		if(content != ""):
			c = Comment.objects.create(user = user, book = book, date = now,comment = content)
			c.save()
			book.comments.add(c)

	return HttpResponseRedirect("/book/"+idbook)
	
def cancel_request(request, demande):
	"""
	Action qui permet d'annuler une demande d'emprunt
	"""
	Demander.objects.get(pk=demande).delete()

	return HttpResponseRedirect("/my_requests")

def accept_request(request, demande):
	"""
	Action qui permet de valider une demande d'emprunt
	"""
	d = Demander.objects.get(pk=demande)
	d.statut = "c"
	d.save()

	return HttpResponseRedirect("/my_requests")
	
def refuse_request(request, demande):
	"""
	Action qui permet de refuser une demande d'emprunt
	"""
	d = Demander.objects.get(pk=demande)
	d.statut = "n"
	d.save()

	return HttpResponseRedirect("/my_requests")

def get_author_json(request, pk):
	author = Author.objects.get(pk=pk)
	data = {"firstname" : author.lastname,
			"lastname" : author.firstname}
	import json
	text = json.dumps(data, indent=2, ensure_ascii = False)

	response = HttpResponse(text, mimetype="application/json; charset=utf8")
	return response
