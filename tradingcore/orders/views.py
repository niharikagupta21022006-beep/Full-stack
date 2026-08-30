from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self,serializer):
        order = serializer.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'orders_group',
            {
                'type':'send_order_update',
                'order':{
                    'id':order.id,
                    'price':str(order.price),
                    'quantity':order.quantity,
                    'side':order.side,
                }
            }
            
        )

# Create your views here.
