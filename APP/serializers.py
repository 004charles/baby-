from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario, Baba, Pedido, Avaliacao, Localizacao

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'pais', 'tipo_usuario', 'data_criacao', 'ultima_atualizacao']
    
    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return value
    
    def create(self, validated_data):
        senha = validated_data.pop('senha', None)
        usuario = Usuario.objects.create(**validated_data)
        if senha:
            usuario.senha = make_password(senha)
            usuario.save()
        return usuario

class BabaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baba
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'


class LocalizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizacao
        fields = '__all__'
