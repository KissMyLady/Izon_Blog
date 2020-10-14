import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv('IZONE_SECRET_KEY', '#!kta!9e0)24d@9#=*=ra$r!0k0+p5@w+a%7g1bbof9+ad@4_(')

# 是否开启[在线工具]应用
TOOL_FLAG = os.getenv('IZONE_TOOL_FLAG', 'True').upper() == 'TRUE'

# 是否开启[API]应用
API_FLAG = os.getenv('IZONE_API_FLAG', 'False').upper() == 'TRUE'

# 开启debug
DEBUG = os.getenv('IZONE_DEBUG', 'True').upper() == 'TRUE'
ALLOWED_HOSTS = ['*', ]


sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
INSTALLED_APPS = [
    'bootstrap_admin',  # 注册bootstrap后台管理界面,这个必须放在最前面
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.humanize',  # 添加人性化过滤器  在html中使用
    'django.contrib.sites',     # 这个是自带的，会创建一个sites表，用来存放域名 优化搜索引擎设置
    'django.contrib.sitemaps',  # 网站地图  优化搜索引擎设置
    
    # allauth需要注册的应用
    'allauth', 'allauth.account',
    'allauth.socialaccount',  #
    'allauth.socialaccount.providers.weibo',   # 微博认证
    'allauth.socialaccount.providers.github',  # git认证
    
    'rest_framework',
    
    'crispy_forms',  # bootstrap表单样式
    'imagekit',  # 上传图片的应用
    
    'haystack',  # 全文搜索应用 这个要放在其他应用之前
    'oauth',  # 自定义用户应用
    'blog',  # 博客应用
    'tool',  # 工具
    'comment',  # 评论
]

# 自定义用户model
AUTH_USER_MODEL = 'oauth.Ouser'

# allauth配置
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# allauth需要的配置
# 当出现"SocialApp matching query does not exist"这种报错的时候就需要更换这个ID
# 设置当前站点
SITE_ID = 2

# 设置登录和注册成功后重定向的页面，默认是/accounts/profile/
LOGIN_REDIRECT_URL = "/"

# Email setting
# 注册中邮件验证方法:“强制（mandatory）”,“可选（optional）【默认】”或“否（none）”之一。
# 开启邮箱验证的话，如果邮箱配置不可用会报错，所以默认关闭，根据需要自行开启
ACCOUNT_EMAIL_VERIFICATION = os.getenv('IZONE_ACCOUNT_EMAIL_VERIFICATION', 'none')
# 登录方式，选择用户名或者邮箱都能登录
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# 设置用户注册的时候必须填写邮箱地址
ACCOUNT_EMAIL_REQUIRED = True
# 登出直接退出，不用确认
ACCOUNT_LOGOUT_ON_GET = True

# 表单插件的配置
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'izone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.blog.context_processors.settings_info',  # 自定义上下文管理器 dict()
            ],
        },
    },
]
'''
def settings_info(request):
    return {
        'site_logo_name': settings.SITE_LOGO_NAME,
        'site_end_title': settings.SITE_END_TITLE,
        'site_description': settings.SITE_DESCRIPTION,
        'site_keywords': settings.SITE_KEYWORDS,
        'tool_flag': settings.TOOL_FLAG,
        'api_flag': settings.API_FLAG,
        'cnzz_protocol': settings.CNZZ_PROTOCOL,
        'beian': settings.BEIAN,
        'my_github': settings.MY_GITHUB,
        'site_verification': settings.MY_SITE_VERIFICATION,
        'site_url': site_full_url(),
        'hao_console': settings.HAO_CONSOLE
    }
'''

WSGI_APPLICATION = 'izone.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False  # 关闭国际时间，不然数据库报错


# 静态文件收集
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 媒体文件收集
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 统一分页设置
BASE_PAGE_BY = 10
BASE_ORPHANS = 5

# 全文搜索应用配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',  # 选择语言解析器为自己更换的结巴分词
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),   # 保存索引文件的地址，选择主目录下，这个会自动生成
    }
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


# blog.views 分页功能设置
# restframework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

