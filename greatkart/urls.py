"""greatkart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

# URL cho xử lý chuyển ngôn ngữ (bắt buộc giữ bên ngoài)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Các URL chính nằm trong i18n_patterns để hoạt động với /ja/, /en/
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('orders/', include('orders.urls')),
)

# Phục vụ file media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

