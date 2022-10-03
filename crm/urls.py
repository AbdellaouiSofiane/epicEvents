from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet, ContractViewSet, EventViewSet


router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'contracts', ContractViewSet, basename='contracts')
router.register(r'events', EventViewSet, basename='events')
urlpatterns = router.urls
