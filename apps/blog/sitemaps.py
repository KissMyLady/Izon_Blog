# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from .models import Article, Category, Tag
from django.db.models.aggregates import Count
from .utils import site_protocol


'''
sitemap是 Google 最先引入的网站地图协议，采用 XML 格式，它的作用简而言之就是优化搜索引擎的索引效率
'''


# 基础类
class MySitemap(Sitemap):
    protocol = site_protocol()


# 文章协议
class ArticleSitemap(MySitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.update_date


class CategorySitemap(MySitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Category.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)

    def lastmod(self, obj):
        return obj.article_set.first().create_date


# 标签地图
class TagSitemap(MySitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Tag.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)

    def lastmod(self, obj):
        return obj.article_set.first().create_date
