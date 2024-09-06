from django.urls import path
from .views import (
    UsuarioApiView, UsuarioDetailApiView,
    BabaApiView, BabaDetailApiView,
    PedidoApiView, PedidoDetailApiView,
    AvaliacaoApiView, AvaliacaoDetailApiView,
    LocalizacaoApiView, LocalizacaoDetailApiView
)


from .views import  UsuarioProfileApiView, BabaProfileApiView

urlpatterns = [
    
    path('usuarios/', UsuarioApiView.as_view(), name='usuario-list'),
    path('usuarios/<int:pk>/', UsuarioDetailApiView.as_view(), name='usuario-detail'),

    path('perfil/usuario/', UsuarioProfileApiView.as_view(), name='perfil_usuario'),
    path('perfil/baba/', BabaProfileApiView.as_view(), name='perfil_baba'),

   
    path('babas/', BabaApiView.as_view(), name='baba-list'),
    path('babas/<int:pk>/', BabaDetailApiView.as_view(), name='baba-detail'),

    
    path('pedidos/', PedidoApiView.as_view(), name='pedido-list'),
    path('pedidos/<int:pk>/', PedidoDetailApiView.as_view(), name='pedido-detail'),

    
    path('avaliacoes/', AvaliacaoApiView.as_view(), name='avaliacao-list'),
    path('avaliacoes/<int:pk>/', AvaliacaoDetailApiView.as_view(), name='avaliacao-detail'),

    
    path('localizacoes/', LocalizacaoApiView.as_view(), name='localizacao-list'),
    path('localizacoes/<int:pk>/', LocalizacaoDetailApiView.as_view(), name='localizacao-detail'),
]
