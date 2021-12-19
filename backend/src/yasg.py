from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Records API",
        default_version='v1',
        description=_("API Documentation for FoodGram project"),
        terms_of_service="https://github.com/reakfog/foodgram-project-react",
        contact=openapi.Contact(email="evgeny_perchun@mail.ru"),
        license=openapi.License(name="BSD 3-Clause License",),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
