from django.contrib import admin
from .models import Usuario, Baba, Pedido, Avaliacao, Localizacao, API

admin.site.register(API)

# Registro do model Usuario no admin
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'cidade', 'pais', 'tipo_usuario', 'data_criacao']
    search_fields = ['nome', 'email']
    list_filter = ['cidade', 'estado', 'pais', 'tipo_usuario']
    ordering = ['data_criacao']

# Registro do model Baba no admin
@admin.register(Baba)
class BabaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'experiencia', 'preco_hora', 'avaliacao_media', 'disponibilidade', 'data_criacao']
    search_fields = ['user__nome', 'user__email']
    list_filter = ['disponibilidade', 'preco_hora']
    ordering = ['data_criacao']

# Registro do model Pedido no admin
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'babysitter', 'status', 'data_hora_inicio', 'data_hora_fim', 'preco_total', 'data_criacao']
    search_fields = ['cliente__nome', 'babysitter__user__nome']
    list_filter = ['status', 'data_hora_inicio', 'data_hora_fim']
    ordering = ['data_criacao']

# Registro do model Avaliacao no admin
@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'babysitter', 'avaliacao', 'data_criacao']
    search_fields = ['cliente__nome', 'babysitter__user__nome']
    list_filter = ['avaliacao']
    ordering = ['data_criacao']

# Registro do model Localizacao no admin
@admin.register(Localizacao)
class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'latitude', 'longitude', 'cidade', 'estado', 'pais', 'data_criacao']
    search_fields = ['usuario__nome', 'cidade', 'estado', 'pais']
    list_filter = ['cidade', 'estado', 'pais']
    ordering = ['data_criacao']

