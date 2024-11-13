
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from mriya import settings
from my_account.views import ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path("", include("dreams.urls")),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', ProfileView.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
