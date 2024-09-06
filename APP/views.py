from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Usuario, Baba, Pedido, Avaliacao, Localizacao
from .serializers import UsuarioSerializer, BabaSerializer, PedidoSerializer, AvaliacaoSerializer, LocalizacaoSerializer
from django.http import HttpResponse
from .models import API

def index(request):
    apis = API.objects.all()
    return render(request, 'index.html', {'apis': apis})


# views resposnavel pelos usuarios
class UsuarioApiView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Retorna uma lista de usuarios.
        """
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Cria um novo usuario.
        """
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def cadastro(self, request):
        """
        Cria um novo usuário.
        """
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        """
        Autentica um usuário.
        """
        email = request.data.get('email')
        senha = request.data.get('senha')

        if not email or not senha:
            return Response({'erro': 'Email e senha são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

        usuario = authenticate(email=email, password=senha)
        if usuario is not None:
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
class UsuarioDetailApiView(APIView):
    def get_object(self, pk):
        """
        Obtém um usuário específico.
        """
        try:
            return Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        """
        Retorna os detalhes de um usuário específico.
        """
        usuario = self.get_object(pk)
        if usuario is None:
            return Response({'erro': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """
        Atualiza um usuário específico.
        """
        usuario = self.get_object(pk)
        if usuario is None:
            return Response({'erro': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Deleta um usuário específico.
        """
        usuario = self.get_object(pk)
        if usuario is None:
            return Response({'erro': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    # views responsavel pelas babas
class BabaApiView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Retorna uma lista de babas.
        """
        babas = Baba.objects.all()
        serializer = BabaSerializer(babas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Cria uma nova baba.
        """
        serializer = BabaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        """
        Autentica uma baba.
        """
        email = request.data.get('email')
        senha = request.data.get('senha')

        if not email or not senha:
            return Response({'erro': 'Email e senha são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.tipo_usuario == 'baba':
                baba = Baba.objects.get(usuario=usuario)
                if baba and baba.usuario.senha == senha:
                    serializer = BabaSerializer(baba)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'erro': 'Credenciais inválidas ou não é uma babá'}, status=status.HTTP_401_UNAUTHORIZED)
        except Usuario.DoesNotExist:
            return Response({'erro': 'Usuario nao encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Baba.DoesNotExist:
            return Response({'erro': 'Baba nao encontrada'}, status=status.HTTP_404_NOT_FOUND)

    def cadastro(self, request):
        """
        Cria uma nova baba.
        """
        serializer = BabaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UsuarioProfileApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retorna o perfil do usuário autenticado.
        """
        usuario = request.user
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Atualiza o perfil do usuário autenticado.
        """
        usuario = request.user
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BabaDetailApiView(APIView):
    def get_object(self, pk):
        """
        Obtém uma babá específica.
        """
        try:
            return Baba.objects.get(pk=pk)
        except Baba.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        """
        Retorna os detalhes de uma babá específica.
        """
        baba = self.get_object(pk)
        if baba is None:
            return Response({'erro': 'Babá não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BabaSerializer(baba)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """
        Atualiza uma babá específica.
        """
        baba = self.get_object(pk)
        if baba is None:
            return Response({'erro': 'Babá não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BabaSerializer(baba, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Deleta uma babá específica.
        """
        baba = self.get_object(pk)
        if baba is None:
            return Response({'erro': 'Babá não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        baba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BabaProfileApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retorna o perfil da baba autenticada.
        """
        usuario = request.user
        try:
            baba = Baba.objects.get(usuario=usuario)
        except Baba.DoesNotExist:
            return Response({'erro': 'Babá não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BabaSerializer(baba)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Atualiza o perfil da baba autenticada.
        """
        usuario = request.user
        try:
            baba = Baba.objects.get(usuario=usuario)
        except Baba.DoesNotExist:
            return Response({'erro': 'Babá não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BabaSerializer(baba, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# viwes responsavel pelos pedidos
class PedidoApiView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Retorna uma lista de pedidos.
        """
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Cria um novo pedido.
        """
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PedidoDetailApiView(APIView):
    def get_object(self, pk):
        """
        Obtém um pedido específico.
        """
        try:
            return Pedido.objects.get(pk=pk)
        except Pedido.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        """
        Retorna os detalhes de um pedido específico.
        """
        pedido = self.get_object(pk)
        if pedido is None:
            return Response({'erro': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """
        Atualiza um pedido específico.
        """
        pedido = self.get_object(pk)
        if pedido is None:
            return Response({'erro': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PedidoSerializer(pedido, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Deleta um pedido específico.
        """
        pedido = self.get_object(pk)
        if pedido is None:
            return Response({'erro': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        pedido.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# viwes resposnavel pela avaliacao
class AvaliacaoApiView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Retorna uma lista de avaliações.
        """
        avaliacoes = Avaliacao.objects.all()
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Cria uma nova avaliação.
        """
        serializer = AvaliacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AvaliacaoDetailApiView(APIView):
    def get_object(self, pk):
        """
        Obtém uma avaliação específica.
        """
        try:
            return Avaliacao.objects.get(pk=pk)
        except Avaliacao.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        """
        Retorna os detalhes de uma avaliação específica.
        """
        avaliacao = self.get_object(pk)
        if avaliacao is None:
            return Response({'erro': 'Avaliação não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AvaliacaoSerializer(avaliacao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """
        Atualiza uma avaliação específica.
        """
        avaliacao = self.get_object(pk)
        if avaliacao is None:
            return Response({'erro': 'Avaliação não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AvaliacaoSerializer(avaliacao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Deleta uma avaliação específica.
        """
        avaliacao = self.get_object(pk)
        if avaliacao is None:
            return Response({'erro': 'Avaliação não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        avaliacao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# views resposvel pela localizacao
class LocalizacaoApiView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Retorna uma lista de localizações.
        """
        localizacoes = Localizacao.objects.all()
        serializer = LocalizacaoSerializer(localizacoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Cria uma nova localização.
        """
        serializer = LocalizacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LocalizacaoDetailApiView(APIView):
    def get_object(self, pk):
        """
        Obtém uma localização específica.
        """
        try:
            return Localizacao.objects.get(pk=pk)
        except Localizacao.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        """
        Retorna os detalhes de uma localização específica.
        """
        localizacao = self.get_object(pk)
        if localizacao is None:
            return Response({'erro': 'Localização não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LocalizacaoSerializer(localizacao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """
        Atualiza uma localização específica.
        """
        localizacao = self.get_object(pk)
        if localizacao is None:
            return Response({'erro': 'Localização não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LocalizacaoSerializer(localizacao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Deleta uma localização específica.
        """
        localizacao = self.get_object(pk)
        if localizacao is None:
            return Response({'erro': 'Localização não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        localizacao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)