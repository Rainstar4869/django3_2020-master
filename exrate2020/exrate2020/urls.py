from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from nichiei.views import ContactView
import debug_toolbar


handler500 = 'authentication.views.error_500'

urlpatterns = [
    path('i18n/', include("django.conf.urls.i18n")),
    path('__debug__/', include(debug_toolbar.urls)),
    path("", TemplateView.as_view(template_name="nichiei/index.html"), name="top"),
    path("company/", TemplateView.as_view(template_name="nichiei/company.html"), name="company"),
    path("services/", TemplateView.as_view(template_name="nichiei/services.html"), name="services"),
    path("contact/", ContactView.as_view(), name="contact"),

    path('admin/', admin.site.urls),
    path("apiauth/", include("authentication.urls")),
    path("webauth/", include("web_auth.urls")),
    path('accounts/', include('allauth.urls')),

    path('back/store/', include('store.urls')),
    path('chat/', include('chat.urls')),

    path('qr_code/', include('qr_code.urls', namespace="qr_code")),

]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
