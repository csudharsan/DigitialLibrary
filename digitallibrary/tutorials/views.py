from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Q
from django.http import HttpResponse
from . models import SoftwareTutorials, Book
from . forms import SoftwareTutorialsForm, BookForm, UserForm
from django.urls import reverse
from django.http.response import HttpResponseRedirect, HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
#from django.template import loader
# Create your views here.

def delete_tutorial(request, softwaretutorials_id):
    tuts = SoftwareTutorials.objects.get(pk=softwaretutorials_id)
    all_softwaretuts = SoftwareTutorials.objects.all()
    #template = loader.get_template('tutorials/index.html')
    try:
        tuts.delete()
        return HttpResponseRedirect('/tutorials/')
    except ObjectDoesNotExist:
        return HttpResponseServerError()
          
    context = {
        'all_softwaretuts' : all_softwaretuts
        }

    return render(request, 'tutorials/index.html', context)
    

def create_tutorial(request):
    if not request.user.is_authenticated():
        form = UserForm(request.POST or None)
        return render(request, 'tutorials/user_login.html', {'form' : form})
    else:
        form = SoftwareTutorialsForm(request.POST or None, request.FILES or None)
    
        if form.is_valid():
            #soft_tuts = form.save(commit=False)
            soft_tuts = form.save()
            
            return render(request,'tutorials/detail.html', {'soft_tuts' : soft_tuts })
            #return render(request, 'music/detail.html', {'album': album})
        
        context = {
            'form' : form
            }
        return render(request, 'tutorials/create_tutorial.html', context)


def create_book(request, softwaretutorials_id):
    form = BookForm(request.POST or None, request.FILES or None)
    soft_tuts = get_object_or_404(SoftwareTutorials, pk=softwaretutorials_id)
        
    if form.is_valid():
        #clean data
        for data in soft_tuts.book_set.all():
            if data.book_title == form.cleaned_data.get("book_title"):
                context= {
                    'soft_tuts' : soft_tuts,
                    'form' : form,
                    'error_message' : "Book already exists!!!"
                }
                return render(request,'tutorials/create_book.html', context)
        book = form.save(commit=False)
        book.softwaretutorials = soft_tuts    
        
        book.save()
        #return HttpResponse("<h1> Book created</h1>")
        print("Soft tuts:", soft_tuts)
        return render(request, 'tutorials/detail.html', { 'soft_tuts' : soft_tuts })
    
    context = {
        'soft_tuts' : soft_tuts,
        'form' : form
        }
    return render(request,'tutorials/create_book.html', context)
    #return HttpResponse('<h1>Add book here</h1>')
    
    
def delete_book(request, softwaretutorials_id, book_id):
    soft_tuts = SoftwareTutorials.objects.get(pk=softwaretutorials_id)
    book = Book.objects.get(pk=book_id)
    try:
        book.delete()
        print("book is deleted:", soft_tuts.id)
        #return HttpResponse('<h1> Hello world</h1>')
        return HttpResponseRedirect('/tutorials/'+str(soft_tuts.id)+'/')
    except Book.DoesNotExist:
        return HttpResponseServerError()
        #reverse('books/detail.html', kwargs = {'soft_tuts' : soft_tuts })
        
        #return redirect(detail, { 'soft_tuts' :soft_tuts })
        #template = loader.get_template('books/index.html')  
    context = {
        'soft_tuts' : soft_tuts
        }

    return render(request, 'tutorials/detail.html', context)

    

def view_books(request):
    
    all_softwaretuts = SoftwareTutorials.objects.all()
    
    return render(request,'tutorials/view_books.html', {'all_softwaretuts' : all_softwaretuts})




def index(request):
    if not request.user.is_authenticated():
        return render(request, 'tutorials/user_login.html')
    else:
        tutorials = SoftwareTutorials.objects.all()
        books = Book.objects.all()
        query = request.GET.get('q')
        if query:
            tutorials = tutorials.filter(
                    Q(language__icontains=query) |
                    Q(creator__icontains=query)
                ).distinct()
            books = books.filter(
                    Q(book_title__icontains=query)|
                    Q(book_author__icontains=query)
                ).distinct()
            return render(request, 'tutorials/index.html', {
                'all_softwaretuts': tutorials,
                'q_books': books,
                })
            
    all_softwaretuts = SoftwareTutorials.objects.all()
    #template = loader.get_template('tutorials/index.html')  
    context = {
        'all_softwaretuts' : all_softwaretuts
        }
    #return HttpResponse()
    #return HttpResponse(template.render(context,request))
    return render(request, 'tutorials/index.html', context)
    
    

def detail(request, softwaretutorials_id):
    try:
        soft_tuts = SoftwareTutorials.objects.get(pk=softwaretutorials_id)
    except SoftwareTutorials.DoesNotExist:
        raise Http404("Could not find Software tutorial!!!")
    
    return render(request, 'tutorials/detail.html', {'soft_tuts': soft_tuts})
    
    #return HttpResponse('<h2>Books on Software Tutorial '+str(softwaretutorials_id)+' </h2>')
    
    
def user_registration(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('i am here')
                all_softwaretuts = SoftwareTutorials.objects.all()
                return render(request, 'tutorials/index.html', {'all_softwaretuts' : all_softwaretuts } )
            else:
                return render(request,'tutorials/user_login.html', {'error_message': "Your account is disabled"})
        else:
            return render(request,'tutorials/user_login.html', {'error_message': "Invalid login"})
    context = {
        'form' : form
        }    
        
    return render(request,'tutorials/user_registration.html', context)
    
        

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                tutorials = SoftwareTutorials.objects.all()
                return render(request, 'tutorials/index.html', {'all_softwaretuts' : tutorials})
            else:
                return render(request,'tutorials/user_login.html', {'error_message': "Your account is disabled"})
        else:
            return render(request,'tutorials/user_login.html', {'error_message': "Invalid login"})
         
    return render(request,'tutorials/user_login.html')
        


def user_logout(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        'form' : form
        }
    return render(request, 'tutorials/user_login.html', context)

