from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializer import *
from users.models import *
from books.models import *

# Create your views here.
class cartOperations(APIView):
    permission_classes=[IsAuthenticated]
    serializer = createCartSerializer
    model = CartItemModel

    def post(self,request):
        try:
            data = request.data
            cart = self.serializer(data=data)

            if not cart.is_valid():
                return Response({'message': cart.error_messages},status=400)
            
            print(cart.validated_data.get('userId'),cart.validated_data.get('price'))
            db_user = CustomUser.objects.get(id=cart.validated_data.get('userId'))
            db_book = BookModel.objects.get(id=cart.validated_data.get('bookId'))
            price = cart.validated_data.get('price')
            quantity = cart.validated_data.get('quantity')

            cartItem,created = self.model.objects.get_or_create(user=db_user,book=db_book,price=price,quantity=quantity)
            cart = self.model.objects.filter(user_id = request.user.id)

            full_cart = [{'id': c.id,'user': c.user.id,'book': c.book.id,'price': c.price,'quantity': c.quantity} for c in cart]

            return Response({
                'cart': full_cart,
            },status=200)

        except Exception as err:
            return Response({'message':err.args},status=500)
        
        
    def get(self,request):
        try:
            cart = self.model.objects.filter(user__id = request.user.id)
            full_cart = [{'id': c.id,'user': c.user.id,'book': c.book.id,'price': c.price,'quantity': c.quantity} for c in cart]

            return Response({
                'cart': full_cart,
            },status=200)

        except Exception as err:
            return Response({'message':err.args},status=500)
        


class CartItemView(APIView):
    permission_classes=[IsAuthenticated]
    model = CartItemModel
    
    def get(self,request):
        try:
            cart = self.model.objects.filter(user__id = request.user.id)
            full_cart = [{'id': c.id,'user': c.user.id,'book': c.book.id,'price': c.price,'quantity': c.quantity} for c in cart]

            return Response({
                'cart': full_cart,
            },status=200)

        except Exception as err:
            return Response({'message':err.args},status=500)
        
    def delete(self,request,id):
        try:
            print(id)
            cart_item = self.model.objects.get(id=id)

            cart_item.delete()

            cart = self.model.objects.filter(user__id = request.user.id)
            full_cart = [{'id': c.id,'user': c.user.id,'book': c.book.id,'price': c.price,'quantity': c.quantity} for c in cart]

            return Response({
                'message':'deleted successfully',
                'cart': full_cart
            },status=200)

        except Exception as err:
            print(err.args)
            return Response({'message':err.args},status=500)
