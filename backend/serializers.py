from rest_framework import serializers
from .models import Category, Item, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        # Check if category already exists
        category_name = validated_data.get('name')

        existing_category = Category.objects.filter(name=category_name).first()

        # If category already exists, raise a validation error
        if existing_category:
            raise serializers.ValidationError(
                "Category with this name already exists.")

        # If category doesn't exist, create a new one
        category_instance = Category.objects.create(**validated_data)

        return category_instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    tags = TagSerializer(many=True, required=False, allow_empty=True)

    class Meta:
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        print("Serial: ", validated_data)
        category_data = validated_data.pop('category', None)
        tags_data = validated_data.pop('tags', [])

        if category_data:
            category_id = category_data['name']
            if category_id:
                category_instance = Category.objects.get(name=category_id)
        item = Item.objects.create(
            **validated_data, category=category_instance)

        tags = []
        for tag_data in tags_data:
            tag_id = tag_data.get('id')
            if tag_id:
                tag = Tag.objects.get(id=tag_id)
                tags.append(tag)

        item.tags.set(tags)
        item.save()
        return item
