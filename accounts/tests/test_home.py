# accounts/tests/test_views.py

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_index_view(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert 'Welcome' in response.content.decode()


@pytest.mark.django_db
def test_register_view(client):
    # Envie uma solicitação POST para a página de registro com dados de teste
    response = client.post(reverse('register'), data={
        'email': 'newuser@example.com',
        'first_name': 'New',
        'password1': 'newpassword',
        'password2': 'newpassword',
    })

    # Verifique se a resposta foi um redirecionamento, indicando sucesso
    assert response.status_code == 302  # Código de status para redirecionamento

    # Verifique se o usuário foi criado com sucesso
    User = get_user_model()
    assert User.objects.filter(email='newuser@example.com').exists()
