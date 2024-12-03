import json

with open("consts.json", "r") as f:
    consts = json.load(f)

ACTIVITY_ID = consts["activity_id"]
GET_SCORE_FLOW_ID = consts["flow_id"]
FLOW_ID = consts["exchange_flow_id"]
ITEMS = consts["packages"]
