from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Cidadao, Noticia, Evento, Ficheiro, Questionario, Pergunta, Opcao, Mensagem, Ocorrencia, Requerimento, Servico


class CidadaoInline(admin.StackedInline):
    model = Cidadao
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (CidadaoInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class NoticiaAdmin(admin.ModelAdmin):
    list_display = ("titulo", 'data_insercao')


class FicheiroAdmin(admin.ModelAdmin):
    list_display = ("titulo", 'data_insercao', 'tipo')


class EventoAdmin(admin.ModelAdmin):
    list_display = ("titulo", 'data_evento', 'data_insercao')


class QuestionarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_insercao')


class OpcaoAdmin(admin.TabularInline):
    model = Opcao
    extra = 2


class PerguntaAdmin(admin.ModelAdmin):
    inlines = (OpcaoAdmin, )
    list_display = ('titulo', 'data_insercao', 'ativo')


class MensagemAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    list_display = ('remetente', 'assunto', 'data_insercao')


class OcorrenciaAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    list_display = ('utilizador', 'categoria', 'local', 'data_insercao')


class RequerimentoAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    list_display = ('utilizador', 'servico', 'estado', 'data_req')


class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Ficheiro, FicheiroAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Questionario, QuestionarioAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Mensagem, MensagemAdmin)
admin.site.register(Ocorrencia, OcorrenciaAdmin)
admin.site.register(Requerimento, RequerimentoAdmin)
admin.site.register(Servico, ServicoAdmin)




