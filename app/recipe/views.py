"""views for recipe api."""
from core.models import Recipe
from recipe import serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        """create a new recipe"""
        serializer.save(user=self.request.user)
