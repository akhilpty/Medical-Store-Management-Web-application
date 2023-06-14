from medical_store.models import Medicine
from rest_framework import serializers


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ('__all__')