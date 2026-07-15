import random

arthur_hp = 120
arthur_min_dmg, arthur_max_dmg = 15, 25
crit_chance = 0.25

smaug_hp = 300
smaug_min_dmg, smaug_max_dmg = 12, 22

def roll_swing(min_hit, max_hit, crit=0.0):
    base_dmg = random.randint(min_hit, max_hit)
    
    if random.random() < crit:
        return int(base_dmg * 1.5), True
    return base_dmg, False

def start_brawl():
    global arthur_hp, smaug_hp
    
    round_idx = 1
    while arthur_hp > 0 and smaug_hp > 0:
        print(f"\n--- Round {round_idx} ---")
        
        # arthur attacks
        swing, is_crit = roll_swing(arthur_min_dmg, arthur_max_dmg, crit_chance)
        smaug_hp -= swing
        
        crit_tag = " (CRIT!)" if is_crit else ""
        print(f"Arthur slashes for {swing}{crit_tag}. Smaug HP: {max(0, smaug_hp)}")
        
        if smaug_hp <= 0:
            print("Smaug falls. Arthur wins.")
            break
            
        # smaug hits back
        breath, _ = roll_swing(smaug_min_dmg, smaug_max_dmg)
        arthur_hp -= breath
        print(f"Smaug breathes fire for {breath}. Arthur HP: {max(0, arthur_hp)}")
        
        if arthur_hp <= 0:
            print("Arthur died.")
            break
            
        round_idx += 1

if __name__ == "__main__":
    start_brawl()
