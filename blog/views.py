from django.shortcuts import render
from blog.models import Article, Category
from django.views.generic.list import ListView
from blog.models import Tag
from django.db.models import Q

# Create your views here.
def index(request):
    article_list = Article.objects.filter()
    category_list = Category.objects.all().order_by('name')
    date_archive = Article.objects.archive()
    tag_list = Tag.objects.all().order_by('name')
    footer = True
    return render(request, 'blog/index.html', {'article_list': article_list, 'category_list': category_list,
                                               'date_archive': date_archive, 'tag_list': tag_list, 'footer': footer})


def article_detail(request, article_slug):
    article = Article.objects.get(slug=article_slug)
    category_list = Category.objects.all().order_by('name')
    date_archive = Article.objects.archive()
    tag_list = Tag.objects.all().order_by('name')
    return render(request, 'blog/detail.html', {'article': article,
                                                'category_list': category_list,
                                                'date_archive': date_archive,
                                                'tag_list': tag_list})


class TagView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'])
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        return super(TagView, self).get_context_data(**kwargs)


def category_detail(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    article_list = Article.objects.filter(category=category)
    return render(request, 'blog/category.html', {'category': category, 'article_list': article_list})


class CategoryView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(category__slug=self.kwargs['category_slug'])
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(CategoryView, self).get_context_data(**kwargs)


class ArchiveView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        article_list = Article.objects.filter(write_time__year=year, write_time__month=month)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        return super(ArchiveView, self).get_context_data(**kwargs)


class SearchView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(Q(title__icontains=self.kwargs['search_key']) |
                                              Q(content__icontains=self.kwargs['search_key']))
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(SearchView, self).get_context_data(**kwargs)


# 处理关于的部分
def about(request):
    category_list = Category.objects.all().order_by('name')
    date_archive = Article.objects.archive()
    tag_list = Tag.objects.all().order_by('name')
    return render(request, 'blog/about.html', {'category_list': category_list,
                                               'date_archive': date_archive,
                                               'tag_list': tag_list})