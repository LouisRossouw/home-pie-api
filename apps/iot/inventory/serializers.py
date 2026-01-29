from rest_framework import serializers
from .models import StorageUnit, Compartment, Part, Inventory


class StorageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageUnit
        fields = ["id", "name", "description", "location"]


class CompartmentSerializer(serializers.ModelSerializer):
    low_quantity = serializers.ReadOnlyField()

    class Meta:
        model = Compartment
        fields = [
            "id", "storage_unit", "name", "led_address_start", "led_address_end",
            "led_count", "max_quantity", "low_quantity_threshold", "current_quantity", "low_quantity"
        ]


class InventorySerializer(serializers.ModelSerializer):
    part_name = serializers.ReadOnlyField(source="part.name")
    compartment_name = serializers.ReadOnlyField(source="compartment.name")

    class Meta:
        model = Inventory
        fields = ["id", "part", "compartment",
                  "quantity", "part_name", "compartment_name"]


class PartSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(
        source="inventory_set", many=True, read_only=True)

    class Meta:
        model = Part
        fields = [
            "id", "name", "description", "sku", "manufacturer", "part_number",
            "category", "value", "tolerance", "voltage_rating", "package_type",
            "quantity", "inventory"
        ]
