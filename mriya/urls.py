import debug_toolbar
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from mriya import settings
from my_account.views import ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path("", include("dreams.urls")),
    path('accounts/', include('my_account.urls')),
    path('accounts/profile/', ProfileView.as_view()),
]+ debug_toolbar_urls()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
