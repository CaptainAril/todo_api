from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('creator', 'collaborators', 'created_at', 'updated_at', 'status')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['priority'].error_messages['invalid_choice'] = f'Invalid priority value. Allowed values: {", ".join([str(priority[0]) for priority in Todo.PRIORITY_CHOICES])}'
        self.fields['status'].error_messages['invalid_choice'] = f'Invalid status value. Allowed values: {", ".join([status[0] for status in Todo.STATUS_CHOICES])}'
    
    def create(self, validated_data):
        print(validated_data)  
        return Todo.objects.create(**validated_data)

@extend_schema_serializer(
    component_name="TodoColaborator"
)
class TodoCollaboratorSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    collaborator_id = serializers.CharField()