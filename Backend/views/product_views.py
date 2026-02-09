from Backend.serializers.product_serializer import ProductSerializer
from Backend.models.product_model import Product
from rest_framework.response import Response    
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # PAS besoin de context={'request': request} 
        # car on retourne juste le chemin
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Produit créé avec succès',
                'product': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductCatalogueView(APIView):
    permission_classes = [AllowAny]

class ProductCatalogueView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.all()
        # AJOUTER le context pour générer les URLs complètes
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        # PAS besoin de context={'request': request}
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({
                'error': 'Produit non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # PAS besoin de context={'request': request}
        serializer = ProductSerializer(product, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Produit mis à jour avec succès',
                'product': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({
                'error': 'Produit non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({
            'message': 'Produit supprimé avec succès'
        }, status=status.HTTP_200_OK)
    
    
# from Backend.serializers.product_serializer import ProductSerializer
# from Backend.models.product_model import Product
# from rest_framework.response import Response    
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework import status



# class ProductCreateView(APIView):
#     """
#     Vue pour créer un nouveau produit
#     POST /products/create/
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'message': 'Produit créé avec succès',
#                 'product': serializer.data
#             }, status=status.HTTP_201_CREATED)
        
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )
    
# class ProductCatalogueView(APIView):
#     """
#     Vue PUBLIQUE pour afficher le catalogue
#     GET /api/products/catalog/
#     - Accessible à TOUS (visiteurs + admin)
#     """
#     permission_classes = [AllowAny]

#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)    
# class ProductListView(APIView):
#     """
#     Vue pour lister tous les produits
#     GET /products/
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)    


# class ProductUpdateView(APIView):
#     """
#     Vue pour mettre à jour un produit existant
#     PUT /products/<int:pk>/update/
#     """
#     permission_classes = [IsAuthenticated]

#     def put(self, request, pk):
#         try:
#             product = Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             return Response({
#                 'error': 'Produit non trouvé'
#             }, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ProductSerializer(product, data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'message': 'Produit mis à jour avec succès',
#                 'product': serializer.data
#             }, status=status.HTTP_200_OK)
        
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )
    
# class ProductDeleteView(APIView):
#     """
#     Vue pour supprimer un produit existant
#     DELETE /products/<int:pk>/delete/
#     """
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, pk):
#         try:
#             product = Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             return Response({
#                 'error': 'Produit non trouvé'
#             }, status=status.HTTP_404_NOT_FOUND)
        
#         product.delete()
#         return Response({
#             'message': 'Produit supprimé avec succès'
#         }, status=status.HTTP_200_OK)    


