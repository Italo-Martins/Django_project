from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from .forms import ContatoForm, ProdutoModelForm
from .models import Produto

# Create your views here.

def index(request):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)

def contato(request):
    form = ContatoForm(request.POST or None)
    print(request.POST)
    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()

            '''nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            assunto = form.cleaned_data['assunto']
            mensagem = form.cleaned_data['mensagem']

            print('Mesnagem Enviada')
            print(f'Nome: {nome}')
            print(f'E-mail: {email}')
            print(f'Assunto: {assunto}')
            print(f'Mensagem: {mensagem}')'''

            messages.success(request, 'E-mail enviado com sucesso!')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar E-mail!')
    context = {
        'form' : form
    }
    return render(request, 'contato.html', context)

def produto(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                '''prod = form.save(commit = False)
                print(f'Nome: {prod.nome}')
                print(f'Preço: {prod.preco}')
                print(f'Estoque: {prod.estoque}')
                print(f'Imagem: {prod.imagem}')'''
                
                messages.success(request, 'Produto salvo com sucesso!')
                form = ProdutoModelForm()
            else:
                messages.error(request, 'Erro ao salvar o produto!')
        else:
            form = ProdutoModelForm()
        context = {
            'form' : form
        }
        return render(request, 'produto.html', context)
    else:
        return redirect('index')

