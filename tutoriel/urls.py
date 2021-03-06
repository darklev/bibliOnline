from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'tutoriel.views.home', name='home'),
    #url(r'^tutoriel/', include('tutoriel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #Page d'accueil de l'application
    url(r'^/?$', "biblio.views.show_main"),

    #Liste des sujets
    url(r'^subjects/?$', "biblio.views.show_subjects"),
    url(r'^addsubject/?$', "biblio.views.show_addSubjectForm"),

    #Liste des livres
    url(r'^books/?$', "biblio.views.show_books"),
	#DÃ©tail d'un  livre
    url(r'^book/(\d+)/?$', "biblio.views.show_book"),
    #Formulaire ajout d'un livre
    url(r'^addbook/?$', "biblio.views.show_addBookForm"),

    #Liste des auteurs
    url(r'^authors/?$', "biblio.views.show_authors"),
    #Affichage des informations d'un auteur
    url(r'^author/(\d+)/?$', "biblio.views.show_author"),

    url(r'^author-json/(\d+)/?$', "biblio.views.get_author_json"),

    #suppression d'un auteur
    url(r'^delauthor/(\d+)/?$', "biblio.views.delete_author"),

    #Formulaire ajout d'un auteur
    url(r'^addauthor/?$', "biblio.views.show_addAuthorForm"),

    #page d'authenfication
    url(r'^authentification[\?next=.*]?$', "biblio.views.login_page"),

    #log out
    url(r'^logout/?$', "biblio.views.logout_action"),


    #les users
    url(r'^users/?$', "biblio.views.show_users"),

    #Demande d'emprunt. arg1 = id membre user cible. arg2 = livre cible
    url(r'^askabook/(.*)/(\d+)/?$', "biblio.views.askfor_action"),

    #met Ã  jour les livres de l'utilisateur
    url(r'^setbooks/?$', "biblio.views.i_own_these_books"),

    #les livres que possÃ©dent le user.
    url(r'^mybooks/?$', "biblio.views.show_mybooks"),

    #les users qui possÃ©dent ce livre
    url(r'^whoownthisbook/(\d+)/?$', "biblio.views.who_own_this_book"),

	#commenter un livre
    url(r'^book/comment/(\d+)/?$', "biblio.views.comment"),

	#les demandes
    url(r'^my_requests/?$', "biblio.views.my_requests"),
    
    #annuler une demande
    url(r'^cancel/(\d+)?$', "biblio.views.cancel_request"),
    
    #accepter une demande
    url(r'^accept/(\d+)?$', "biblio.views.accept_request"),
    
    #refuser une requete
    url(r'^refuse/(\d+)?$', "biblio.views.refuse_request")
)
