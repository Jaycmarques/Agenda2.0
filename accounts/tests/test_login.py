import pytest
from django.urls import reverse
from model_bakery import baker

from models import User
# from project.django_assertions import assert_contains, assert_not_contains


@pytest.fixture
def resp(client, db):
    return client.get(reverse('login'))


def test_login_page(resp):
    assert resp.status_code == 200


@pytest.fixture
def usuario(db, django_user_model):
    usuario_modelo = baker.make(django_user_model)
    senha = 'senha'
    usuario_modelo.set_password(senha)
    usuario_modelo.save()
    usuario_modelo.senha_plana = senha
    return usuario_modelo


@pytest.fixture
def resp_post(client, usuario):
    return client.post(reverse('login'), {'username': usuario.email, 'password': usuario.senha_plana})


def test_login_redirect(client, usuario):
    # Realiza o login com o usuário criado
    response = client.post(reverse('login'), {
        'email': usuario.email,
        'password': usuario.senha_plana,
    })

    # Verifica se o status de resposta é de redirecionamento
    assert response.status_code == 302
    # Verifica a URL de redirecionamento após o login
    assert response.url == reverse('home')
    # Verifica se o usuário foi autenticado corretamente (não estritamente necessário se o teste é para redirecionamento)
    assert User.objects.filter(email=usuario.email).exists()
