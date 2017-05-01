from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_slug>[^/]+)/$', views.CategoryView.as_view(), name="category"),
    url(r'^article/(?P<article_slug>[^/]+)/$', views.article_detail, name="article"),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$', views.ArchiveView.as_view(), name='archive'),
    url(r'^tag/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),
    url(r'^search/(?P<search_key>.*)/$', views.SearchView.as_view(), name="search")
]