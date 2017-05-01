from django.contrib import admin
from blog.models import Category, Article, LBUser, Tag
from ueditor.widgets import Ueditor
from django.forms import ModelForm
# Register your models here.


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            'content': Ueditor(),
        }


class ArticleAdmin(admin.ModelAdmin):
    # list_display = ('title', 'slug', 'category', 'user', 'write_time')
    form = ArticleForm
    # search_fields = ('content',)
    # class Media:
    #     # 在管理后台的HTML文件中加入js文件, 每一个路径都会追加STATIC_URL/
    #     js = (
    #         'ueditor/ueditor.all.js',
    #         # 'ueditor/ueditor.config.js',
    #         # 'ueditor/lang/zh-cn/zh-cn.js'
    #     )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'user')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(LBUser)
admin.site.register(Tag)
