import pytest
from django.urls import reverse
from accounts.models import User  # Importa o modelo de usuário personalizado


@pytest.mark.django_db
def test_user_registration(client):
    response = client.post(reverse('register'), {
        'email': 'testuser@example.com',  # Usando 'email' em vez de 'username'
        'first_name': 'Test',             # Incluindo o campo 'first_name' se necessário
        'password1': 'securepassword123',
        'password2': 'securepassword123'
    })
    # Espera-se redirecionamento após registro bem-sucedido
    assert response.status_code == 302
    # Verifique a URL de redirecionamento
    assert response.url == reverse('success')
    # Verifique se o usuário foi criado no banco de dados
    assert User.objects.filter(email='testuser@example.com').exists()
