from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'name', 'current_designation', 'experiences', 'skills', 'file', 'summary', 'created_at']

    def create(self, validated_data):
        return Resume.objects.create(**validated_data)

    def to_representation(self, instance):
        """Customize the output for the serialized instance."""
        representation = super().to_representation(instance)
        return representation