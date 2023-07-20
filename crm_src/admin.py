from django.contrib import admin
from .models import Client, Contract, Event, StatusContract


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'email', 'prospect')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'signed', 'amount')


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_event')


class StatusContractAdmin(admin.ModelAdmin):
    list_display = ('get_contract', 'get_contract_status', 'sales_contact', 'support_contact')

    def obetnir_contrat(self, obj):
        return obj.contract.client.email

    def obtenir_status_contrat(self, obj):
        return obj.contract.signed

    obetnir_contrat().short_description = 'contract'  # Renames column head


admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(StatusContract, StatusContractAdmin)
