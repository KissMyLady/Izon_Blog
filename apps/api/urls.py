# -*- coding:utf-8 -*-
# @Date  : 2019/2/1
from rest_framework.routers import DefaultRouter
from .views import UserListSet
from .views import ArticleListSet
from .views import TagListSet
from .views import CategoryListSet
from .views import TimelineListSet
from .views import ToolLinkListSet


# 管理页面注册
router = DefaultRouter()

router.register(r'users', UserListSet)
router.register(r'articles', ArticleListSet)
router.register(r'tags', TagListSet)
router.register(r'categorys', CategoryListSet)
router.register(r'timelines', TimelineListSet)
router.register(r'toollinks', ToolLinkListSet)