# 配置数据库
MYSQL_HOST = os.getenv('IZONE_MYSQL_HOST', 'localhost')
MYSQL_NAME = os.getenv('IZONE_MYSQL_NAME', 'izone')
MYSQL_USER = os.getenv('IZONE_MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('IZONE_MYSQL_PASSWORD', 'YING123ZZ')
MYSQL_PORT = os.getenv('IZONE_MYSQL_PORT', 3306)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 修改数据库为MySQL，并进行配置
        'NAME': MYSQL_NAME,  # 数据库的名称
        'USER': MYSQL_USER,  # 数据库的用户名
        'PASSWORD': MYSQL_PASSWORD,  # 数据库的密码
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
        'OPTIONS': {'charset': 'utf8'}
    }
}


# 使用django-redis缓存页面，缓存配置如下：
REDIS_HOST = os.getenv('IZONE_REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('IZONE_REDIS_PORT', 6379)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}".format(REDIS_HOST, REDIS_PORT),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# 配置管理邮箱，服务出现故障会收到到邮件，环境变量值的格式：name|test@test.com 多组用户用英文逗号隔开
ADMINS = []
admin_email_user = os.getenv('IZONE_ADMIN_EMAIL_USER')
if admin_email_user:
    for each in admin_email_user.split(','):
        a_user, a_email = each.split('|')
        ADMINS.append((a_user, a_email))


# 邮箱配置
EMAIL_HOST = os.getenv('IZONE_EMAIL_HOST', 'smtp.163.com')
EMAIL_HOST_USER = os.getenv('IZONE_EMAIL_HOST_USER', 'your-email-address')
EMAIL_HOST_PASSWORD = os.getenv('IZONE_EMAIL_HOST_PASSWORD', 'your-email-password')  # 这个不是邮箱密码，而是授权码
EMAIL_PORT = os.getenv('IZONE_EMAIL_PORT', 465)  # 由于阿里云的25端口打不开，所以必须使用SSL然后改用465端口
EMAIL_TIMEOUT = 5
# 是否使用了SSL 或者TLS，为了用465端口，要使用这个
EMAIL_USE_SSL = os.getenv('IZONE_EMAIL_USE_SSL', 'True').upper() == 'TRUE'

# 默认发件人，不设置的话django默认使用的webmaster@localhost，所以要设置成自己可用的邮箱
DEFAULT_FROM_EMAIL = os.getenv('IZONE_DEFAULT_FROM_EMAIL', 'TendCode博客 <your-email-address>')



# 网站默认设置和上下文信息
SITE_LOGO_NAME = os.getenv('IZONE_LOGO_NAME', 'TendCode')
SITE_END_TITLE = os.getenv('IZONE_SITE_END_TITLE', 'izone')
SITE_DESCRIPTION = os.getenv('IZONE_SITE_DESCRIPTION', 'izone 是一个使用 Django+Bootstrap4 搭建的个人博客类型网站')
SITE_KEYWORDS = os.getenv('IZONE_SITE_KEYWORDS', 'izone, Django博客,个人博客')


# 个性化设置，非必要信息
# 个人 Github 地址
MY_GITHUB = os.getenv('IZONE_GITHUB', 'https://github.com/KissMyLady')
# 工信部备案信息
BEIAN = os.getenv('IZONE_BEIAN', '网站备案信息')
# 站长统计（友盟）
CNZZ_PROTOCOL = os.getenv('IZONE_CNZZ_PROTOCOL', '')
# 站长推送
MY_SITE_VERIFICATION = os.getenv('IZONE_SITE_VERIFICATION', '')
# 使用 http 还是 https （sitemap 中的链接可以体现出来）
PROTOCOL_HTTPS = os.getenv('IZONE_PROTOCOL_HTTPS', 'HTTP').lower()
# hao.tendcode.com
HAO_CONSOLE = {
    'flag': os.getenv('IZONE_HAO_FLAG', 'False').upper() == 'TRUE',
    'name': os.getenv('IZONE_HAO_NAME', '我的小姐姐'),
    'url': os.getenv('IZONE_HAO_URL', 'http://www.mylady.top')
}