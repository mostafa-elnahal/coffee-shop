import copy
import uuid
from datetime import datetime, timezone

from flask import abort;

from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

from api.schemas import ScheduleOrderSchema, ScheduleStatusSchema, GetScheduleOrderSchema, GetKitchenScheduleParameters

blueprint = Blueprint("kitchen", __name__, description="Kitchen API")

# mock schedule orders object

schedules = []

# define validation for order schedule base on GetScheduledOrderSchema
def validate_schedule(schedule):
    schedule = copy.deepcopy(schedule)
    errors = GetScheduleOrderSchema().validate(schedule)
    if errors:
        raise ValidationError(errors)

#endpoints

@blueprint.route("/kitchen/schedules")
class Schedules(MethodView):
    @blueprint.arguments(GetKitchenScheduleParameters, location="query")
    @blueprint.response(status_code=200, schema=GetScheduleOrderSchema(many=True))
    def get(self, parameters):
        for schedule in schedules:
            schedule = copy.deepcopy(schedule)
            errors = GetScheduleOrderSchema().validate(schedule)
            if errors:
                raise ValidationError(errors)
        query_set = schedules
        in_progress = parameters.get("in_progress")
        if in_progress is not None:
            if in_progress:
                query_set = [schedule for schedule in query_set if schedule["status"] == "in progress"]
            else:
                query_set = [schedule for schedule in query_set if schedule["status"] != "in progress"]
        since = parameters.get("since")
        if since is not None:
            query_set = [schedule for schedule in query_set if schedule["scheduled"] >= since]
        limit = parameters.get("limit")
        if limit is not None:
            query_set = query_set[:limit]
        return query_set, 200

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=201, schema=GetScheduleOrderSchema)
    def post(self, payload):
        payload['id'] = str(uuid.uuid4())
        payload['scheduled'] = datetime.now(timezone.utc)
        payload['status'] = 'pending'
        schedules.append(payload)
        validate_schedule(payload)
        return payload, 201

@blueprint.route("/kitchen/schedules/<schedule_id>")
class KitchenSchedule(MethodView):
    @blueprint.response(status_code=200, schema=GetScheduleOrderSchema)
    def get(self, schedule_id):
        """Get a scheduled order by ID"""
        for schedule in schedules:
            if schedule["id"] == schedule_id:
                validate_schedule(schedule)
                return schedule
            abort(404, message="Schedule not found")

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=200, schema=GetScheduleOrderSchema)
    def put(self, schedule_id, payload):
        for schedule in schedules:
            if schedule["id"] == schedule_id:
                schedule.update(payload)
                validate_schedule(schedule)
                return schedule
        abort(404, message="Schedule not found")
    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        for index, schedule in enumerate(schedules):
            if schedule["id"] == schedule_id:
                del schedules[index]
                return '', 204
        abort(404, message="Schedule not found")

@blueprint.route("/kitchen/schedules/<schedule_id>/cancel", methods=["POST"])
@blueprint.response(status_code=200, schema=GetScheduleOrderSchema)
def cancel_schedule(schedule_id):
    """Cancel a scheduled order by ID"""
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            schedule["status"] = "cancelled"
            validate_schedule(schedule)
            return schedule, 200
    abort(404, message="Schedule not found")
@blueprint.route("/kitchen/schedules/<schedule_id>/status", methods=["GET"])
@blueprint.response(status_code=200, schema=ScheduleStatusSchema)
def get_schedule_status(schedule_id):
    """Get the status of a scheduled order by ID"""
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            validate_schedule(schedule)
            return {"status": schedule["status"]}, 200
    abort(404, message="Schedule not found")
