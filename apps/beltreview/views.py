from django.shortcuts import render, HttpResponse, redirect 
from django.contrib import messages
from models import *
import bcrypt

def index(request):
    context = {
        "user" : User.objects.all()
    }
    return render(request, 'beltreview/index.html', context)

def register(request):
    errors = User.objects.register(request.POST)
    if len(errors):
        for key, error in errors.iteritems():
            messages.error(request, error)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name= request.POST['name'], alias= request.POST['alias'], email = request.POST['email'], password = hash1)
        request.session['id'] = user.id
        return redirect('/books')

def login(request):
    if request.method == "POST":
        userList=User.objects.filter(email=request.POST['email'])
        errors = User.objects.login(request.POST)
        if len(userList) > 0:
            print userList
            user = userList[0]
        else:
            messages.error(request, "Email or password incorrect")
            return redirect('/')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['id'] = user.id
            return redirect('/books')
        else:
            messages.error(request, "Email or password incorrect")
            return redirect('/')
    else:
        return redirect('/')

def success(request):
    if not 'id' in request.session:
        return redirect('/')
    else:
        context = {
            "user" : User.objects.get(id=request.session['id']),
            "reviews" : Review.objects.order_by("-created_at")[:3],
            "books" : Book.objects.all()
        }
        return render(request, 'beltreview/success.html', context)

def user(request, user_id):
    if not 'id' in request.session:
        return redirect('/')
    else:
        num_reviews = Review.objects.filter(user_id=request.session['id']).count()
        context = {
            "user" : User.objects.get(id=request.session['id']),
            "num_reviews" : num_reviews,
            "reviews" : Review.objects.filter(user=User.objects.get(id=request.session['id']))
        }
        return render(request, 'beltreview/user.html', context)

def add(request):
    if not 'id' in request.session:
        return redirect('/')
    else:
        context = {
            "author" : Author.objects.all(),
            "book" : Book.objects.all(),
            "review" : Review.objects.all()
        }
        return render(request, 'beltreview/add.html', context)

def process(request):
# creates new author, book, and review
    if request.method == "POST":
        user = User.objects.get(id=request.session['id'])
        if request.POST['new_author'] == "":
            author = Author.objects.get(name=request.POST['existing_author'])
        else:
            author = Author.objects.create(name=request.POST['new_author'])
        book = Book.objects.create(title=request.POST["book_title"], author=author)
        review = Review.objects.create(content=request.POST['book_review'], rating=request.POST["rating"], user=user, book=book)
        return redirect('/books/' + str(book.id))
    else:
        return redirect('/')

def add_review(request, book_id):
# creates new review on existing book
    if request.method == "POST":
        user = User.objects.get(id=request.session['id'])
        book = Book.objects.get(id=book_id)
        review = Review.objects.create(content=request.POST['book_review'], rating=request.POST["rating"], user=user, book=book)
        
        return redirect('/books/' + str(book.id))
    else:
        return redirect('/')

def book(request, book_id):
    if not 'id' in request.session:
        return redirect('/')
    else:
        context = {
            "book" : Book.objects.get(id=book_id),
            "reviews" : Review.objects.filter(book=Book.objects.get(id=book_id))
        }
        return render(request, 'beltreview/book.html', context)

def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    book_id = review.book.id
    review.delete()
    return redirect('/books/' + str(book_id))

def logout(request):
    del request.session['id']
    return redirect('/')