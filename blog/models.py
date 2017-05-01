from django.db import models
from django.contrib.auth.models import User
from uuslug import slugify
from markdown import markdown
from django.core.urlresolvers import reverse
from collections import defaultdict


# 文章分类
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="类名")
    slug = models.SlugField(max_length=150, null=True, blank=True, editable=False)
    user = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category', args=(self.slug,))

    def __str__(self):
        return self.name


class ArticleManage(models.Manager):
    def archive(self):
        date_list = Article.objects.datetimes('write_time', 'month', order='DESC')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
        return sorted(date_dict.items(), reverse=True)  # 模板不支持defaultdict


class Article(models.Model):
    objects = ArticleManage()
    title = models.CharField(max_length=100)
    abstract = models.TextField(default='', null=True, blank=True)
    user = models.ForeignKey(User, default=None, null=True, blank=True, verbose_name="作者")
    category = models.ForeignKey(Category)
    slug = models.SlugField(max_length=150, null=True, blank=True, editable=False)
    content = models.TextField(default='', verbose_name="内容")
    write_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:article', args=(self.slug,))

    class Meta:
        ordering = ['-write_time']

    def __str__(self):
        return self.title


# 保存用户个人信息
class LBUser(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    headimg = models.ImageField(upload_to='user/headimg', blank=True)
    signature = models.CharField(max_length=50, default="欢迎来到我的小站")

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField('标签名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name
