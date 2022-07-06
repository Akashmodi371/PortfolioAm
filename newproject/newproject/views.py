import email
# ----------------Blog------------------
from datetime import datetime
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from blog.forms import BlogForm, SignUpForm,EditProfile,EditAdminProfile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from blog.models import Blog,Images
from django.core.files.storage import FileSystemStorage
# --------------------------------------
from logging import exception
from queue import Empty
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import contactform 
from contact.models import contact
def aboutid(request,name):
    return HttpResponse(name)

def home(request):
    fn=contactform()
    try:
        Name=Empty
        if request.method=="POST":
            Name=request.POST['Name']
            Email=request.POST['Email']
            Mobile=request.POST['Mobile']
            Message=request.POST['message']
            en=contact(Name=Name,Email=Email,Mobile=Mobile,Message=Message)
            print(Name,Email,Mobile,Message)
            en.save()
    except:
        pass
    return render(request,'index.html',{'output':fn})
    
def contact(request):
    return render(request,'contact.html')


def blog(request):
    blog=Blog.objects.all()
    images=Images.objects.all()
    # images=Image.obj.filter()
    return render(request,'blog/home.html',{'blogs':blog,'images':images}) 

def signup(request):
    if request.method=="POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,'Thanks for resgistration')
            fm.save()
            return HttpResponseRedirect('/signin/')
    else:
        fm=SignUpForm()
    return render(request,'blog/signup.html',{'form':fm})


