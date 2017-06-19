"""PortalJunta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^manager/utilizador/$', RedirectView.as_view(url="/admin/auth/user")),
    url(r'^manager/evento/$', RedirectView.as_view(url="/admin/myapp/evento")),
    url(r'^manager/noticia/$', RedirectView.as_view(url="/admin/myapp/noticia")),
    url(r'^manager/ficheiro/$', RedirectView.as_view(url="/admin/myapp/ficheiro")),
    url(r'^manager/questionario/$', RedirectView.as_view(url="/admin/myapp/questionario")),
    url(r'^manager/pergunta/$', RedirectView.as_view(url="/admin/myapp/pergunta")),
    url(r'^manager/servico/$', RedirectView.as_view(url="/admin/myapp/servico")),
    url(r'^manager/requerimento/$', RedirectView.as_view(url="/admin/myapp/requerimento")),
    url(r'^manager/mensagem/(?P<num>[0-9]+)/$', views.mensagem_redirect),
    url(r'^manager/ocorrencia/(?P<num>[0-9]+)/$', views.ocorrencia_redirect),
    url(r'^manager/requerimento/(?P<num>[0-9]+)/$', views.requerimento_redirect),
    url(r'^manager/requerimento/(?P<num>[0-9]+)/change/$', views.change_state),
    url(r'^manager/utilizador/(?P<num>[0-9].*)', views.show_cidadao),
    url(r'^manager/eupago/$', views.eupago_redirect),
    url(r'^manager/paypal/$', views.paypal_redirect),
    url(r'^manager/$', views.admin, name="admin"),

    url(r'^success/(?P<num>[0-9]+)/$', views.success_paypal),
    url(r'^requerimento/eupago/$', views.euPago),

    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.mylogin, name='login'),
    url(r'^logout/$', views.logout_page, name="logout_page"),
    url(r'^register/$', views.register_page, name="register_page"),
    url(r'^heraldica/$', views.show_heraldica, name="heraldica"),
    url(r'^historia/$', views.show_historia, name="historia"),
    url(r'^assembleia/composicao/$', views.show_composicao, name="composicao"),
    url(r'^junta/executivo/$', views.show_executivo, name="executivo"),
    url(r'^junta/competencias/$', views.show_jcompetencias, name="junta_competencias"),
    url(r'^assembleia/competencias/$', views.show_acompetencias, name="assembleia_competencias"),
    url(r'^contactos/$', views.show_contactos, name="contactos"),
    url(r'^noticias/$', views.noticias),
    url(r'^noticias/(?P<num>[0-9]+)/$', views.noticias),
    url(r'^eventos/$', views.eventos),
    url(r'^eventos/(?P<num>[0-9]+)/$', views.eventos),
    url(r'^planosdeacao/$', views.show_acao, name="acao"),
    url(r'^contas/$', views.show_contas, name="contas"),
    url(r'^actas/$', views.show_atas, name="actas"),
    url(r'^outros/$', views.show_outros, name="outros"),
    url(r'^utilizador/ativar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activationview, name='user-activation-link'),
    url(r'^mensagem/add$', views.send_message, name="mensagem"),
    url(r'^votacao/$', views.show_votacao, name="votacao"),
    url(r'^votacao/(?P<num>[0-9]+)/$', views.show_votacao2),
    url(r'^votacao/(?P<pergunta_id>[0-9]+)/votar$', views.votar, name='votar'),
    url(r'^questionario/$', views.questionario),
    url(r'^questionario/(?P<num>[0-9]+)/$', views.questionario2),
    url(r'^votacao/votos/(?P<num>[0-9]+)/$', views.show_votos),
    url(r'^ocorrencia/$', views.ocorrencias),
    url(r'^requerimento/$', views.requerimentos),
    url(r'^requerimento/consultar$', views.estado_requerimentos),
    url(r'^servicos/$', views.show_taxas),

    url(r'^autenticacao/error/$', views.auth_error, name='auth_error'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.my_404_view
