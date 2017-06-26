from django.test import TestCase

# Create your tests here.

from django.test import Client
import unittest
from django.contrib.auth.models import User
from myapp.models import Cidadao, Servico
import datetime
import json

class MyTest (unittest.TestCase):

    def setUp(self):
        #Valid register structure
        self.json_register_valid = {'username': 'testeuser', 'password1': 'teste123', 'password2': 'teste123',
                                                'email': 'exemplo@teste.com', 'nome': 'Exemplo', 'apelido': 'Teste',
                                                'num_bi': 13927456, 'data_nascimento': datetime.date(2009, 1, 1), 'morada': 'Rua do Teste',
                                                'codigopostal': '3030-007', 'localidade': 'Aquela', 'telefone': 917976372,
                                                'nro_eleitor': 123, 'pai': 'Armando', 'mae': 'Gertrudes'}

        #Invalid register structure (passwords não correspondem)
        self.json_register_invalid_pass = {'username': 'testeuser2', 'password1': 'teste123', 'password2': 'teste12345',
                                                'email': 'exemplo@ateste.com', 'nome': 'Exemplo', 'apelido': 'Teste',
                                                'num_bi': 13927486, 'data_nascimento': datetime.date(2009, 1, 1), 'morada': 'Rua do Teste',
                                                'codigopostal': '3030-007', 'localidade': 'Aquela', 'telefone': 917976372,
                                                'nro_eleitor': 123, 'pai': 'Armando', 'mae': 'Gertrudes'}

        #Invalid register structure (username existente)
        self.json_register_invalid_username = {'username': 'testeuser', 'password1': 'teste123', 'password2': 'teste123',
                                                'email': 'exemplo@bteste.com', 'nome': 'Exemplo', 'apelido': 'Teste',
                                                'num_bi': 13927786, 'data_nascimento': datetime.date(2009, 1, 1), 'morada': 'Rua do Teste',
                                                'codigopostal': '3030-007', 'localidade': 'Aquela', 'telefone': 917976372,
                                                'nro_eleitor': 123, 'pai': 'Armando', 'mae': 'Gertrudes'}

        #Invalid register structure (campo por preencher - num_bi)
        self.json_register_invalid_required = {'username': 'testeuser3', 'password1': 'teste123', 'password2': 'teste12345',
                                                'email': 'exemplo@cteste.com', 'nome': 'Exemplo', 'apelido': 'Teste',
                                                'num_bi': None,'data_nascimento': datetime.date(2009, 1, 1), 'morada': 'Rua do Teste',
                                                'codigopostal': '3030-007', 'localidade': 'Aquela', 'telefone': 917976372,
                                                'nro_eleitor': 123, 'pai': 'Armando', 'mae': 'Gertrudes'}

        self.json_login_valid = {'username': 'testeuser', 'password': 'teste123'}
        self.json_login_invalid = {'username': 'exemplo', 'password': 'teste123'}


        self.client = Client()


    ### POST ###

    if True:
        def test_invalid_pass_register(self):
            request = self.client.post('/register/', self.json_register_invalid_pass, format='json')
            #print (request.status_code)
            assert request.status_code == 400

        def test_invalid_username_register(self):
            request = self.client.post('/register/', self.json_register_invalid_username, format='json')
            #print (request.status_code)
            assert request.status_code == 400

        def test_invalid_required_register(self):
            request = self.client.post('/register/', self.json_register_invalid_required, format='json')
            #print (request.status_code)
            assert request.status_code == 400

        def test__valid_register(self):
            request = self.client.post('/register/', self.json_register_valid, format='json')
            #print (request.status_code)
            User.objects.filter(username = 'testeuser').update(is_active = True)
            Cidadao.objects.filter(user = User.objects.get(username = 'testeuser')).update(aprovado = True)
            assert request.status_code == 200

        def test_login_invalid(self):
            request = self.client.post('/login/', self.json_login_invalid, format='json')
            #print (request.status_code)
            #print (request.content)
            assert request.status_code == 400

        def test_login_valid(self):
            #self.logged = self.client.login(username = 'testeuser', password='teste123')
            #print (self.logged)
            request = self.client.post('/login/', self.json_login_valid, format='json')
            #print (request.status_code)
            #print (request.content)
            assert request.status_code == 200

    if False:
        def test_requerimento_valid(self):
            self.servico = Servico(nome='Atestado de vida', preco=10.0, descricao='Blabla bla bla bla')
            self.servico.save()

            self.client.post('/login/', self.json_login_valid, format='json')

            #Valid requerimento structure
            self.json_requerimento_valid = {'servico': self.servico.id, 'descricao': 'Qualquer coisa' , 'documento': None, 'envio': 'C', 'pagamento': 'O'}
            request = self.client.post('/requerimento/', self.json_requerimento_valid, format='json', follow=True)
            print (request.content)
            assert request.status_code == 200

        def test_requerimento_invalid(self):
            self.client.post('/login/', self.json_login_valid, format='json')

            #Valid requerimento structure
            #self.json_requerimento_invalid = {'servico': None, 'descricao': 'Qualquer coisa' , 'documento': None, 'envio': 'C', 'pagamento': 'O'}
            #request = self.client.post('/requerimento/', self.json_requerimento_invalid, format='json', follow=True)

            #assert request.status_code == 400

    if True:
        def test_ocorrencia_valid(self):
            self.client.post('/login/', self.json_login_valid, format='json')
            self.json_ocorrencia_valid = {'local': 'Rua Qualquer', 'categoria': 'Animais abandonados', 'informacao': 'Qualquer coisa', 'imagem': None}
            request = self.client.post('/requerimento/', self.json_ocorrencia_valid, format='json', follow=True)
            assert request.status_code == 200

    def test_requerimento_consultar(self):
        self.client.post('/login/', self.json_login_valid, format='json')

        request = self.client.get('/requerimento/consultar')
        assert request.status_code == 200

    ### GET ###

    def test_homepage(self):
        request = self.client.get('/')
        #print (request.status_code)
        #print (request.content)
        assert request.status_code == 200

    def test_login_page(self):
        request = self.client.get('/login/')
        #print (request.status_code)
        #print (request.content)
        assert request.status_code == 200

    def test_heraldica(self):
        request = self.client.get('/heraldica/')
        #print (request.status_code)
        #print (request.content)
        assert request.status_code == 200

    def test_historia(self):
        request = self.client.get('/historia/')
        #print (request.status_code)
        #print (request.content)
        assert request.status_code == 200

    def test_assembleia_composicao(self):
        request = self.client.get('/assembleia/composicao/')
        #print (request.status_code)
        #print (request.content)
        assert request.status_code == 200

    def test_assembleia_competencias(self):
        request = self.client.get('/assembleia/competencias/')
        #print (request.status_code)
        #print (request.content)
        assert request.status_code == 200

    def test_junta_executivo(self):
        request = self.client.get('/junta/executivo/')
        #print (request.status_code)
        #print (request.content)
        assert request.status_code == 200

    def test_junta_competencias(self):
        request = self.client.get('/junta/competencias/')
        #print (request.status_code)
        #print (request.content)
        assert request.status_code == 200

    def test_noticias(self):
        request = self.client.get('/noticias/')
        #print (request.status_code)
        #print (request.content)
        assert request.status_code == 200

    def test_eventos(self):
        request = self.client.get('/eventos/')
        #print (request.status_code)
        #print (request.content)
        assert request.status_code == 200

    def test_contatos(self):
        request = self.client.get('/contactos/')
        #print (request.status_code)
        assert request.status_code == 200

    def test_planos_acao(self):
        request = self.client.get('/planosdeacao/')
        #print (request.status_code)
        assert request.status_code == 200

    def test_contas(self):
        request = self.client.get('/contas/')
        #print (request.status_code)
        assert request.status_code == 200

    def test_atas(self):
        request = self.client.get('/actas/')
        #print (request.status_code)
        assert request.status_code == 200

    def test_outros(self):
        request = self.client.get('/outros/')
        #print (request.status_code)
        assert request.status_code == 200

    def test_servicos(self):
        request = self.client.get('/servicos/')
        #print (request.status_code)
        assert request.status_code == 200

    def test_requerimentos_auth(self):
        logged_in = self.client.post('/login/', self.json_login_valid, format='json')
        request = self.client.get('/requerimento/')
        assert request.status_code == 200

    def test_requerimentos_without_auth(self):
        self.client.logout()
        request = self.client.get('/requerimento/', follow=True)
        #print (request.status_code)
        assert request.status_code == 404

    def test_requerimento_consultar_auth(self):
        self.client.login(username='testeuser', password='teste123')
        request = self.client.get('/requerimento/consultar', follow=True)
        #print (request.status_code)
        assert request.status_code == 200

    def test_requerimento_consultar_without_auth(self):
        self.client.logout()
        request = self.client.get('/requerimento/consultar', follow=True)
        #print (request.status_code)
        assert request.status_code == 404

    def test_questionario_consultar_auth(self):
        self.client.login(username='testeuser', password='teste123')
        request = self.client.get('/questionario/', follow=True)
        #print (request.status_code)
        assert request.status_code == 200

    def test_questionar_consultar_without_auth(self):
        self.client.logout()
        request = self.client.get('/questionario/', follow=True)
        #print (request.status_code)
        assert request.status_code == 404



