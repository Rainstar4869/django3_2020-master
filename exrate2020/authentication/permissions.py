from rest_framework import permissions
from rolepermissions.checkers import has_role
from exrate2020.roles import Distributor


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsDistributor(permissions.BasePermission):
    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        if has_role(request.user, Distributor):
            return True

        return False
