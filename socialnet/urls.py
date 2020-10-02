from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url="/account/")),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("images/", include("images.urls", namespace="images")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),