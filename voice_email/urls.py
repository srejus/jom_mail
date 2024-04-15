from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('mail/',include('mail.urls')),
    path('',include('home.urls')),

    # path('ckeditor/', include('ckeditor.urls')),
]
