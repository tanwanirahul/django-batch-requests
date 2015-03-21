def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': ':memory:'}},
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'tests',
            'batch_requests',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        BATCH_REQUESTS = {
            "HEADERS_TO_INCLUDE": ["HTTP_USER_AGENT", "HTTP_COOKIE"],
            "DEFAULT_CONTENT_TYPE": "application/xml",
            "USE_HTTPS": True,
            "MAX_LIMIT": 3
        }
    )
    try:
        import django
        django.setup()
    except AttributeError:
        pass
