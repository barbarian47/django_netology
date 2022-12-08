from rest_framework.routers import DefaultRouter

from .views import AdvertisementViewSet, FavoritesAdvertisementsViewSet

router = DefaultRouter()
router.register('advertisements', AdvertisementViewSet)
router.register('favorites_advertisements', FavoritesAdvertisementsViewSet)

urlpatterns = router.urls