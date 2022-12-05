from django.shortcuts import render , HttpResponse , redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import login , logout , authenticate


def home ( request ) :
    return render ( request , 'home/home.html' )


def about ( request ) :
    return render ( request , 'home/about.html' )


def contact ( request ) :
    if request.method == 'POST' :
        name = request.POST [ 'name' ]
        email = request.POST [ 'email' ]
        phone = request.POST [ 'phone' ]
        content = request.POST [ 'content' ]

        if name == " " or len ( email ) < 8 or len ( phone ) < 10 or len ( content ) < 2 :
            messages.error ( request , "Please fill the form correctly !!" )
        else :
            contact = Contact ( name=name , email=email , phone=phone , content=content )
            contact.save ()
            messages.success ( request , "Issue has been reported !!" )

    return render ( request , 'home/contact.html' )


def search ( request ) :
    query = request.GET [ 'query' ]
    if len ( query ) > 50 or len ( query ) == 0 :
        allPosts = Post.objects.none ()
        message = "Please Fill the Keyword(s) to be Searched!"
        messages.warning ( request , message )
    else :
        allPostsTitle = Post.objects.filter ( title__icontains=query )
        allPostsContent = Post.objects.filter ( content__icontains=query )
        allPosts = allPostsTitle.union ( allPostsContent )
    if allPosts.count () == 0 and len ( query ) != 0 :
        messages.warning ( request , "No Match to Query found" )

    params = {'allPosts' : allPosts , 'query' : query}
    return render ( request , 'home/search.html' , params )


def handleSignUp ( request ) :
    if request.method == 'POST' :
        username = request.POST [ 'username' ]
        fname = request.POST [ 'fname' ]
        lname = request.POST [ 'lname' ]
        email = request.POST [ 'email' ]
        pass1 = request.POST [ 'pass1' ]
        pass2 = request.POST [ 'pass2' ]
        print ( fname , lname )

        if len ( username ) < 5 :
            messages.error ( request , "Username must contain 5 Characters!" )
            return redirect ( 'home' )

        if username [ 0 ] in '0123456789' :
            messages.error ( request , "Username must begin with Character!" )
            return redirect ( 'home' )

        if not username.isalnum () :
            messages.error ( request , "Username should only contain Alphabets and Numbers !!" )
            return redirect ( 'home' )

        if pass1 != pass2 :
            messages.error ( request , "Passwords do not match" )
            return redirect ( 'home' )

        # create user
        myuser = User.objects.create_user ( username , email , pass1 )
        myuser.first_name = fname
        myuser.lasr_name = lname
        myuser.save ()
        messages.success ( request , 'Account Created Successfully !!!' )
        return redirect ( home )

    else :
        return HttpResponse ( '404-Not Found' )


def handleLogIn ( request ) :
    if request.method == 'POST' :
        loginusername = request.POST [ 'loginusername' ]
        loginpass = request.POST [ 'loginpass' ]

        user = authenticate ( username=loginusername , password=loginpass )

        if user is not None :
            login ( request , user )
            messages.success ( request , "Logged In Successfully" )
            return redirect ( 'home' )
        else :
            messages.error ( request , "Invalid Username or Password, Try Again!!!" )
            return redirect ( 'home' )
    return HttpResponse ( "404 - Not Found!!" )


def handleLogOut ( request ) :
    logout ( request )
    messages.success ( request , "Logged Out Successful" )
    return redirect ( 'home' )
    return HttpResponse ( "Handle LogOut" )
