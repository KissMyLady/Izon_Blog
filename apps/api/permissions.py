# -*- coding: utf-8 -*-
from rest_framework import permissions
# 它是基于Django的，帮助我们快速开发符合restful规范的接口框架,它主要适用于前后端分离项目。
# pip install djangorestframework 需要在app中安装它
# 介绍使用: https://www.jianshu.com/p/714b20de337a


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff