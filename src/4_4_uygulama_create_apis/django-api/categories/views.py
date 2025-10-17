from rest_framework import status
from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer, CategoryCreateSerializer
from  rest_framework.response import Response
from rest_framework.decorators import api_view

# / categories
# / categories/create

@api_view(['GET','POST'])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":    
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def category_detail(request,pk):
    category = Category.objects.get(pk=pk)
    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data)

    


