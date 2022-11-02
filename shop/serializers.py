from dataclasses import fields
from email.policy import default
from requests import request
from rest_framework import serializers
from django.db.models import Avg
from .models import(
    Category,
    Product,
    ProductImage,
    Tag,
    Comment,
)

class CategoryListSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Category
        fields = ('name', 'slug')


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('user', 'name', 'image', 'slug')


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = 'image',


class ProductCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    carousel_img = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        tag = validated_data.pop('tag')
        product = Product.objects.create(**validated_data)
        product.tag.set(tag)
        images = []
        for image in carousel_images:
            images.append(ProductImage(product=product, image=image))
        ProductImage.objects.bulk_create(images)
        return product


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = Comment
        exclude = ['product']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def validate(self, attrs):
        tag = attrs.get('name')
        if Tag.objects.filter(name=tag).exists():
            raise serializers.ValidationError('Tag with this name already exists')
        return attrs


#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['comments'] = CommentSerializer(
#             instance.comments.all(), many=True).data
#         representation['carousel'] = PostImageSerializer(
#             instance.post_images.all(), many=True).data
#         rating = instance.ratings.aggregate(Avg('rating'))['rating__avg']
#         # representation['likes'] = instance.likes.all().count()
#         # representation['liked_by'] = LikeSerializer(instance.likes.all().only('user'), many=True).data
#         if rating:
#             representation['rating'] = round(rating, 1)
#         else:
#             representation['rating'] = 0.0
#         return representation


# class PostImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PostImage
#         fields = 'image',


# class PostCreateSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(
#         default=serializers.CurrentUserDefault(),
#         source='user.username'
#     )
#     carousel_img = serializers.ListField(
#         child=serializers.ImageField(),
#         write_only=True
#     )

#     class Meta:
#         model = Post
#         fields = '__all__'
    
#     def create(self, validated_data):
#         carousel_images = validated_data.pop('carousel_img')
#         tag = validated_data.pop('tag')
#         post = Post.objects.create(**validated_data)
#         post.tag.set(tag)
#         images = []
#         for image in carousel_images:
#             images.append(PostImage(post=post, image=image))
#         PostImage.objects.bulk_create(images)
#         return post


# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(
#         default=serializers.CurrentUserDefault(),
#         source='user.username'
#     )

#     class Meta:
#         model = Comment
#         exclude = ['post']


# class RatingSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(
#         source='user.username'
#     )
    
#     class Meta:
#         model = Rating
#         fields = ('rating', 'user', 'post')
        
#     def validate(self, attrs):
#         user = self.context.get('request').user
#         attrs['user'] = user
#         rating = attrs.get('rating')
#         if rating not in (1, 2, 3, 4, 5):
#             raise serializers.ValidationError('Wrong value! Rating must be between from 1 to 5'
#             )
#         return attrs

#     def update(self, instance, validated_data):
#         instance.rating = validated_data.get('rating')
#         return super().update(instance, validated_data)


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = '__all__'

#     def validate(self, attrs):
#         tag = attrs.get('title')
#         if Tag.objects.filter(title=tag).exists():
#             raise serializers.ValidationError('Tag with this name already exists')
#         return attrs


# class CurrentPostDefault:
#     requires_context = True

#     def __call__(self, serializer_field):
#         return serializer_field.context['post']


# class LikeSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     post = serializers.HiddenField(default=CurrentPostDefault())

#     class Meta:
#         model = Like
#         fields = '__all__'

#     def create(self, validated_data):
#         user = self.context.get('request').user
#         post = self.context.get('post').pk
#         like = Like.objects.filter(user=user, post=post).first()
#         if like:
#             raise serializers.ValidationError('You have already liked this post!')
#         return super().create(validated_data)

#     def unlike(self):
#         user = self.context.get('request').user
#         post = self.context.get('post').pk
#         like = Like.objects.filter(user=user, post=post).first()
#         if like:
#             like.delete()
#         else:
#             raise serializers.ValidationError('Not liked yet!')


# class LikedPostSerializer(serializers.ModelSerializer):
#     url = serializers.URLField(source='post.get_absolute_url')
#     post = serializers.ReadOnlyField(source='post.title')

#     class Meta:
#         model = Like
#         fields = ['post', 'user', 'url']