from django.contrib import admin

from schedule.models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'get_invited_contacts')
    list_filter = ('start_time', 'end_time')  # Filtro por data
    search_fields = ('title', 'invited_contacts__first_name', 'invited_contacts__last_name')  # Busca por título ou contatos
    ordering = ('start_time',)

    # Mostrar os contatos convidados em uma linha (campo personalizado)
    def get_invited_contacts(self, obj):
        return ", ".join([str(contact) for contact in obj.invited_contacts.all()])
    get_invited_contacts.short_description = "Invited Contacts"

    # Exibir widgets mais amigáveis para campos de data/hora
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)  # Opcional para estilos
        }
        js = ('admin/js/custom_admin.js',)  # Opcional para scripts
