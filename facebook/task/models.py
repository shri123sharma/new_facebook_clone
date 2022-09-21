from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfileUpload(models.Model):
    profileuser=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profileuser')
    bio=models.CharField(max_length=200,default='',null=True,blank=True)
    detail=models.CharField(max_length=200,default='',null=True,blank=True)
    hobbies=models.CharField(max_length=200,default='',null=True,blank=True)
    friends=models.ManyToManyField(User,related_name='friends',blank=True,)
    img=models.ImageField(upload_to='profile_image',default='')
    cover_img=models.ImageField(upload_to='cover_image',default='')

    def __str__(self):
        
        return str(self.hobbies)

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

status_choices=[
    ('send','send'),
    ('accepted','accepted'),
]
class FriendList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='userfriend',null=True,blank=True)
    friend=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',null=True,blank=True)
    status = models.CharField(max_length=8,default='send',choices=status_choices,null=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}-{self.friend}-{self.status}"
        
    def get_request(self):
        return self.friend.all().count()

class Post(models.Model):
    postuser=models.ForeignKey(
        User,
        verbose_name='UserProfile',
        null=True,
        blank=True,
        related_name='user_post',
        on_delete=models.CASCADE,
    )
    post_date=models.DateTimeField(auto_now_add=True)
    caption=models.TextField()
    file=models.FileField(upload_to='post_image',blank=True,null=True,default='')
    liked=models.ManyToManyField(User,default=None,blank=True,related_name='liked')
    
    def __str__(self):
        return str(self.file)

    @property
    def post_like(self):
        return self.liked.all().count()
    
    @property
    def post_profile(self):
        return ProfileUpload.objects.filter(profileuser=self.postuser).first().img.url


Like_choices=[

    ('Like','Like'),
    ('UnLike','UnLike')
]
   
class PostLikes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='postlikeuser',null=True,blank=True)
    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='postlike',
        null=True,
        blank=True,
    )
    value=models.CharField(choices=Like_choices,default='Like',max_length=10)

    def __str__(self):
        return self.value

class PostComment(models.Model):
    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='postcomment',
        
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="ok")
    comment=models.CharField(max_length=100)
    comment_date=models.DateField(auto_now=True)
    commentliked=models.ManyToManyField(User,default=None,blank=True,related_name='likecomment')

    def __str__(self):
        return str(self.comment)

class CommentLike(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post_comment=models.ForeignKey(
        PostComment,
        on_delete=models.CASCADE,
    )

