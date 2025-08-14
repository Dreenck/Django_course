from django.db import models
from django.core.validators import MinLengthValidator
from django.urls import reverse

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.caption}"


class Author(models.Model):
    firts_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.firts_name} {self.second_name}"


class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images", null=True)
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, related_name="posts", null=True)
    tag = models.ManyToManyField(Tag)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])

    def get_absolute_url(self):
        return reverse("", args=[self.slug])
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=254)
    comment_text = models.TextField(max_length=300)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return f"{self.user_name}, {self.user_email}"