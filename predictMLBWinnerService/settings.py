import os

INSTALLED_APPS = [
    'predictMLBWinnerService',
    'django.contrib.contenttypes',
    'django.contrib.auth',
]
ROOT_URLCONF = 'predictMLBWinnerService.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mlb',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEBUG = True
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # 指定模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 模板文件夾的路徑列表
        'APP_DIRS': False,  # 是否在應用程序目錄中查找模板
        'OPTIONS': {
            'context_processors': [  # 上下文處理器列表
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True,  # 啟用模板調試模式
            'loaders': [  # 自定義模板加載器
                ('django.template.loaders.filesystem.Loader', [os.path.join(BASE_DIR, 'templates')]),
                'django.template.loaders.app_directories.Loader',
            ],
            'string_if_invalid': 'Invalid variable: %s',  # 無效變量的顯示格式
        },
    },


SECRET_KEY = 'django'
