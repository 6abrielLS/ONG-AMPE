from django.contrib import admin
# Importando TODOS os models que criamos
from .models import (
    Pet, 
    FotoPet, 
    Adotante, 
    Voluntario, 
    Adocao, 
    DocumentoTransparencia
)


class FotoPetInline(admin.TabularInline):
    model = FotoPet
    extra = 1  


class PetAdmin(admin.ModelAdmin):
  
    list_display = ('nome', 'categoria_pet', 'sexo', 'porte', 'is_castrado', 'is_adotado')
    
    # Filtros na barra lateral direita
    list_filter = ('categoria_pet', 'sexo', 'porte', 'is_adotado', 'is_castrado')
    
    # Barra de pesquisa (Busca por nome ou descrição)
    search_fields = ('nome', 'descricao')
    
    # editar o status de adoção direto na lista 
    list_editable = ('is_adotado',)
    
    inlines = [FotoPetInline]
    
    # Paginação (se tiver muitos animais)
    list_per_page = 20


class AdotanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf')
    search_fields = ('nome', 'cpf')


class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


class AdocaoAdmin(admin.ModelAdmin):
    list_display = ('pet', 'adotante', 'voluntario', 'data')
    list_filter = ('data',)
    
    # O Django usa "__" para buscar dentro de outra tabela
    # buscama pelo NOME do Pet e pelo NOME do Adotante
    search_fields = ('pet__nome', 'adotante__nome', 'adotante__cpf')
    
    # Mostra a data de cadastro automaticamente, mas como leitura
    readonly_fields = ('data',)


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'data_publicacao')
    list_filter = ('categoria', 'data_publicacao') # Cria filtro lateral por data e tipo
    search_fields = ('titulo',)
    
    # Adiciona textos de ajuda na tela
    fieldsets = (
        ('Informações do Arquivo', {
            'fields': ('titulo', 'categoria', 'arquivo')
        }),
        ('Data', {
            'fields': ('data_publicacao',),
            'description': 'A data serve para organizar o arquivo na listagem mensal/anual.'
        }),
    )

admin.site.register(Pet, PetAdmin)
# admin.site.register(FotoPet) # Não precisa registrar separado, já está dentro de Pet
admin.site.register(Adotante, AdotanteAdmin)
admin.site.register(Voluntario, VoluntarioAdmin)
admin.site.register(Adocao, AdocaoAdmin)
admin.site.register(DocumentoTransparencia, DocumentoAdmin)
