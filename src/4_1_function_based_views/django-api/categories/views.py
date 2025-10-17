from django.shortcuts import render
from  rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET','POST'])
def category_list(request):
    if request.method == "POST":
        return Response(
            {
                "message": "Bilgiler kayıt edildi", 
                "data": request.data
            })
    return Response({
        "message": "Veriler listelendi."
    })


