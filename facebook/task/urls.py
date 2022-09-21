from django.urls import path
from.import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
       path('',views.home,name='home'),
       path('register/',views.register,name='register'),
       path('signin/',views.signin,name='signin'),
       path('signout/',views.signout,name='signout'),
       path('page/',views.Page.as_view(),name='page'),
       path('friend/',views.UserFriend.as_view(),name='friend'),
       path('friend/<int:id>',views.UserFriend.as_view(),name='friends'),
       path('profile/',views.ProfileView.as_view(),name='profile'),
       path('profiledelete/?<int:id>',views.del_profile,name='profiledelete'),
       path('postuser/',views.PostUser.as_view(),name='postuser'),
       path('postdelete/<int:id>/',views.del_post,name='postdelete'),
       path('showpost/',views.ShowPost.as_view(),name='showpost'),
       path('likes/',views.LikeView.as_view(),name='likes'),
       path('comment/<int:id>/',views.Comment.as_view(),name='comment'),
       path('proupdate/',views.profile_content_update,name='proupdate'),
       path('like/',views.like_post,name='like'),
       path('commentlike/',views.like_comment,name='commentlike'),     
       path('commentdelete/<int:id>/',views.deletecomment,name='commentdelete'),
       path('searchbar/',views.search_bar,name='searchbar'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

