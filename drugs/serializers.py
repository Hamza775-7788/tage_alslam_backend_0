from rest_framework import serializers
from .models import Drug, DrugCategory, DrugUnits, Order, OrderItem,Offer
from django.contrib.auth import get_user_model

User = get_user_model()

class DrugCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugCategory
        fields = ['id', 'name', 'description']


class DrugUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugUnits
        fields = ['id', 'name', 'description']


class DrugSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category.name', read_only=True)
    unit_name = serializers.StringRelatedField(source='unit.name', read_only=True)

    agent = serializers.SerializerMethodField()
    manufacturer = serializers.SerializerMethodField()
    country_of_origin = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    usage = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    expiry_date = serializers.SerializerMethodField()

    class Meta:
        model = Drug
        fields = [
            'id', 'name_ar', 'name_en',
            'description',
            'agent', 'manufacturer', 'country_of_origin', 'scientific_name',
            'category', 'category_name', 'unit', 'unit_name',
            'usage', 'price',
            'expiry_date', 'image',
            'is_active', 'created_at', 'updated_at'
        ]

    def get_agent(self, obj):
        return obj.agent if obj.show_agent else None

    def get_manufacturer(self, obj):
        return obj.manufacturer if obj.show_manufacturer else None

    def get_country_of_origin(self, obj):
        return obj.country_of_origin if obj.show_country_of_origin else None

    def get_scientific_name(self, obj):
        return obj.scientific_name if obj.show_scientific_name else None

    def get_usage(self, obj):
        return obj.usage if obj.show_usage else None

    def get_price(self, obj):
        return obj.price if obj.show_price else None
    def get_description(self, obj):
        return obj.description if obj.show_description else None
    def get_expiry_date(self, obj):
        return obj.expiry_date if obj.show_expiry_date else None


class DrugSimpleSerializer(serializers.ModelSerializer):
    """للإدخال (POST) عند إنشاء طلب"""
    class Meta:
        model = Drug
        fields = ['id']


class OrderItemSerializer(serializers.ModelSerializer):
    drug = DrugSerializer(read_only=True)
    # drug_name = serializers.StringRelatedField(read_only=True,source='drug.name_ar')
    drug = serializers.StringRelatedField(read_only=True,source='drug.name_ar')
    drug_id = serializers.PrimaryKeyRelatedField(queryset=Drug.objects.all(),  source='drug')

    class Meta:
        model = OrderItem
        fields = ['id', 'drug', 'drug_id', 'quantity', 'price_at_order', 'total_price']
        read_only_fields = ['total_price']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'created_at', 'updated_at',
            'is_confirmed', 'is_delivered', 'notes', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class DrugMostOrderingSerializer(serializers.Serializer):
    drug = DrugSerializer()
    total_quantity = serializers.IntegerField()
    # total_price = serializers.FloatField()