import os
from django.core.exceptions import ValidationError

def validar_imagem(foto):
    # 1. Tamanho máximo (ex.: 5 MB)
    max_size = 5 * 1024 * 1024
    if foto.size > max_size:
        raise ValidationError("A imagem deve ter no máximo 5MB.")

    # 2. Extensões permitidas
    ext_permitidas = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(foto.name)[1].lower()

    if ext not in ext_permitidas:
        raise ValidationError("A imagem deve ser JPG ou PNG.")

    # 3. Sanitizar nome do arquivo
    foto.name = foto.name.replace(" ", "_")
