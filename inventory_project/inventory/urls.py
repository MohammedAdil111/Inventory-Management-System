from django.urls import path
from .views import *

urlpatterns = [

    path('register/', register_user, name='register-user'),
    path('login/', login_user, name='login-user'),

    path('items/', create_item, name='create-item'),
    path('items/<int:item_id>/', read_item, name='read-item'),
    path('items/<int:item_id>/update/', update_item, name='update-item'),
    path('items/<int:item_id>/delete/', delete_item, name='delete-item'),


    path('test-redis/', test_redis, name='test-redis'),
]
