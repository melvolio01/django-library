from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a genre (eg "Comedy")')

    def __str__(self):
        #String for representing the Model object
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100, help_text='Language Name')

    def __str__(self):
        return self.name

class Book(models.Model):
    # Model representing a 'book' but not a specific instance  (ie, individual library copy)
    title = models.CharField(max_length=200)

    # Foreign key - book can have only one author here, though each author can have multiple books
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text="Please add a short description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 character ISBN number')

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Return url to access detail record for the book
        return(reverse('book-detail', args=[str(self.id)]))

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this copy")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    LOAN_STATUS = (
        ('m', 'maintenance'),
        ('o', 'on loan'),
        ('r', 'reserved'),
        ('a', 'available')
    )

    status = models.CharField(
        max_length = 1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{ self.id } ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text='Author\'s first name')  
    surname = models.CharField(max_length=100, help_text='Author\'s surname')
    date_of_birth = models.DateField(null=True, blank=True)  
    date_of_death = models.DateField('Died', null=True, blank=True) 

    class Meta: 
        ordering = ['surname', 'first_name']

    def get_absolute_url(self):
        return(reverse('author-detail', args=[str(self.id)])) 

    def __str__(self):
        return f'{ self.surname }, { self.first_name }'
