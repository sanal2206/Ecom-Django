from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Category,ProductImage,CustomUser
from django.db.models import Avg

from django .contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm,ReviewForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    products=Product.objects.all()
     
    # Calculate the average rating for each product
    for product in products:
        avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
        product.avg_rating = round(avg_rating, 1) if avg_rating else 0
        product.stars_range = range(1, 6)  # Create a range from 1 to 5 for stars

    return render(request,'home.html',{'products':products })





def about(request):
    return render(request,'about.html',{})


def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)  # Could be a coroutine

        if user is not None:
            login(request,user)
            messages.success(request,("You have been logged in"))
            return redirect('home')

        else:
            messages.success(request,'There was an error')
            return redirect('login')
    
    else:

        return render(request,'login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,('You have been logged out...Thanks for shopping'))
    return redirect('home')


#register

def register_user(request):
    form=SignUpForm()
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            #log in user
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,('You have registered succesfully..'))
            return redirect('home')
        else:
            messages.success(request,('There was a problem Registering ,Pplease try agian...'))
            return redirect('register')


    else:

    
    # messages.success(request,('You have been logged out...Thanks for shopping'))
        return render(request,'register.html',{'form':form})


# #product view
# def product(request, pk):
#     products = Product.objects.get(id=pk)
#     images = ProductImage.objects.filter(product=products)
#     related_products = Product.objects.filter(category=products.category).exclude(pk=pk)[:4]  # Show up to 4 related products


#     return render(request, 'product.html', {'products': products, 'image': images, 'related_products': related_products})

@login_required
def product(request, pk):
    # Get the product by primary key (id)
    products = get_object_or_404(Product, id=pk)
    
    # Fetch images for the product
    images = ProductImage.objects.filter(product=products)
    
    # Get related products (same category but excluding the current product)
    related_products = Product.objects.filter(category=products.category).exclude(pk=pk)[:4]  # Show up to 4 related products
    

    # Calculate the average rating for the product
    avg_rating = products.reviews.aggregate(Avg('rating'))['rating__avg']  # Get the average rating
    avg_rating = round(avg_rating, 1) if avg_rating else 0  # Round to 1 decimal place, default to 0 if no reviews

    
     

    # Fetch reviews for the product
    reviews = products.reviews.all()  # Access the reviews related to the product
    
    # Initialize the review form
    form = ReviewForm()

    # Handle POST request for adding a review
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = products  # Associate the review with the current product
            review.user = request.user  # Associate the review with the logged-in user
            review.save()  # Save the review to the database
            return redirect('product', pk=products.id)  # Redirect to the same product page after saving the review

    context = {
        'products': products,
        'images': images,
        'related_products': related_products,
        'reviews': reviews,
        'form': form,  # Include the form for adding reviews
        'avg_rating': avg_rating,  # Pass the average rating to the template

    }

    return render(request, 'product.html', context)

# #category
# def category(request,cat):
#     print(f"Category passed to view: {cat}")  # Debugging statement

#     #replace hyphens with spaces
 

#     #grab the category

#     try:
#         #look up the category
#         category=Category.objects.get(name=cat)
#         products=Product.objects.filter(category=category)
#         return render(request,'category.html',{'products':products,'category':category})
        
#     except:
#         messages.success(request,("Sorry...That category Doesn't exist"))

#         return redirect('home')

def category(request, cat):
    print(f"Category passed to view: {cat}")  # Debugging statement

    # Replace hyphens with spaces (if needed for consistency)
    cat = cat.replace('-', ' ')
    
    try:
        # Look up the category
        category = get_object_or_404(Category, name=cat)  # This will raise a 404 if not found
        print(f"Category found in database: {category.name}")  # Debugging statement
        
        # Get products in the category
        products = Product.objects.filter(category=category)

        for product in products:
            avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
            product.avg_rating = round(avg_rating, 1) if avg_rating else 0
            product.stars_range = range(1, 6)  # Create a range from 1 to 5 for stars
        
        return render(request, 'category.html', {'products': products, 'category': category})
    
    except Category.DoesNotExist:
        # Specific exception if category not found
        print(f"Category not found: {cat}")  # Debugging statement
        messages.error(request, "Sorry... That category doesn't exist.")  # Use 'error' for better visibility
        return redirect('home')