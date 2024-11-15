from django.urls import path
from django.conf.urls.static import static
from dreams.views import (
    DreamsListView,
    DreamsDetailView,
    DreamsCreateView,
    DreamUpdateView,
    DreamsDeleteView,
    TagAutocomplete,
    DreamsSearchView,
    upload_image,
    DreamsDonatetView,
    TermsOfServiceView,
    PrivatePolycyView, HomePageView
)
from mriya import settings

urlpatterns = [

    path("", HomePageView.as_view()),
    path("private_polycy", PrivatePolycyView.as_view(), name="private_polycy"),
    path("terms_of_service", TermsOfServiceView.as_view(), name="terms_of_service"),
    path("dream", DreamsListView.as_view(), name="dream_list"),
    path("dream/search", DreamsSearchView.as_view(), name="dream_search"),
    path("dream/create", DreamsCreateView.as_view(), name="dream_create"),
    path("dream/<int:id>", DreamsDetailView.as_view(), name="dream_detail"),
    path("dream/<int:id>/update", DreamUpdateView.as_view(), name="dream_update"),
    path("dream/<int:id>/delete", DreamsDeleteView.as_view(), name="dream_delete"),
    path("dream/<int:id>/donate", DreamsDonatetView.as_view(), name="dream_donate"),
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete'),
    path('upload_image/', upload_image, name='upload_image'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

