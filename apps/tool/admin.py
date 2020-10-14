from django.contrib import admin
from .models import ToolCategory, ToolLink
from django.conf import settings


'''
# 是否开启[在线工具]应用
TOOL_FLAG = os.getenv('IZONE_TOOL_FLAG', 'True').upper() == 'TRUE'
'''

# 工具标志
# Register your models here.
if settings.TOOL_FLAG:
    @admin.register(ToolLink)  # 使用装饰器生成管理类, 不用注册
    class ToolLinkAdmin(admin.ModelAdmin):
        # 显示字段
        list_display = ('name', 'description', 'link', 'order_num', 'category')
        
        # 筛选字段
        list_filter = ('category',)


    @admin.register(ToolCategory)  # 使用装饰器生成管理类, 不用在admin注册
    class ToolCategoryAdmin(admin.ModelAdmin):
        list_display = ('name', 'order_num')


