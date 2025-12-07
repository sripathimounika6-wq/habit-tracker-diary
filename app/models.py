"""Habit model supporting diary entries with 'done', 'notes', 'date'."""

import os
import time
import uuid
import logging

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except Exception:
    boto3 = None

logger = logging.getLogger(__name__)

TABLE_NAME = os.environ.get("DDB_TABLE", "HabitTracker")
REGION = os.environ.get("AWS_REGION", "eu-west-1")
USE_DYNAMODB = os.environ.get("USE_DYNAMODB", "0") == "1"


def _has_aws_credentials():
    if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
        return True
    return False


class HabitModel:
    def __init__(self):
        self.table = None
        self._store = {}
        if USE_DYNAMODB and boto3 and _has_aws_credentials():
            try:
                self.dynamodb = boto3.resource("dynamodb", region_name=REGION)
                self.table = self.dynamodb.Table(TABLE_NAME)
                logger.info("DynamoDB enabled for HabitModel")
            except Exception as e:
                logger.warning(
                    "DynamoDB init failed, falling back to memory store: %s",
                    e,
                )
                self.table = None
        else:
            logger.info(
                "Using in-memory store for HabitModel (USE_DYNAMODB=%s)",
                USE_DYNAMODB,
            )

    def _make_item(self, user_id, data):
        hid = str(uuid.uuid4())
        return {
            "id": hid,
            "user_id": user_id,
            "title": data.get("title"),
            "frequency": data.get("frequency", "daily"),
            "done": bool(data.get("done", False)),
            "notes": data.get("notes"),
            "date": data.get("date"),
            "created_at": int(time.time()),
        }

    def create_habit(self, user_id, data):
        item = self._make_item(user_id, data)
        if self.table:
            try:
                item["type"] = "habit"
                self.table.put_item(Item=item)
            except Exception as e:
                logger.error("Dynamo put failed, storing in-memory: %s", e)
                self._store.setdefault(user_id, {})[item["id"]] = item
        else:
            self._store.setdefault(user_id, {})[item["id"]] = item
        return item

    def list_habits(self, user_id):
        if self.table:
            try:
                resp = self.table.query(
                    IndexName="user_idx",
                    KeyConditionExpression=Key("user_id").eq(user_id),
                )
                return resp.get("Items", [])
            except Exception:
                try:
                    resp = self.table.scan()
                    return [
                        it
                        for it in resp.get("Items", [])
                        if it.get("user_id") == user_id
                    ]
                except Exception as e:
                    logger.error("Dynamo scan failed: %s", e)
                    return list(self._store.get(user_id, {}).values())
        return list(self._store.get(user_id, {}).values())

    def update_habit(self, user_id, hid, data):
        # partial update: only update fields present in data
        if self.table:
            try:
                # In Dynamo mode we replace the item for simplicity
                item = {
                    "id": hid,
                    "user_id": user_id,
                    "title": data.get("title"),
                    "frequency": data.get("frequency", "daily"),
                    "done": bool(data.get("done", False)),
                    "notes": data.get("notes"),
                    "date": data.get("date"),
                    "updated_at": int(time.time()),
                    "type": "habit",
                }
                self.table.put_item(Item=item)
                return item
            except Exception as e:
                logger.error("Dynamo update failed: %s", e)
        # in-memory update
        if user_id in self._store and hid in self._store[user_id]:
            obj = self._store[user_id][hid]
            for k, v in data.items():
                if k in ["title", "frequency", "done", "notes", "date"]:
                    obj[k] = v
            obj["updated_at"] = int(time.time())
            return obj
        return None

    def delete_habit(self, user_id, hid):
        if self.table:
            try:
                self.table.delete_item(Key={"id": hid})
                return True
            except Exception as e:
                logger.error("Dynamo delete failed: %s", e)
        if user_id in self._store and hid in self._store[user_id]:
            del self._store[user_id][hid]
            return True
        return False
