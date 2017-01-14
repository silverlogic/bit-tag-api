from django.conf.urls import include, url

from .v1.urls import router as v1_router

urlpatterns = [
    url(r'v1/', include(v1_router.urls, namespace='v1')),
]
