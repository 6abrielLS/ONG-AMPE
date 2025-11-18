from django.db import models
from .validators import validar_imagem
from django.core.validators import RegexValidator

# -----------------------------
#           PET
# -----------------------------
class Pet(models.Model):

    class Sexo(models.TextChoices):
        FEMININO = 'F', 'Feminino'
        MASCULINO = 'M', 'Masculino'

    class CategoriaPet(models.TextChoices):
        CACHORRO = 'C', 'Cachorro'
        GATO = 'G', 'Gato'

    class Idade(models.TextChoices):
        FILHOTE = 'FILHOTE', 'Filhote'
        ADULTO = 'ADULTO', 'Adulto'

    class Porte(models.TextChoices):
        PEQUENO = 'P', 'Pequeno'
        MEDIO = 'M', 'Médio'
        GRANDE = 'G', 'Grande'

    class IsCastrado(models.TextChoices):
        CASTRADO = 'C', 'Castrado'
        NAO_CASTRADO = 'NC', 'Não Castrado'

    class IsCondicaoEspecial(models.TextChoices):
        SIM = 'S', 'Sim'
        NAO = 'N', 'Não'

    nome = models.CharField(max_length=30, 
                            blank=False,
                            validators=[RegexValidator(r'^[A-Za-zÀ-ÿ ]+$', 
                                        "Nome deve conter apenas letras")])
    
    coloracao = models.CharField(max_length=20, 
                                 blank=False,
                                 validators=[RegexValidator(r'^[A-Za-zÀ-ÿ ]+$', 
                                             "Cor deve conter apenas letras")])
    
    descricao = models.CharField(max_length=255, blank=False)

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
        upload_to="img_pets/",
        validators=[validar_imagem],
        blank=True,
        null=True
    )

    is_condicao_especial = models.CharField(
        max_length=1,
        choices=IsCondicaoEspecial.choices,
        default=IsCondicaoEspecial.NAO,
    )

    def __str__(self):
        return f"{self.nome} ({self.get_categoria_pet_display()})"


# -----------------------------
#        ADOTANTE
# -----------------------------
class Adotante(models.Model):
    nome = models.CharField(max_length=30)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='O CPF deve conter apenas números (11 dígitos).'
            )
        ]
    )
    
    def __str__(self):
        return f"{self.nome} - {self.cpf}"


# -----------------------------
#       VOLUNTÁRIOS
# -----------------------------
class Voluntario(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


# -----------------------------
#          ADOÇÃO
# -----------------------------
class Adocao(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.PROTECT,
        related_name="adocoes"
    )

    adotante = models.ForeignKey(
        Adotante,
        on_delete=models.PROTECT,
        related_name="adocoes"
    )

    voluntario = models.ForeignKey(
        Voluntario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="adocoes"
    )

    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adoção de {self.pet.nome} por {self.adotante.nome}"
