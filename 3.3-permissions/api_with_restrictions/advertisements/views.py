from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.decorators import action

from .models import Advertisement, FavoritesAdvertisements
from .serializers import AdvertisementSerializer, FavoritesAdvertisementsSerializer
from .filters import AdvertisementFilter
from .permission import IsOwnerOrReadOnlyPermission


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = AdvertisementFilter

    def list(self, request, *args, **kwargs):
        filter_queryset = []
        for adv in Advertisement.objects.all():
            if (adv.draft is False) or adv.creator == request.user:
                filter_queryset.append(adv)
        serializer = AdvertisementSerializer(filter_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_to_favorites(self, request, pk=None):
        if request.data.get('creator') is not None and self.request.user.id == request.data.get('creator').get('id'):
            return Response({'Свои объявления нельзя добавлять в избранное.'})
        if len(FavoritesAdvertisements.objects.filter(user=request.user, advertisement=pk)) == 0:
            favorite = FavoritesAdvertisements.objects.create(user=request.user, advertisement=self.get_object())
            serializer = FavoritesAdvertisementsSerializer(favorite)
            return Response(serializer.data)
        else:
            Response({'Уже добавлено'})

    def get_permissions(self):
        """Получение прав для действий."""
        if self.request.user.is_staff:
            return [IsAdminUser()]
        if self.action in ["create", "add_to_favorites"]:
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnlyPermission()]
        return []


class FavoritesAdvertisementsViewSet(ModelViewSet):
    queryset = FavoritesAdvertisements.objects.all()
    serializer_class = FavoritesAdvertisementsSerializer

    def list(self, request, *args, **kwargs):
        queryset = FavoritesAdvertisements.objects.filter(user=request.user)
        serializer = FavoritesAdvertisementsSerializer(queryset, many=True)
        return Response(serializer.data)
