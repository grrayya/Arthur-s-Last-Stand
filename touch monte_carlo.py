import random

arthur_health = 120
arthur_min, arthur_max = 15, 25
crit_rate = 0.25
dragon_hp = 300
dragon_min, dragon_max = 12, 22

def roll_attack(min_hit, max_hit, crit=0.0):
    base_swing = random.randint(min_hit, max_hit)
    
    if random.random() < crit:
        return int(base_swing * 1.5), True
    return base_swing, False

def start_brawl():
    global arthur_health, dragon_hp
    
    turn_count = 1
    while arthur_health > 0 and dragon_hp > 0:
        print(f"\n--- Turn {turn_count} ---")
        
        swing, is_crit = roll_attack(arthur_min, arthur_max, crit_rate)
        dragon_hp -= swing
        
        crit_indicator = " (CRIT!)" if is_crit else ""
        print(f"Arthur hits for {swing}{crit_indicator}. Dragon HP: {max(0, dragon_hp)}")
        
        if dragon_hp <= 0:
            print("Dragon slayed.")
            break
            
        breath_dmg, _ = roll_attack(dragon_min, dragon_max)
        arthur_health -= breath_dmg
        print(f"Dragon breathes fire for {breath_dmg}. Arthur HP: {max(0, arthur_health)}")
        
        if arthur_health <= 0:
            print("Arthur died.")
            break
            
        turn_count += 1

if __name__ == "__main__":
    start_brawl()
