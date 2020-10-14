from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.views import generic
from django.conf import settings

# 导入模型类
from .models import Article, Tag, Category, Timeline, Silian, AboutBlog

# 返回当前站点完整地址，协议+域名
from .utils import site_full_url
from django.core.cache import cache

from markdown.extensions.toc import TocExtension  # 锚点的拓展
import markdown
import time, datetime

from haystack.generic_views import SearchView  # 导入搜索视图
from haystack.query import SearchQuerySet


# test 文件什么都没写
def goview(request):
    return render(request, 'test_html.html')


# 档案文件
class ArchiveView(generic.ListView):
    model = Article
    template_name = 'blog/archive.html'
    context_object_name = 'articles'
    paginate_by = 200
    paginate_orphans = 50


'''
# 统一分页设置
BASE_PAGE_BY = 10
BASE_ORPHANS = 5
'''
# 分页升级版
# 博客文章: https://www.cnblogs.com/rinka/p/django_generic_view_ListView.html
class IndexView(generic.ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)     # 分页
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)   # 分页

    def get_ordering(self):
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ('-is_top', '-create_date')


# 详情页面
class DetailView(generic.DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super(DetailView, self).get_object()
        
        # 设置浏览量增加时间判断, 同一篇文章两次浏览超过半小时才重新统计阅览量, 作者浏览忽略
        u = self.request.user
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        if u != obj.author:
            if not is_read_time:
                obj.update_views()
                ses[the_key] = time.time()
            else:
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 * 30:
                    obj.update_views()
                    ses[the_key] = time.time()
                    
        # 获取文章更新的时间，判断是否从缓存中取文章的markdown,可以避免每次都转换
        ud = obj.update_date.strftime("%Y%m%d%H%M%S")
        md_key = '{}_md_{}'.format(obj.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            obj.body, obj.toc = cache_md
        else:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
            ])
            obj.body = md.convert(obj.body)
            obj.toc = md.toc
            cache.set(md_key, (obj.body, obj.toc), 60 * 60 * 12)
        return obj


# 种类
class CategoryView(generic.ListView):
    model = Article
    template_name = 'blog/category.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(CategoryView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(CategoryView, self).get_queryset()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return queryset.filter(category=cate)

    def get_context_data(self, **kwargs):
        context_data = super(CategoryView, self).get_context_data()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章分类'
        context_data['search_instance'] = cate
        return context_data


# 标签视图
class TagView(generic.ListView):
    model = Article
    template_name = 'blog/tag.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(TagView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(TagView, self).get_queryset()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return queryset.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context_data = super(TagView, self).get_context_data()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章标签'
        context_data['search_instance'] = tag
        return context_data


# 关于站长
def AboutView(request):
    if request.method == "GET":
        obj = AboutBlog.objects.first()
        # 数据库提取
        if obj:
            ud = obj.update_date.strftime("%Y%m%d%H%M%S")
            md_key = '{}_md_{}'.format(obj.id, ud)
            cache_md = cache.get(md_key)
            
            if cache_md:
                body = cache_md
            else:
                body = obj.body_to_markdown()
                cache.set(md_key, body, 3600 * 24 * 15)
        # None
        else:
            repo_url = 'https://github.com/KissMyLady'
            body = '<li>作者 Github 地址：<a href="{}">{}</a></li>'.format(repo_url, repo_url)
        return render(request, 'blog/about.html', context={'body': body})
    

# 时间线
class TimelineView(generic.ListView):
    model = Timeline
    template_name = 'blog/timeline.html'
    context_object_name = 'timeline_list'


# 站点地图
class SilianView(generic.ListView):
    model = Silian
    template_name = 'blog/silian.xml'
    context_object_name = 'badurls'


# 重写搜索视图，可以增加一些额外的参数，且可以重新定义名称
class MySearchView(SearchView):
    context_object_name = 'search_list'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    queryset = SearchQuerySet().order_by('-views')


# 爬虫协议
def robots(request):
    site_url = site_full_url()
    
    context = {
        'site_url': site_url
    }
    return render(request, 'robots.txt', context, content_type='text/plain')
