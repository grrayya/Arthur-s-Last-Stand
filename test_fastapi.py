from fastapi.testclient import TestClient
from api import app, active_battles

client = TestClient(app)

def test_start_encounter_creates_battle_state():
    resp = client.post("/start/session1")
    assert resp.status_code == 200
    body = resp.json()
    assert body["hero_hp"] == 120
    assert body["boss_hp"] == 350
    assert body["game_over"] is False


def test_status_404_for_unknown_session():
    resp = client.get("/status/ghost")
    assert resp.status_code == 404


def test_attack_action_damages_boss():
    client.post("/start/session2")
    resp = client.post("/action/session2", params={"action": "attack"})
    assert resp.json()["boss_hp"] < 350

def test_flask_action_out_of_flasks_logs_and_skips_boss_turn():
    client.post("/start/session3")
    active_battles["session3"]["hero"].flasks = 0
    resp = client.post("/action/session3", params={"action": "flask"})
    body = resp.json()
    assert resp.status_code == 200
    assert body["log"][-1] == "Out of flasks!"
    assert body["hero_hp"] == 120 

def test_action_on_missing_session_returns_404():
    resp = client.post("/action/nowhere", params={"action": "attack"})
    assert resp.status_code == 404
