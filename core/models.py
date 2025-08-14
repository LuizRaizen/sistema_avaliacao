from django.db import models

class Avaliacao(models.Model):
    """Uma avaliação no site."""
    nome = models.CharField(max_length=100)
    nota = models.IntegerField()
    comentario = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return f"{self.nome} - Nota: {self.nota}"
