from django.db import models


class API(models.Model):
    nome = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    senha = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    tipo_usuario = models.CharField(max_length=50, choices=[('cliente', 'Cliente'), ('baba', 'Babá')])
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Baba(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    biografia = models.TextField()
    experiencia = models.IntegerField()
    preco_hora = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    avaliacao_media = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    disponibilidade = models.CharField(max_length=50, choices=[('disponivel', 'Disponível'), ('ocupada', 'Ocupada'), ('fora_de_servico', 'Fora de Serviço')])
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.nome} - {self.preco_hora} por hora'


class Pedido(models.Model):
    cliente = models.ForeignKey(Usuario, related_name='pedidos_cliente', on_delete=models.CASCADE)
    babysitter = models.ForeignKey(Baba, related_name='pedidos_babysitter', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pendente', 'Pendente'), ('aceito', 'Aceito'), ('rejeitado', 'Rejeitado'), ('concluido', 'Concluído')])
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Pedido de {self.cliente.nome} para {self.babysitter.user.nome}'


class Avaliacao(models.Model):
    cliente = models.ForeignKey(Usuario, related_name='avaliacoes_cliente', on_delete=models.CASCADE)
    babysitter = models.ForeignKey(Baba, related_name='avaliacoes_babysitter', on_delete=models.CASCADE)
    avaliacao = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentarios = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cliente', 'babysitter'], name='unique_avaliacao_cliente_babysitter')
        ]

    def __str__(self):
        return f'{self.cliente.nome} avaliou {self.babysitter.user.nome}'

class Localizacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    endereco_completo = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Localização de {self.usuario.nome}'
