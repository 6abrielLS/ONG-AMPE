from django.shortcuts import render, get_object_or_404
from .models import DocumentoTransparencia
from .models import Pet
from .forms import CadastroAdotanteForm
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    return render(request, 'index.html')


def sobre(request):
    return render(request, 'sobre.html')


def contato(request):
    return render(request, 'contato.html')


# 1. Página "Capa" (Só visual + Botão)
def transp(request):
    return render(request, 'transparencia.html')


# 2. Página "Arquivo" (Com filtros)
def prestacao_contas(request):
    # --- LÓGICA DE FILTRO ---
    # Pegamos o que veio na URL (ex: ?ano=2025&mes=3)
    ano_filtro = request.GET.get('ano')
    mes_filtro = request.GET.get('mes')

    # Base dos documentos mensais
    docs_mensais = DocumentoTransparencia.objects.filter(categoria='MENSAL')

    # Se escolheu ano, filtra
    if ano_filtro:
        docs_mensais = docs_mensais.filter(data_publicacao__year=ano_filtro)
    
    # Se escolheu mês, filtra
    if mes_filtro:
        docs_mensais = docs_mensais.filter(data_publicacao__month=mes_filtro)

    # Ordena do mais recente para o mais antigo
    docs_mensais = docs_mensais.order_by('-data_publicacao')

    # Documentos anuais (geralmente não precisam de filtro de mês)
    docs_anuais = DocumentoTransparencia.objects.filter(categoria='ANUAL').order_by('-data_publicacao')

    # --- PARA POPULAR O SELECT DO HTML ---
    # Pega todos os anos disponíveis no banco para montar o <select>
    anos_disponiveis = DocumentoTransparencia.objects.dates('data_publicacao', 'year', order='DESC')

    return render(request, 'prestacao_contas.html', {
        'docs_mensais': docs_mensais,
        'docs_anuais': docs_anuais,
        'anos_disponiveis': anos_disponiveis,
        'ano_selecionado': ano_filtro, # Para manter o select marcado
        'mes_selecionado': mes_filtro,
    })


def lista_pets(request):
    # Busca apenas quem NÃO foi adotado
    # O 'prefetch_related' serve para carregar as fotos junto e não travar o site
    pets = Pet.objects.filter(is_adotado=False).prefetch_related('fotos')
    
    return render(request, 'adote.html', {'pets': pets})


def detalhes_pet(request, pet_id):
    # Busca o pet pelo ID. Se não existir (ex: ID 999), dá erro 404 automaticamente.
    pet = get_object_or_404(Pet, pk=pet_id)
    
    return render(request, 'detalhes_pet.html', {'pet': pet})


def cadastro_adotante(request, pet_id=None):
    pet_interesse = None
    
    # Se veio com ID na URL, busca o pet para mostrar no formulário/email
    if pet_id:
        pet_interesse = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = CadastroAdotanteForm(request.POST)
        if form.is_valid():
            # 1. Salva no Banco de Dados
            adotante = form.save()
            
            # 2. Monta o E-mail de Alerta
            assunto = f'Novo Interessado: {adotante.nome}'
            mensagem = f"""
            Olá equipe AMPA,
            
            Uma nova pessoa preencheu a ficha de interesse no site!
            
            --- DADOS DO ADOTANTE ---
            Nome: {adotante.nome}
            Telefone: {adotante.telefone}
            E-mail: {adotante.email}
            Endereço: {adotante.endereco}
            CPF: {adotante.cpf}
            """
            
            # Se tiver pet selecionado, adiciona no e-mail
            if pet_interesse:
                mensagem += f"\n\n--- INTERESSE NO PET ---\nNome: {pet_interesse.nome} (ID: {pet_interesse.id})"
            
            # 3. Dispara o E-mail (vai aparecer no seu terminal)
            send_mail(
                subject=assunto,
                message=mensagem,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['ampa.mirassol@hotmail.com'], 
                fail_silently=False,
            )

            # 4. Manda para a tela de sucesso
            return render(request, 'cadastro_sucesso.html') 
    else:
        form = CadastroAdotanteForm()

    return render(request, 'cadastro_adotante.html', {
        'form': form,
        'pet': pet_interesse 
    })


def index(request):
    # Busca 3 pets disponíveis para mostrar na capa
    # Se quiser aleatório, pode usar .order_by('?')[:3]
    pets_destaque = Pet.objects.filter(is_adotado=False).order_by('-id')[:3]
    
    return render(request, 'index.html', {'pets_destaque': pets_destaque})