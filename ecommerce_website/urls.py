from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from account.views import ProfileRegisterView
from shop import views as shop_views

account_router = DefaultRouter()
account_router.register('register', ProfileRegisterView)

shop_router = DefaultRouter()
shop_router.register('category', shop_views.CategoryViewSet)

oreder_router = DefaultRouter()
oreder_router.register('order', shop_views.OrderListCreateAPIView)


schema_view = get_schema_view(
   openapi.Info(
      title="Ecommerce API",
      default_version='v0.1',
      description="API для интернет магазина",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/token/', obtain_auth_token),

    path('api/account/', include(account_router.urls)),

    path('api/shop/', include(shop_router.urls)),
    path('api/shop/category/<int:category_id>/item/', shop_views.ItemListCreateAPIView.as_view()),
    path('api/shop/category/<int:category_id>/item/<int:pk>/', shop_views.ItemRetrieveUpdateDestroyAPIView.as_view()),

    path('api/order/', include(shop_router.urls)),
    path('api/shop/category/<int:category_id>/item/<int:item_id>/order/', shop_views.OrderListCreateAPIView.as_view()),
    path('api/shop/category/<int:category_id>/item/<int:item_id>/order/<int:pk>/',
         shop_views.OrderRetrieveDestroyUpdateAPIView.as_view()),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_ui'),
    path('json_doc/', schema_view.without_ui(cache_timeout=0), name='json_doc'),
]

#
# urlpatterns = [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#    ...
