from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'pycart.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('products.urls')),
    
    #url(r'cart/$',"products.views.show_cart",name="show_cart"),

    url(r'^cart/(?P<id>\d+)/$', 'cart.views.remove_from_cart', name='remove_from_cart'),
    url(r'^cart/(?P<slug>[\w-]+)/$', 'cart.views.add_to_cart', name='add_to_cart'),
    url(r'^cart/$', 'cart.views.view', name='cart'),
    url(r'^place_order/$', 'order.views.place_order', name='place_order'),
    url(r'^orders/$', 'order.views.orders', name='client_orders'),
    url(r'^search/$', 'products.views.search', name='search'),
     url(r'^logout/$', 'account.views.Logout', name='Logout'),
    url(r'^login/$', 'account.views.Login', name='login'),
    url(r'^register/$', 'account.views.registration_view', name='register'),
    url(r'^account/activate/(?P<activation_key>\w+)/$', 'account.views.activation_view', name='activation_view'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



handler404 = '.views.file_not_found_404'