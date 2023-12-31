from django.urls import path
from .views import encryption, decryption, HomePage, encryption_result

urlpatterns = [
    path('', HomePage, name='encryption'),
    path('encryption/', encryption, name='encryption'),
    path('decryption/', decryption, name='decryption'),
    path('encryption_result/', encryption_result, name='encryption_result'),
]
