![alt tag](http://truetug.info/django-admin-helper.gif)

To install add 'admin_helper' to installed apps

    INSTALLED_APPS += (
        'admin_helper',
    )
    
Define suggest view using url notation
    
    ADMIN_HELPER_SUGGEST_VIEW = 'admin_helper:suggest_user'
    
Add middleware
    
    MIDDLEWARE_CLASSES += (
        'admin_helper.middleware.SuMiddleware',
        'admin_helper.middleware.CheckSuMiddleware',
    )
    
If you use default authentication backends, then add its import in the beginning of settings.py file and add authentication backend
    
    import django.conf.global_settings as DEFAULT_SETTINGS
        
    AUTHENTICATION_BACKENDS = DEFAULT_SETTINGS.AUTHENTICATION_BACKENDS + (
        'admin_helper.backends.SuAuthBackend',
    )
    
Or if AUTHENTICATION_BACKENDS already defined just add ours

    AUTHENTICATION_BACKENDS += (
        'admin_helper.backends.SuAuthBackend',
    )
    
Add urls

    urlpatterns = [
        ...
        url(r'^admin_helper/', include('admin_helper.urls', namespace='admin_helper')),
        ...
    ]

Add to template

    {% load admin_helper %}
    {% admin_helper %}
