from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, TagViewSet, CommentCreateDeleteView


router = DefaultRouter()
router.register('product', ProductViewSet, 'product')
router.register('comment', CommentCreateDeleteView, 'comment')
router.register('tag', TagViewSet, 'tag')
urlpatterns = []
urlpatterns += router.urls