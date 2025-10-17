from rest_framework import serializers
from .models import Product
import os

def validate_name(value):
    if len(value) < 3:
        raise serializers.ValidationError("Ürün adı en az 3 karakter olmalıdır.")
    
    if len(value) > 200:
        raise serializers.ValidationError("Ürün adı en çok 200 karakter olmalıdır.")
    
    return value
    
def validate_price(value):
    if value < 1:
        raise serializers.ValidationError("Fiyat sıfırdan büyük olmalıdır.")
    return value

def validate_slug(value,instance=None):
    product_id = instance.id if instance else None

    if Product.objects.filter(slug=value).exclude(id=product_id).exists():
        raise serializers.ValidationError("Bu slug zaten kullanılıyor.")
    return value

def validate_product_object(data):
    if data.get("isHome") and not data.get("isActive"):
        raise serializers.ValidationError("Ana sayfada gösterilecek ürün aktif olmalıdır.")
    
    name = data.get("name", "")
    description = data.get("description", "")

    if not description and len(name) < 10:
        raise  serializers.ValidationError("Açıklama yoksa ürün adı en az 10 karakter olmalıdır.")
    
    if data.get("isActive") and data.get("stock", 0) == 0:
        raise serializers.ValidationError("Aktif ürünlerin stoğu 0 olamaz.")

    return data

ALLOWED_EXTENSIONS = [".jpg",".jpeg"]
MAX_FILE_SIZE_MB = 1

def validate_uploaded_image(file):
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise serializers.ValidationError(f"Desteklenmeyen bir resim uzantısı:{ext}. Sadece .jpg ve .jpeg resimleri yükleyiniz.")
    
    file_size_mb = file.size / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        raise serializers.ValidationError(f"Resim boyutu çok fazla. Max. kabul edilen {MAX_FILE_SIZE_MB} mb.")