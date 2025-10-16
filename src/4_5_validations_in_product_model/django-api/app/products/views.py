from .models import Product
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET','POST'])
def product_list(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def product_details(request,pk):

    if request.method == 'GET':

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'Error':'Product not found'}, status=404)
        
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)