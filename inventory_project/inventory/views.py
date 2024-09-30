from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import generics
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication



@api_view(['POST'])
@permission_classes([AllowAny]) 
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        cache.set(f'user_{user.id}', serializer.data, timeout=60*15)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:  
        return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
def create_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()  
        cache.set(f'item_{item.id}', item, timeout=60 * 15)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])

def read_item(request, item_id):
    item = cache.get(f'item_{item_id}')
    if item is None:
        try:
            item = Item.objects.get(pk=item_id)
            cache.set(f'item_{item_id}', item, timeout=60*15) 
        except Item.DoesNotExist:
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])

def update_item(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.set(f'item_{item_id}', item, timeout=60*15) 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])

def delete_item(request, item_id):
    try:
        print(f"Deleting item with ID: {item_id}")
        item = Item.objects.filter(pk=item_id)
        if item is None:
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)  
        item.delete()
        print(f"Deleting item with ID: {item_id}")

        cache.delete(f'item_{item_id}')  
        return Response({'message': 'Item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)


# Checking Redis is connected or not 

from django.core.cache import cache
from django.http import JsonResponse

@authentication_classes([TokenAuthentication])
def test_redis(request):
    cache.set('my_key', 'Hello from Redis!', timeout=60)  
    value = cache.get('my_key') 
    return JsonResponse({'message': value})  