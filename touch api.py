from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from oop import Knight, Dragon

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_battles = {}

class BattleStatus(BaseModel):
    session_id: str
    hero_hp: int
    boss_hp: int
    flasks: int
    log: list[str]
    game_over: bool

@app.post("/start/{session_id}")
def start_encounter(session_id: str):
    active_battles[session_id] = {
        "hero": Knight("Arthur", 120, 18, 28, 0.25, 2),
        "boss": Dragon("Smaug", 350, 15, 25, 6),
        "log": ["A wild Smaug appears."]
    }
    return get_status(session_id)

@app.get("/status/{session_id}", response_model=BattleStatus)
def get_status(session_id: str):
    if session_id not in active_battles:
        raise HTTPException(status_code=404, detail="Battle not found")
        
    battle = active_battles[session_id]
    hero = battle["hero"]
    boss = battle["boss"]
    
    return {
        "session_id": session_id,
        "hero_hp": hero.hp,
        "boss_hp": boss.hp,
        "flasks": hero.flasks,
        "log": battle["log"][-5:], # just send the last 5 events
        "game_over": not hero.is_alive() or not boss.is_alive()
    }

@app.post("/action/{session_id}")
def execute_turn(session_id: str, action: str):
    if session_id not in active_battles:
        raise HTTPException(status_code=404)
        
    battle = active_battles[session_id]
    hero = battle["hero"]
    boss = battle["boss"]
    
    if not hero.is_alive() or not boss.is_alive():
        return get_status(session_id)
        
    # Player Turn
    if action == "attack":
        dmg = hero.roll_attack()
        mitigated = boss.take_damage(dmg)
        battle["log"].append(f"Arthur hits for {mitigated}.")
    elif action == "flask":
        if hero.drink_flask():
            battle["log"].append("Arthur drinks a flask. HP +50.")
        else:
            battle["log"].append("Out of flasks!")
            return get_status(session_id) # free turn if they mess up
            
    if not boss.is_alive():
        battle["log"].append("Smaug is dead. You win!")
        return get_status(session_id)
        
    # Boss Turn
    boss_dmg = boss.roll_attack()
    hero.take_damage(boss_dmg)
    battle["log"].append(f"Smaug retaliates for {boss_dmg}.")
    
    if not hero.is_alive():
        battle["log"].append("Arthur died. Game Over.")
        
    return get_status(session_id)
