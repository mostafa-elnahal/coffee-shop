from marshmallow import Schema, fields, validate, EXCLUDE

class OrderItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    product = fields.String(required=True)
    size = fields.String(required=True, validate=validate.OneOf(["Small", "Medium", "Large"]))
    quantity = fields.Integer(validate=validate.Range(min=1, min_inclusive=True), required=True)

class ScheduleSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    order = fields.Nested(OrderItemSchema, required=True)

class ScheduleOrderSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    order = fields.List(fields.Nested(OrderItemSchema), required=True)
    scheduled = fields.DateTime(required=False)

class GetScheduleOrderSchema(ScheduleOrderSchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.String(required=True)
    status = fields.String(
        required=True,
        validate=validate.OneOf(
            ["pending", "progress", "cancelled", "finished"]
        ),
    )
    order = fields.List(fields.Nested(OrderItemSchema), required=True)
    # by default DateTime() in marshmallow is iso format by default
    scheduled = fields.DateTime(required=True)

class ScheduleStatusSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    status = fields.String(
        required=True,
        validate=validate.OneOf(
            ["pending", "progress", "cancelled", "finished"]
        ),
    )

class GetKitchenScheduleParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    progress = fields.Boolean()
    limit = fields.Integer()
    since = fields.DateTime()