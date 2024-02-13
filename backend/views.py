from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer


class ItemAPI(APIView):
    # authentication_classes = [SessionAuthentication,
    #                           BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PageNumberPagination()

        # Retrieve query parameters
        keyword = request.query_params.get('keyword')
        category = request.query_params.get('category')
        sku = request.query_params.get('sku')
        name = request.query_params.get('name')
        in_stock_min = request.query_params.get('in_stock_min')
        in_stock_max = request.query_params.get('in_stock_max')
        available_stock_min = request.query_params.get('available_stock_min')
        available_stock_max = request.query_params.get('available_stock_max')
        net_stock_min = request.query_params.get('net_stock_min')
        net_stock_max = request.query_params.get('net_stock_max')

        # Build the queryset based on the filters
        queryset = Item.objects.all()

        # Filter by keyword in SKU, Category, and Name
        if keyword:
            queryset = queryset.filter(
                Q(sku__icontains=keyword) |
                Q(category__name__icontains=keyword) |
                Q(name__icontains=keyword))

        if sku:
            queryset = queryset.filter(sku__icontains=sku)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if name:
            queryset = queryset.filter(name__icontains=name)

        # Filter by range for In Stock
        if in_stock_min is not None:
            queryset = queryset.filter(in_stock__gte=in_stock_min)
        if in_stock_max is not None:
            queryset = queryset.filter(in_stock__lte=in_stock_max)

        # Filter by range for Available Stock
        if available_stock_min is not None:
            queryset = queryset.filter(
                available_stock__gte=available_stock_min)
        if available_stock_max is not None:
            queryset = queryset.filter(
                available_stock__lte=available_stock_max)

        # Filter by range for Net Stock
        if net_stock_min is not None:
            queryset = queryset.filter(net_stock__gte=net_stock_min)
        if net_stock_max is not None:
            queryset = queryset.filter(net_stock__lte=net_stock_max)

        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ItemSerializer(paginated_queryset, many=True)
        # Extracting relevant fields for the dashboard
        data = [
            {
                'SKU': item['sku'],
                'Name': item['name'],
                'Category': item['category']['name'] if item['category'] else None,
                'Tags': [tag['name'] for tag in item['tags']],  # TODO: Add url
                'InStock': item['in_stock'],
                'AvailableStock': item['available_stock'],
            }
            for item in serializer.data
        ]

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        print("Request: ", request.data)
        serializer = ItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryAPI(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print("Request: ", request.data)
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
