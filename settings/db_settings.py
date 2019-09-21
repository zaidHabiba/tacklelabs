import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES_List = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    , 'host': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wsgi',
        'USER': 'ZaidXHub@wsgi',
        'PASSWORD': 'iwue#$%#%46815*@@FVnwejifnjklfwefwe',
        'HOST': 'wsgi.mysql.database.azure.com',
        'PORT': '3306',
    }
}
DATABASES = {'default': DATABASES_List['default']}
