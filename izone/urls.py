from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView

from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import ArticleSitemap, CategorySitemap, TagSitemap
from blog.feeds import AllArticleRssFeed
from blog.views import robots


# 网站地图
sitemaps = {
    'articles': ArticleSitemap,
    'tags': TagSitemap,
    'categories': CategorySitemap
}


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/blog/img/favicon.ico')),
    path('admin/', admin.site.urls),
    
    # app框架
    path('accounts/', include('allauth.urls')),  # allauth
    path('accounts/', include(('oauth.urls', 'oauth'), namespace='oauth')),  # oauth,只展现一个用户登录界面
    path('', include(('blog.urls', 'blog'), namespace='blog')),  # blog
    path('comment/', include(('comment.urls', 'comment'),namespace='comment')),  # comment
    
    # 爬虫准许文件
    path('robots.txt', robots, name='robots'),  # robots
    
    # 游客默认不开启
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),  # 网站地图
    path('feed/', AllArticleRssFeed(), name='rss'),   # rss订阅
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件

'''
# 是否开启[API]应用
API_FLAG = os.getenv('IZONE_API_FLAG', 'False').upper() == 'TRUE'
'''
if settings.API_FLAG:
    from api.urls import router
    urlpatterns.append(path('api/v1/', include((router.urls, router.root_view_name), namespace='api')))    # restframework

'''
# 是否开启[在线工具]应用
TOOL_FLAG = os.getenv('IZONE_TOOL_FLAG', 'True').upper() == 'TRUE'
'''
if settings.TOOL_FLAG:
    # 工具导航页面, 提供别家的工具
    urlpatterns.append(path('tool/', include(('tool.urls', 'tool'), namespace='tool')))    # tool