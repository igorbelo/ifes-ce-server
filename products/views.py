from products.models import Product, Order, Item
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('created','deleted')

class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Item
        exclude = ('order','created','deleted')

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ('created','deleted')

    def get_total(self, obj):
        return obj.total()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        order = Order.objects.create()
        items = request.data.get('items')
        for item in items:
            Item.objects.create(
                order_id = order.id,
                product_id = item['product_id'],
                quantity = item['quantity']
            )

        return Response(
            self.get_serializer(order).data
        )
