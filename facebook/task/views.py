from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.views import generic,View
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .forms import *
from django.shortcuts import HttpResponseRedirect, HttpResponse

# Create your views here.
# ..........................................................signup,signin,signout......................................
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = NewUserForm(data=request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Sucessful')
            return redirect('home')
        else:
            message = form.errors
            return render(request, 'home.html', {'message': message})
    else:
        form = NewUserForm()
        return render(request, 'home.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request,"Login Sucessfully")
                return redirect('page')
        else:
            messages.info(request, 'Please Enter Valid Username and Password')
            return render(request, 'home.html', {'form': form})
    
    form = AuthenticationForm()
    return render(request, 'home.html', {'form': form})

def signout(request):
    logout(request)
    messages.success(request, "Logout Sucessfully")
    return redirect(reverse('home'))
    
# .....................................profile pic upload               view.........................................................
class ProfileView(generic.View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            profiledata, created = ProfileUpload.objects.get_or_create(profileuser=request.user)
            posts =Post.objects.filter(postuser=request.user).order_by('-post_date')
            return render(request,'profile.html',{'profiledata':profiledata,'posts':posts,})   
            
    def post(self,request,*args,**kwrags):
        if request.user.is_authenticated:
            data = ProfileUpload.objects.filter(profileuser=request.user).first()
            if data:
                if request.FILES.get('profilefile'):
                    data.img= request.FILES.get('profilefile')
                if request.FILES.get('coverimage'):
                    data.cover_img=request.FILES.get('coverimage')
                if request.POST.get('bio'):
                    data.bio=request.POST.get('bio')
                if request.POST.get('detail'):
                    data.detail=request.POST.get('detail')
                if request.POST.get('hobbies'):
                    data.hobbies=request.POST.get('hobbies')
                data.save()
                return redirect(reverse('page'))
             
            bio=request.POST.get('bio')
            detail=request.POST.get('detail')
            hobbies=request.POST.get('hobbies')
            profilefile=request.FILES.get('profilefile')
            cover_img=request.FILES.get('coverimage')   
            data=ProfileUpload.objects.create(profileuser=request.user,bio=bio,detail=detail,hobbies=hobbies,img=profilefile,cover_img=cover_img)
            return redirect(reverse('page'))

def del_profile(request,id):
        del_post=ProfileUpload.objects.get(id=id)
        del_post.delete()
        return redirect('page')
    
    
def profile_content_update(request):
    if request.method=='POST':
        form=profileupload(data=request.POST)
        if form.is_valid():
            form.save()
        return render(request,'profileupdate.html',)

    else:
        form=profileupload()
        return render(request,'profileupdate.html',)


# ................................................Main page.......................................................... 

class Page(generic.View):
    def get(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        if request.user.is_authenticated:
            ls= []
            friends = FriendList.objects.filter(user=request.user)
            for i in friends:
                ls.append(i.friend_id)
            ls.append(request.user.id)

            others = User.objects.exclude(id__in=ls)
            others_user = []
            for i in others:
                others_user.append(i.id)
            userpost = Post.objects.exclude(postuser__in=others_user).order_by('-post_date')
            # import pdb;pdb.set_trace()
            post_id = request.POST.get('post_id')
            post_profile=Post.objects.filter(postuser=request.user).first().post_profile
            profiledata=ProfileUpload.objects.filter(profileuser=request.user).first()
            likes = PostLikes.objects.filter(user=request.user,post_id=post_id)
            return render(request, 'page.html', {'userpost': userpost, 'likes': likes,'profiledata':profiledata,'post_profile':post_profile})
        else:
            return redirect('signin')
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            post_id = request.POST.get('post_id')
            access_post=Post.objects.all().order_by('-post_date')
            try:
                profiledata = ProfileUpload.objects.get(profileuser=request.user)
            except  ProfileUpload.DoesNotExist:
                profiledata=None      
            data = PostLikes.objects.filter(user=request.user, post_id=post_id).first()
        
        if data:
            data.delete()
            messages.error(request,'UnLiked')
            return render(request, 'page.html', {'profiledata': profiledata,'access_post':access_post})
        
        PostLikes.objects.create(user=request.user, post_id=post_id)
        messages.success(request,'Liked')
        return render(request, 'page.html', {'profiledata': profiledata,})
#..............................................post section...........................................................

class PostUser(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profiledata=ProfileUpload.objects.filter(profileuser=request.user).first()
            post_data=Post.objects.all().order_by('-post_date')

            return render(request,'create_post.html',{'profiledata': profiledata,'post_data':post_data})

    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            update_post=Post.objects.filter(postuser=request.user).last()
            if update_post:
                if request.POST.get('caption'):
                    update_post.caption=request.POST.get('caption')
                if request.FILES.get('file_post'):
                    update_post.file_post=request.POST.get('file_post')
            caption = request.POST.get('caption')
            file_post = request.FILES.get('file_post') 
            Post.objects.create(postuser=request.user,caption=caption,file=file_post)
            return redirect(reverse('page'))
        
def del_post(request,id):
    del_post=Post.objects.get(id=id)
    del_post.delete()
    return redirect('page')

def like_post(request):
    user=request.user
    if request.method=='POST':
        post_id=request.POST.get('post_id')
        post_obj=Post.objects.filter(id=post_id).first()

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like,created=PostLikes.objects.get_or_create(user=user,post_id=post_id)
        if not created:
            if like.value=='Like':
                like.value="UnLike"

            else:
                like.value=='Like'

        like.save()
        return redirect('page')
    return render(request,'create_post.html')

class UserFriend(generic.View):
    def get(self, request,*args, **kwargs):
        profiledata, created = ProfileUpload.objects.get_or_create(profileuser=request.user)
        abc = profiledata.__dict__.get('profileuser_id', None)
        users=User.objects.exclude(id = abc)
        friendrequest=FriendList.objects.filter(user=request.user,status='send').all()
        request_user=FriendList.objects.filter(friend=request.user,status='send').all()
        return render(request, 'friend.html',{'profiledata':profiledata,'users':users,'show_request':friendrequest,'request':request_user})

    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            friend_id=request.POST.get('friend')
            fr_user = User.objects.filter(id=friend_id).first()
            status_=request.POST.get('status')      
            if status_!=User.id and status_=='send':
                friendrequest=FriendList.objects.get_or_create(user=request.user,friend=fr_user,status=status_)   
                return render(request, 'friend.html',{'friendrequest':friendrequest})
        
        return HttpResponse("Request not sent please click checkbox and after send request")


class ShowPost(generic.View):
    def get(self, request, *args, **kwargs):
            ls= []
            friends = FriendList.objects.filter(user=request.user.id).all()
            for i in friends:
                ls.append(i.friend_id)
                ls.append(request.user.id)

            others = User.objects.exclude(id__in=ls)
            others_user = []
            for i in others:
                others_user.append(i.id)
            posts= Post.objects.all().exclude(postuser__in=others_user).order_by('-post_date')
            return render(request, 'showpost.html', {'posts': posts})


class LikeView(generic.View):

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            # import pdb;pdb.set_trace()
            p1=Post.objects.filter(postuser=request.user.id)
            for p2 in p1:
                post_like_count=PostLikes.objects.filter(post=p2,like_status='True').count()
                return redirect(reverse('page'))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            post_id = request.POST['post_id']
            like = request.POST.get('like')
            p1=Post.objects.filter(postuser=request.user)
            for p2 in p1:
                post_like_count=PostLikes.objects.filter(post=p2,like_status='True').count()
                return redirect(reverse('page'))
            if not like:
                like=False      
            else:
                like=True
            data = PostLikes.objects.filter(user=request.user, post_id=post_id).first()

            if data:
                data.delete()
                return redirect(reverse('page', kwargs={'pk':post_id}))

            PostLikes.objects.create(user=request.user, post_id=post_id, like_status=like)
            # import pdb;pdb.set_trace()
            return redirect(reverse('page', kwargs={'pk':post_id}))
        else:
            return redirect(reverse('signin'))

class Comment(generic.View):
    def post(self,request,id,*args,**kwargs):
        if request.user.is_authenticated:
            global simple_variable
            simple_variable
            post_id=simple_variable
            comment=request.POST.get('comment')
            PostComment.objects.create(user=request.user,post_id=post_id,comment=comment)
            
        return redirect(f'/comment/{post_id}/')

    def get(self,request, id, *args,**kwargs):
        if request.user.is_authenticated:
            global simple_variable 
            simple_variable=id
            print(simple_variable)
            post_id=id
            comment_count=PostComment.objects.filter(post_id=post_id).count()
            profile=ProfileUpload.objects.filter(profileuser=request.user).first()
            comment=PostComment.objects.filter(post_id=post_id)
    
            return render(request,'comment.html',{'pk':post_id,'comment':comment,'comment_count':comment_count,'profile':profile})

 
def like_comment(request):
    user=request.user
    if request.method=='POST':
        comment_id=request.POST.get('comment_id')
        post_obj=PostComment.objects.filter(id=comment_id).first()

        if user in post_obj.commentliked.all():
            post_obj.commentliked.remove(user)
        else:
            post_obj.commentliked.add(user)    
        like,created=CommentLike.objects.get_or_create(user=user,post_comment=post_obj)
        if not created:
            if  like=='Like':
                like="UnLike"
            else:
                like=='Like'
        like.save()
        return redirect('page')
    return render(request,'comment.html')

def deletecomment(request,id):
    del_comment=PostComment.objects.get(id=id)
    del_comment.delete()
    return redirect('page')

def search_bar(request):
    search_item=""
    if 'search' in request.GET:
        search_item=request.GET['search']
        data=User.objects.filter(Q(first_name__icontains=search_item)|Q(last_name__icontains=search_item)|Q(username__icontains=search_item)|Q(email__icontains=search_item))
        
    else:
        data=User.objects.filter().all()
        data=None
    context={
        'data':data,
    }
    return render(request,'search.html',context)


