from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from Backend.models.blog_model import BlogPost, BlogPostStatus
from Backend.serializers.blog_serializer import BlogPostSerializer


# =========================
# PUBLIC — SITE VITRINE
# =========================

class BlogCatalogueView(APIView):
    """
    Liste des articles publiés (site public)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        posts = BlogPost.objects.filter(
            status=BlogPostStatus.PUBLISHED
        ).order_by('-published_at')

        # context nécessaire pour URLs d’images
        serializer = BlogPostSerializer(
            posts,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogDetailPublicView(APIView):
    """
    Détail d’un article publié (site public)
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        post = get_object_or_404(
            BlogPost,
            slug=slug,
            status=BlogPostStatus.PUBLISHED
        )

        serializer = BlogPostSerializer(
            post,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


# =========================
# ADMIN — DASHBOARD
# =========================

class BlogCreateView(APIView):
    """
    Créer un article (admin)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BlogPostSerializer(
            data=request.data,
            context={'request': request}  # <-- AJOUTÉ ICI
        )

        if serializer.is_valid():
            post = serializer.save()

            # Si publié → définir la date
            if post.status == BlogPostStatus.PUBLISHED and not post.published_at:
                post.publish()

            return Response({
                'message': 'Article créé avec succès',
                'post': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BlogListView(APIView):
    """
    Liste complète des articles (admin)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = BlogPost.objects.all().order_by('-created_at')
        serializer = BlogPostSerializer(
            posts, 
            many=True,
            context={'request': request}  # <-- AJOUTÉ ICI
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogUpdateView(APIView):
    """
    Modifier un article (admin)
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, slug):
        try:
            post = BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            return Response(
                {'error': 'Article non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BlogPostSerializer(
            post, 
            data=request.data, 
            partial=True,
            context={'request': request}  # <-- AJOUTÉ ICI
        )

        if serializer.is_valid():
            post = serializer.save()

            if post.status == BlogPostStatus.PUBLISHED and not post.published_at:
                post.publish()

            return Response({
                'message': 'Article mis à jour avec succès',
                'post': serializer.data
            }, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BlogDeleteView(APIView):
    """
    Supprimer un article (admin)
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        try:
            post = BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            return Response(
                {'error': 'Article non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

        post.delete()

        return Response(
            {'message': 'Article supprimé avec succès'},
            status=status.HTTP_200_OK
        )
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework import status
# from django.shortcuts import get_object_or_404

# from Backend.models.blog_model import BlogPost, BlogPostStatus
# from Backend.serializers.blog_serializer import BlogPostSerializer


# # =========================
# # PUBLIC — SITE VITRINE
# # =========================

# class BlogCatalogueView(APIView):
#     """
#     Liste des articles publiés (site public)
#     """
#     permission_classes = [AllowAny]

#     def get(self, request):
#         posts = BlogPost.objects.filter(
#             status=BlogPostStatus.PUBLISHED
#         ).order_by('-published_at')

#         # context nécessaire pour URLs d’images
#         serializer = BlogPostSerializer(
#             posts,
#             many=True,
#             context={'request': request}
#         )

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class BlogDetailPublicView(APIView):
#     """
#     Détail d’un article publié (site public)
#     """
#     permission_classes = [AllowAny]

#     def get(self, request, slug):
#         post = get_object_or_404(
#             BlogPost,
#             slug=slug,
#             status=BlogPostStatus.PUBLISHED
#         )

#         serializer = BlogPostSerializer(
#             post,
#             context={'request': request}
#         )

#         return Response(serializer.data, status=status.HTTP_200_OK)


# # =========================
# # ADMIN — DASHBOARD
# # =========================

# class BlogCreateView(APIView):
#     """
#     Créer un article (admin)
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = BlogPostSerializer(data=request.data)

#         if serializer.is_valid():
#             post = serializer.save()

#             # Si publié → définir la date
#             if post.status == BlogPostStatus.PUBLISHED and not post.published_at:
#                 post.publish()

#             return Response({
#                 'message': 'Article créé avec succès',
#                 'post': serializer.data
#             }, status=status.HTTP_201_CREATED)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class BlogListView(APIView):
#     """
#     Liste complète des articles (admin)
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         posts = BlogPost.objects.all().order_by('-created_at')
#         serializer = BlogPostSerializer(posts, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class BlogUpdateView(APIView):
#     """
#     Modifier un article (admin)
#     """
#     permission_classes = [IsAuthenticated]

#     def put(self, request, slug):
#         try:
#             post = BlogPost.objects.get(slug=slug)
#         except BlogPost.DoesNotExist:
#             return Response(
#                 {'error': 'Article non trouvé'},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = BlogPostSerializer(post, data=request.data, partial=True)

#         if serializer.is_valid():
#             post = serializer.save()

#             if post.status == BlogPostStatus.PUBLISHED and not post.published_at:
#                 post.publish()

#             return Response({
#                 'message': 'Article mis à jour avec succès',
#                 'post': serializer.data
#             }, status=status.HTTP_200_OK)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class BlogDeleteView(APIView):
#     """
#     Supprimer un article (admin)
#     """
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, slug):
#         try:
#             post = BlogPost.objects.get(slug=slug)
#         except BlogPost.DoesNotExist:
#             return Response(
#                 {'error': 'Article non trouvé'},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         post.delete()

#         return Response(
#             {'message': 'Article supprimé avec succès'},
#             status=status.HTTP_200_OK
#         )
