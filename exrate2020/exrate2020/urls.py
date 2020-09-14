
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import permissions
from upload.views import image_upload
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="INCOME EXPENSES API",
#         default_version='v1',
#         description="Test description",
#         terms_of_service="https://www.ourapp.com/policies/terms/",
#         contact=openapi.Contact(email="contact@expenses.local"),
#         license=openapi.License(name="Test License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="top"),
    # path("upload/", image_upload, name="upload"),
    path('admin/', admin.site.urls),
    path("apiauth/", include("authentication.urls")),
    path("webauth/", include("web_auth.urls")),
    path('accounts/', include('allauth.urls')),
    path('expenses/', include('expenses.urls')),
    path('incomes/', include('income.urls')),
    path('userstats/', include('userstats.urls')),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
