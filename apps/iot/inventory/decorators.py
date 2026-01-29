from drf_spectacular.utils import extend_schema

storage_unit_schema = extend_schema(
    tags=["iot-inventory"],
)

compartment_schema = extend_schema(
    tags=["iot-inventory"],
)

part_schema = extend_schema(
    tags=["iot-inventory"],
)

inventory_schema = extend_schema(
    tags=["iot-inventory"],
)
