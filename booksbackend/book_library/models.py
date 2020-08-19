from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Publisher(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100, default=f'{first_name} {last_name}')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=200, default='')
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING)
    publication_date = models.DateField()
    pages = models.IntegerField(default=0)
    score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )

    read = models.BooleanField(default=0)
    on_wishlist = models.BooleanField(default=1)
    in_possession = models.BooleanField(default=0)
    reading =  models.BooleanField(default=0)
    
    date_added = models.DateField(auto_now_add=True)
    date_started_reading = models.DateField(null=True, blank=True)
    date_acquired = models.DateField(null=True, blank=True)
    date_read = models.DateField(null=True, blank=True)
    
    EAN = models.CharField(max_length=20, default=0)
    URL = models.URLField(max_length=200, default='#')
    
    # class Meta:
        # unique_together = ['title', 'EAN']
    
    def get_authors(self):
        return ", ".join([str(a) for a in self.authors.all()])                    
    
    def __str__(self):
        return self.title

    def __iter__(self):
        for field in self._meta.get_fields():
            value = getattr(self, field.name, None)
            yield (field.name, value)

            
