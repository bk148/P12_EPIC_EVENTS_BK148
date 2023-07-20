from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission
from .models import StatusContract


class is_BasePermission(BasePermission):
    """
    Autorisation pour chaque catégorie d'utilisateur:
        - l'utilisateur ne peut créer un client/contrat/événement qu'en fonction de son autorisation ou
        accéder aux données les concernant
    """
    message = "accès refusé. Vous n'êtes pas autorisé à effectuer cette action"

    def has_permission(self, request, view):
        try:
            HTTP_METHODS = ['GET', 'POST']

            user_group = Group.objects.get(user=request.user)

            if str(user_group.name) == 'sales' and request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'support' and request.method == HTTP_METHODS[0]:
                return True
            if str(user_group.name) == 'management' and request.method == HTTP_METHODS[0]:
                return True
        except Exception as e:
            print(e)
        return False


class ContractPermission(is_BasePermission):
    """
    Autorisation pour chaque catégorie d'utilisateur:
        - l'utilisateur ne peut accéder ou modifier que les données qui le concernent
    """

    def has_object_permission(self, request, view, obj):
        try:
            HTTP_METHODS = ['GET', 'UPDATE', 'PATCH']
            user_group = Group.objects.get(user=request.user)
            print("perm", str(user_group.name), str(user_group.name) == 'management')
            contract_status = StatusContract.objects.get(contract=obj)
            if str(user_group.name) == 'sales' and contract_status.sales_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'support' and contract_status.support_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'management' and request.method in HTTP_METHODS:
                return True
        except KeyError:
            print("This group doesn't exists.")
        except Exception as e:
            print(e)
            self.message = " Accès refusé. Vous n'êtes pas autorisé à consulter ce contrat"
        return False


class ClientsPermission(is_BasePermission):
    message = "Accès refusé. Vous n'êtes pas autorisé à effectuer cette action"

    def has_object_permission(self, request, view, obj):

        try:
            HTTP_METHODS = ['GET', 'UPDATE', 'PATCH']
            user_group = Group.objects.get(user=request.user)
            contract_status = StatusContract.objects.get(contract__client=obj)

            if str(user_group.name) == 'sales' and contract_status.sales_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'support' and contract_status.support_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'management' and request.method in HTTP_METHODS:
                return True
        except Exception as e:
            print(e)
        self.message = "Accès refusé. Vous n'êtes pas autorisé à accéder à ce client"
        return False


class EventsPermission(is_BasePermission):
    message = "Accès refusé. Vous n'êtes pas autorisé à effectuer cette action"

    def has_object_permission(self, request, view, obj):
        try:
            HTTP_METHODS = ['GET', 'UPDATE', 'PATCH']
            user_group = Group.objects.get(user=request.user)
            contract_status = StatusContract.objects.get(contract=obj.contract)
            if str(user_group.name) == 'sales' and contract_status.sales_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'support' and contract_status.support_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'management' and request.method in HTTP_METHODS:
                return True
        except Exception as e:
            print(e)
        self.message = "Accès refusé. Vous n'êtes pas autorisé à accéder à cet event"
        return False
