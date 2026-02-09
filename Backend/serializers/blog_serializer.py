from rest_framework import serializers
from Backend.models import BlogPost
from django.utils.text import slugify

class BlogPostSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "content",
            "image", 
            "image_url",
            "type",
            "status",
            "published_at",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True}
        }
    def get_image_url(self, obj):
        print(f"DEBUG BlogPost {obj.id}: image={obj.image}")
        if obj.image and hasattr(obj.image, 'url'):
            print(f"DEBUG BlogPost {obj.id}: image.url={obj.image.url}")
            # Construire l'URL complète
            request = self.context.get('request')
            if request:
                url = request.build_absolute_uri(obj.image.url)
                print(f"DEBUG BlogPost {obj.id}: absolute_url={url}")
                return url
            url = obj.image.url
            print(f"DEBUG BlogPost {obj.id}: relative_url={url}")
            return url
        print(f"DEBUG BlogPost {obj.id}: No image")
        return ""  # ← CHANGÉ: Retourner chaîne vide au lieu de None
    
    
    def validate(self, data):
        """Validation simple"""
        # Auto-générer le slug si non fourni
        if 'slug' not in data or not data['slug']:
            if 'title' in data and data['title']:
                data['slug'] = slugify(data['title'])
            else:
                raise serializers.ValidationError({
                    "title": "Le titre est requis pour générer le slug"
                })
        
        # Vérifier l'unicité du slug
        slug = data['slug']
        instance = self.instance
        
        if instance:
            # En update
            if BlogPost.objects.exclude(id=instance.id).filter(slug=slug).exists():
                raise serializers.ValidationError({"slug": "Ce slug existe déjà"})
        else:
            # En création
            if BlogPost.objects.filter(slug=slug).exists():
                raise serializers.ValidationError({"slug": "Ce slug existe déjà"})
        
        return data