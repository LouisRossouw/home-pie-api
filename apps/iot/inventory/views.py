from rest_framework import viewsets
from rest_framework.decorators import action
from .models import StorageUnit, Compartment, Part, Inventory
from .serializers import StorageUnitSerializer, CompartmentSerializer, PartSerializer, InventorySerializer
from rest_framework.response import Response
from .decorators import storage_unit_schema, compartment_schema, inventory_schema, part_schema


@storage_unit_schema
class StorageUnitViewSet(viewsets.ModelViewSet):
    queryset = StorageUnit.objects.all()
    serializer_class = StorageUnitSerializer


@compartment_schema
class CompartmentViewSet(viewsets.ModelViewSet):
    queryset = Compartment.objects.all()
    serializer_class = CompartmentSerializer

    @action(detail=True, methods=['post'])
    def light_up(self, request, pk=None):
        compartment = self.get_object()
        unit = compartment.storage_unit

        # TODO; Not sure yet about the colour codes needed for neopixel
        colour = request.data.get("colour", "RGB(255, 255, 255)")

        payload = {
            "start": compartment.led_address_start,
            "end": compartment.led_address_end,
            "colour": colour
        }

        # TODO; Should we define the url for each compartment? or .. ??
        result = esp32_post(f"{unit.base_url}/light", payload)

        return Response({"device_response": result}, status=status.HTTP_200_OK)


@part_schema
class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer


@inventory_schema
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
