from django.db import models

class Pet(models.Model):

    class Sexo(models.TextChoices):
        FEMINIMO = 'F'
        MASCULINO = 'M'

    class CategoriaPet(models.TextChoices):
        CACHORRO = 'C'
        GATO = 'G'

    class Idade(models.TextChoices):
        FILHOTE = 'FILHOTE'
        ADULTO = 'ADULTO'

    class Porte(models.TextChoices):
        PEQUENO = 'P'
        MEDIO = 'M'
        GRANDE = 'G'
    
    class IsCastrado(models.TextChoices):
        CASTRADO = 'C'
        NAO_CASTRADO = 'NC'

    class IsCondicaoEspecial(models.TextChoices):
        SIM = 'S'
        NAO = 'N'

    sexo = models.CharField(
        max_length=1,
        choices=Sexo.choices,
        default=Sexo.MASCULINO,
    )

    categoria_pet = models.CharField(
        max_length=1,
        choices=CategoriaPet.choices,
        default=CategoriaPet.CACHORRO,
    )

    idade = models.CharField(
        max_length=8,
        choices=Idade.choices,
        default=Idade.ADULTO,
    )

    porte = models.CharField(
        max_length=1,
        choices=Porte.choices,
        default=Porte.MEDIO,
    )

    is_castrado = models.CharField(
        max_length=2,
        choices=IsCastrado.choices,
        default=IsCastrado.CASTRADO,
    )

    fotos_pet = models.ImageField(
        upload_to="OngAmpaSite/OngAmp/static/img_pets",
        height_field=1280, 
        width_field=960, 
        max_length=100, 
    )
    
    is_condicao_especial = models.CharField(
        max_length=1,
        choices=IsCondicaoEspecial.choices,
        choices=IsCondicaoEspecial.NAO,
    )
    
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=255)
    cor = models.CharField(max_length=20)
