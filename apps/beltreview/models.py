from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def register(self, postData):
        errors = {}
        userList = User.objects.filter(email = postData['email'])
        email_regex = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
        if len(postData['name']) < 2:
            errors["name"] = "Name should be more than 2 characters"
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should be more than 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be more than 8 characters"
        if postData['password'] != postData['confpw']:
            errors["password"] = "Passwords must match"
        if len(postData['email']) < 1:
            errors["email"] = "Email address field is required"
        if len(userList) > 0:
            errors["email"] = "There can only be one user per email address"
        if not email_regex.match(postData['email']):
            errors["email"] = "Email is invalid."
        return errors

    def login(self, postData):
        errors = {}
        return errors

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, related_name="authors_books")

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="users_reviews")
    book = models.ForeignKey(Book, related_name="reviewed_books")
