from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('creator', 'collaborators', 'created_at', 'updated_at')
        
    def create(self, validated_data):
        print(validated_data)  
        return Todo.objects.create(**validated_data)
    



@extend_schema_serializer(
    component_name="TodoColaborator"
)
class TodoCollaboratorSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    collaborator_id = serializers.CharField()