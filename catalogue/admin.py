from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Author, Genre, Language, Book, BookInstance

# admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('surname', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'surname', ('date_of_birth', 'date_of_death')]

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'isbn')

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

#Registering models with admin site
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)