################## user Signin ######################
def signin(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Login Successfully!!!!!!!!!')
                    return HttpResponseRedirect('/dashboard/')
        fm=AuthenticationForm()
        return render(request,'blog/signin.html',{'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')


################### user logout code ############################
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/signin/')




################  user dashboard code ############################
def dashboard(request):
    if request.user.is_authenticated:
        name=request.user
        blog=Blog.objects.all()
        images=Images.objects.all()
        return render(request,'blog/dashboard.html',{'name':name,'blogs':blog,'images':images})
    else:
        return HttpResponseRedirect('/signin/')


################ user Profile section #############################
def profile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            if request.user.is_superuser ==True:
                fm=EditAdminProfile(request.POST,instance=request.user)
                allusers=User.objects.all()
                if fm.is_valid():
                    messages.success(request,'Profile Updated SuccessFully...')
                    fm.save()
                    messages.success(request,'Profile Updated Successfully..............')
                    return HttpResponseRedirect('/profile/')
            else:
                fm=EditProfile(request.POST,instance=request.user)
                allusers=None
                if fm.is_valid():
                    messages.success(request,'Profile Updated SuccessFully...')
                    fm.save()
                    messages.success(request,'Profile Updated Successfully..............')
                    return HttpResponseRedirect('/profile/')
        else:        
            if request.user.is_superuser ==True:
                fm=EditAdminProfile(instance=request.user)
                allusers=User.objects.all()
            else:
                fm=EditProfile(instance=request.user)
                allusers=None
        return render(request,'blog/profile.html',{'name':request.user.username,'form':fm,'users':allusers})
    else:
        return HttpResponseRedirect('/signin/')


############## change password using old password ########################
def changepass(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,'Password Reset Successfully!!!!')
                return HttpResponseRedirect('/profile/')
        else:
            
            fm=PasswordChangeForm(user=request.user)
        return render(request,'blog/changepass.html',{'form':fm,'name':request.user})
    else:
        return HttpResponseRedirect('/signin/')


################ USer Detail in admin ##################
def userdetail(request,id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        fm=EditAdminProfile(instance=pi)
        return render(request,'blog/userdetail.html',{'form':fm,'name':request.user})
    else:
        return HttpResponseRedirect('/login/')


################ View Blog #########################



############# Add Blog ############################
# def addblog(request):
#     if request.user.is_authenticated:
#         if request.method=="POST":
#             fm=BlogForm(request.POST)
#             if fm.is_valid():
#                 fm.instance.Author=request.user
#                 fm.save()
#                 messages.success(request,"Blog Saved Successfully......")
#                 return HttpResponseRedirect('/dashboard/')
#         else:
#             fm=BlogForm()
#         return render(request,'blog/addblog.html',{'form':fm,'name':request.user})
#     else:
#         return HttpResponseRedirect('/login/')



############# Add Blog With single image ############################
# def addblog(request):
#     if request.user.is_authenticated:
#         if request.method=="POST":
#             blog=Blog()
#             blog.Title= request.POST.get('title')
#             blog.Description= request.POST.get('description')
#             blog.Author=request.user
#             blog.image=request.POST.get('document')
#             blog.save()
#             messages.success(request,"Blog Saved Successfully......")
#             return HttpResponseRedirect('/dashboard/')
#         else:
#             fm=BlogForm()
#         return render(request,'blog/addblog.html',{'name':request.user})
#     else:
#         return HttpResponseRedirect('/login/')





############# Add Blog With Multiple image ############################
def addblog(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            blog=Blog()
            blog.title= request.POST.get('title')
            blog.description= request.POST.get('description')
            blog.author=request.user
            blog.save()
            images=request.FILES.getlist('documents')
            print(images)
            
            
            title=request.POST.get('title')
            # for file in images:
            #     Images.objects.create(blog=request.POST.get('title'),image=file)
            for file in images:
                blogImage = Images()
                blogImage.blogtitle=blog
                blogImage.image=file
                blogImage.save()
            
            messages.success(request,"Blog Saved Successfully......")
            return HttpResponseRedirect('/dashboard/')
        else:
            fm=BlogForm()
        return render(request,'blog/addblog.html',{'name':request.user})
    else:
        return HttpResponseRedirect('/login/')


############### Update Blog ###############################
def updateblog(request,id):
    if request.user.is_authenticated:
            if request.method=="POST":
                obj = get_object_or_404(Blog, id = id)
                obj.title= request.POST.get('title')
                obj.description= request.POST.get('description')
                obj.author=request.user
                obj.updated_on=datetime.now()
                obj.save()
                images=request.FILES.getlist('documents')
                print(images)
                for file in images:
                    blogImage = Images()
                    blogImage.blogtitle=obj
                    blogImage.image=file
                    blogImage.save()
                
                messages.success(request,"Blog Updated Successfully......")
                return HttpResponseRedirect('/dashboard/')
            else:
                blog=Blog.objects.get(pk=id)
                images=Images.objects.filter(blogtitle = blog)
            return render(request,'blog/updateblog.html',{'name':request.user,'blog':blog,'images':images})
    else:
        return HttpResponseRedirect('/login/')


############ Delete Blog ####################################
def deleteblog(request,pk):
    if request.user.is_authenticated:
        pi=Blog.objects.get(pk=pk)
        pi.delete()
        return HttpResponseRedirect('/myblogs/')
    else:
        return HttpResponseRedirect('/login/')

############### delete image ###############################
def deleteimage(request,pk):
    if request.user.is_authenticated:
        pi=Images.objects.get(pk=pk)
        pi.delete()
        return HttpResponseRedirect('/myblogs/')
    else:
        return HttpResponseRedirect('/login/')




###################### Particular User Blogs ###################
def myblogs(request):
    if request.user.is_authenticated:
        blog=Blog.objects.filter(author=request.user)
        images=Images.objects.all()
        
        # blogimage = {} 
        # for i in blog:
        #     images=Images.objects.filter(blogtitle = blog)
        #     blogimage[i['images']] = i[images]
        # print(blogimage)
        
        return render(request,'blog/myblogs.html',{'blogs':blog,'images':images,'name':request.user})
    else:
        return HttpResponseRedirect('/signin')


###################### Particular  Blog ###################
def viewblog(request,pk):
    blog=Blog.objects.get(pk=pk)
    # title=blog.title
    # blog=Blog.objects.filter(pk=pk).first()
    images=Images.objects.filter(blogtitle = blog)
    print(images)
    return render(request,'blog/viewblog.html',{'blog':blog,'images':images,'name':request.user})