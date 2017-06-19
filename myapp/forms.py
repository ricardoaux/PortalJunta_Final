from django.contrib.auth import authenticate
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import extras
from django.conf import settings
from myapp.models import Ficheiro, Cidadao, Questionario, Pergunta, Opcao, Noticia, Evento, Ocorrencia, Requerimento, Servico
from datetime import datetime

class LoginForm(forms.Form):
    user = None
    username = forms.CharField(label="Username", max_length=30,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                                   widget=forms.TextInput(
                                       attrs={'type': 'password', 'name': 'password', 'class': 'form-control'}))


    def clean(self):
        global user
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("O utilizador e a password não correspondem")
        if not user.is_active:
            raise forms.ValidationError("O utilizador não está activo")
        if not user.is_superuser:
            cidadao = Cidadao.objects.get(user=user)
            aproved = cidadao.aprovado
            if not aproved:
                raise forms.ValidationError('O utilizador ainda não foi aprovado')
        return self.cleaned_data

    def getUser(self):
        global user
        return user


class UserCreationForm(forms.Form):
    username = forms.CharField(label='Nome de Utilizador', max_length=30, required=True)
    password1 = forms.CharField(label='Password',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Novamente)',
                        widget=forms.PasswordInput())
    email = forms.EmailField(label='Email', required=True)
    nome = forms.CharField(label='Nome', max_length=30, required=True)
    apelido = forms.CharField(label='Apelidos', max_length=70, required=True)
    num_bi = forms.IntegerField(label='Número do CC', required=True)
    this_year = datetime.now().year
    data_nascimento = forms.DateField(label='Data de Nascimento', required=True, widget=extras.SelectDateWidget(years=range(this_year-117,this_year+1)))
    morada = forms.CharField(label='Morada Completa', max_length=100, required=True)
    codigopostal = forms.CharField(label='Código Postal (xxxx-xxx)', max_length=8, required=True)
    localidade = forms.CharField(label='Localidade', max_length=30, required=True)
    telefone = forms.IntegerField(label='Telefone', required=True)
    nro_eleitor = forms.IntegerField(label='Número de Eleitor', required=True)
    pai = forms.CharField(label='Nome do Pai', max_length=100, required=True)
    mae = forms.CharField(label='Nome da Mãe', max_length=100, required=True)

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('A Password não corresponde')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('O nome de utilizador apenas pode conter caracteres alfanuméricos')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('O nome de utilizador já existe')

    def clean_num_bi(self):
        if 'num_bi' in self.cleaned_data:
            num_bi = self.cleaned_data['num_bi']
            if len(str(num_bi)) != 8:
                raise forms.ValidationError('O número do CC é inválido (8 digitos)')
            else:
                try:
                    Cidadao.objects.get(num_bi = num_bi)
                except ObjectDoesNotExist:
                    return num_bi
                raise forms.ValidationError('O número do BI já existe')

    def clean_codigopostal(self):
        if 'codigopostal' in self.cleaned_data:
            codigopostal = self.cleaned_data['codigopostal']
            r = re.compile('.{4}-.{3}')
            if len(str(codigopostal)) != 8:
                raise forms.ValidationError('O código de postal é inválido (exemplo: 0000-000)')
            elif not r.match(codigopostal):
                raise forms.ValidationError('O código de postal é inválido (exemplo: 0000-000)')
            else:
                return codigopostal

    def clean_telefone(self):
        if 'telefone' in self.cleaned_data:
            telefone = self.cleaned_data['telefone']
            if len(str(telefone)) != 9:
                raise forms.ValidationError('O número de telefone é inválido (9 digitos)')
            else:
                return telefone

#
# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Ficheiro
#         fields = ('titulo', 'descricao', 'tipo', 'ficheiro')
#
#
# class QuestionarioForm(forms.ModelForm):
#     class Meta:
#         model = Questionario
#         fields = ('titulo', 'descricao', 'quest')


class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = '__all__'


class OpcaoForm(forms.ModelForm):
    class Meta:
        model = Opcao
        fields = ('texto',)


class OcorrenciasForm(forms.ModelForm):
    local = forms.CharField(label='Morada Completa', max_length=100, required=True)
    informacao = forms.CharField(label='Descrição', max_length=1000, required=True, widget=forms.Textarea)

    class Meta:
        model = Ocorrencia
        fields = '__all__'
        exclude = ['utilizador', ]


class RequerimentoForm(forms.ModelForm):
    ENV = (
        ("C", "Correio"),
        ("L", "Levantamento na Junta"),
    )

    PAG = (
        ("J", "Pagar na Junta"),
        ("O", "Pagar Online"),
    )

    opcoes = Servico.objects.values_list('id', 'nome')
    servico = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=opcoes)
    descricao = forms.CharField(label='Declaro que:', max_length=1000, required=True, widget=forms.Textarea)
    documento = forms.FileField(label='Anexar ficheiro relevante (não obrigatório)', required=False)

    envio = forms.MultipleChoiceField(label='Envio (O envio por correio acresce 1€)', widget=forms.SelectMultiple, choices=ENV, initial='C')
    pagamento = forms.MultipleChoiceField(label='Método de Pagamento', widget=forms.SelectMultiple, choices=PAG, initial='O')

    class Meta:
        model = Requerimento
        fields = ('__all__')
        exclude = ['utilizador',  'estado', 'mensagem']

    def clean_servico(self):
        if 'servico' in self.cleaned_data:
            id = self.cleaned_data['servico']

            try:
                servico = Servico.objects.get(id = id[0])
                return servico
            except ObjectDoesNotExist:
                raise forms.ValidationError('O serviço não foi encontrado')


    def clean_envio(self):
        if 'envio' in self.cleaned_data:
            envio = self.cleaned_data['envio']
            return envio[0]


    def clean_pagamento(self):
        if 'pagamento' in self.cleaned_data:
            pag = self.cleaned_data['pagamento']
            return pag[0]


class EstadoForm(forms.ModelForm):
    ES = (
        ("ANALISE", "Em Análise"),
        ("PAGAMENTO", "Aguarda Pagamento"),
        ("PAGO", "Pagamento Efetuado"),
        ("DIFERIDO", "Diferido"),
        ("RECUSADO", "Recusado"),
    )

    estado = forms.MultipleChoiceField(label='Estado do Requerimento', widget=forms.SelectMultiple, choices=ES)
    mensagem = forms.CharField(label='Mensagem para o Utilizador', max_length=1000, required=False, widget=forms.Textarea)

    class Meta:
        model = Requerimento
        fields = ('estado', 'mensagem')

    def clean_estado(self):
        if 'estado' in self.cleaned_data:
            estado = self.cleaned_data['estado']
            return estado[0]



#    def __init__(self, id):
#        super(EstadoForm, self).__init__()
#        temp = Requerimento.objects.get(id=id)
#        self.fields['estado'].initial = temp.estado
#        self.fields['mensagem'].initial = temp.mensagem

