
from django.conf.urls.static import static
from django.urls import path, include

from mriya import settings
from my_account.views import ProfileView

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile', ProfileView.as_view(), name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
