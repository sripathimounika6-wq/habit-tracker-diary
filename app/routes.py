"""
Public habit/diary endpoints without authentication.
Uses HabitSchema for creating and UpdateHabitSchema for updates.
"""
from flask import Blueprint, request, jsonify
from .models import HabitModel
from .validators import HabitSchema, UpdateHabitSchema, ValidationError
import logging

logger = logging.getLogger(__name__)
bp = Blueprint("api", __name__)
model = HabitModel()


def get_user_id():
    return request.headers.get("X-User-Id", "anonymous")


@bp.route("/habits", methods=["POST"])
def create_habit():
    user_id = get_user_id()
    try:
        data = HabitSchema.validate(request.json or {})
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    try:
        item = model.create_habit(user_id, data)
        return jsonify(item), 201
    except Exception:
        logger.exception("create_habit failed")
        return jsonify({"error": "internal error"}), 500


@bp.route("/habits", methods=["GET"])
def list_habits():
    user_id = get_user_id()
    try:
        items = model.list_habits(user_id)
        items_sorted = sorted(items, key=lambda x: x.get("created_at", 0), reverse=True)
        return jsonify(items_sorted), 0 if isinstance(items_sorted, int) else 200
    except Exception:
        logger.exception("list_habits failed")
        return jsonify([]), 200


@bp.route("/habits/<string:hid>", methods=["PUT", "PATCH"])
def update_habit(hid):
    """
    Accept partial updates. Use UpdateHabitSchema so only provided keys are validated.
    Example: {"done": true} will toggle the done state without title required.
    """
    user_id = get_user_id()
    try:
        data = UpdateHabitSchema.validate(request.json or {})
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    # If no fields provided, return 400
    if not data:
        return jsonify({"error": "no fields to update provided"}), 400

    try:
        item = model.update_habit(user_id, hid, data)
        if not item:
            return jsonify({"error": "not found"}), 404
        return jsonify(item), 200
    except Exception:
        logger.exception("update_habit failed")
        return jsonify({"error": "internal error"}), 500


@bp.route("/habits/<string:hid>", methods=["DELETE"])
def delete_habit(hid):
    user_id = get_user_id()
    ok = model.delete_habit(user_id, hid)
    return jsonify({"deleted": ok}), (200 if ok else 404)
