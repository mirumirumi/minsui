from django.urls import path
from . import views

app_name = "app_music_db"

urlpatterns = [
    # URLのみハイフン、その他nameやhtmlファイル名はアンダースコアで統一
    path("", views.IndexView.as_view(), name="index"),
    path("add", views.add, name="add"),
    path("add-album", views.add_album, name="add_album"),
    path("edit/<int:pk>", views.edit, name="edit"),
    path("delete/<int:pk>", views.delete, name="delete"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("privacy-policy", views.privacy_policy, name="privacy_policy"),
    path('hygfnfr7gjy8kswdtxhzscx27f9tinm6d86hhyf48iu5dxga893bkcz9pi59zkf4328/', views.CsvImport.as_view(), name='import'),
    path('m4x3n2pa9xy3fsfawn2a9g7dduwnzx32etdbrjp9mkaetyeucgyrs6iu29pkmr8ryhy/', views.CsvExport, name='export'),
    path('api/songs/get/', views.api_songs_get, name='api_songs_get'),
    path('api/composers/get/', views.api_composers_get, name='api_composers_get'),
    path('api/arrangers/get/', views.api_arrangers_get, name='api_arrangers_get'),
    path('api/artists/get/', views.api_artists_get, name='api_artists_get'),
    path('api/cds/get/', views.api_cds_get, name='api_cds_get'),
    # path("detail/<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("comment/<int:pk>/", views.CommentPostView.as_view(), name="comment"),
    path('ajax_comment_add', views.ajax_comment_add, name='ajax_comment_add'),
    path('ajax_recaptcha', views.ajax_recaptcha, name='ajax_recaptcha'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('ads.txt', views.ads, name='ads'),
]
