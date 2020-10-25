from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from .serializers import ShippingAddressSerializer
from .models import ShippingAddress
import logging
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLevelName("error_logger")


class ShippingAddressViewSet(GenericViewSet):
    serializer_class = ShippingAddressSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        addressbook = ShippingAddress.objects.filter(user=self.request.user)
        addressbook_serializer = self.serializer_class(instance=addressbook, many=True)
        if addressbook.exists():
            return Response({
                "result": "OK",
                "operation": "list",
                "addressbook": addressbook_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "result": "NG",
            "operation": "list",
            "addressbook": []
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            address = ShippingAddress.objects.get(pk=pk, user=self.request.user)
            address.delete()
            return Response({
                "result": "OK",
                "operation": "destroy",
                "message": "successfully deleted!",
                "id": pk
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({
                "result": "NG",
                "operation": "destroy",
                "message": "record doesn't exists!",
                "id": pk
            }, status=status.HTTP_200_OK)
