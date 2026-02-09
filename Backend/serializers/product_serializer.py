from rest_framework import serializers
from Backend.models.product_model import CategoryChoices, Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(
        choices=CategoryChoices.choices,
        label="Catégorie"
    )
    
    image = serializers.ImageField(
        label="Image",
        required=False,
        allow_null=True
    )  


    
    title = serializers.CharField(
        max_length=100,
        label="Titre"
    )
    desc = serializers.CharField(
        label="Description"
    )
    price = serializers.CharField(
        max_length=50,
        label="Prix"
    )
    image_url = serializers.SerializerMethodField()
    
    title = serializers.CharField(
        max_length=100,
        label="Titre"
    )
   
    
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            # Construire l'URL complète
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    class Meta:
        model = Product
        fields = ['id', 'category', 'image', 'title', 'desc', 'price', 'image_url']
    
# from rest_framework import serializers
# from Backend.models.product_model import CategoryChoices, Product


# class ProductSerializer(serializers.ModelSerializer):
#     category = serializers.ChoiceField(
#         choices=CategoryChoices.choices,
#         label="Catégorie"
#     )
#     image = serializers.ImageField(
#         label="Image",
#         required=False,
#         allow_null=True
        
       
#     )
#     title = serializers.CharField(
#         max_length=100,
#         label="Titre"
#     )
#     desc = serializers.CharField(
#         label="Description"
#     )
#     price = serializers.CharField(
#         max_length=50,
#         label="Prix"
#     )

#     class Meta:
#         model = Product
#         fields = ['id', 'category', 'image', 'title', 'desc', 'price']
