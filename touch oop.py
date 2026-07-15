
import random

class Entity:
    def __init__(self, name, health, min_dmg, max_dmg):
        self.name = name
        self.max_hp = health
        self.hp = health
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        
    def is_alive(self):
        return self.hp > 0
        
    def take_damage(self, hit):
        self.hp = max(0, self.hp - hit)

    def roll_attack(self):
        return random.randint(self.min_dmg, self.max_dmg)

class Knight(Entity):
    def __init__(self, name, health, min_dmg, max_dmg, crit, flasks):
        super().__init__(name, health, min_dmg, max_dmg)
        self.crit = crit
        self.flasks = flasks
        
    def roll_attack(self):
        base_hit = super().roll_attack()
        if random.random() < self.crit:
            print(f"** {self.name} crits! **")
            return int(base_hit * 1.5)
        return base_hit
        
    def drink_flask(self):
        if self.flasks > 0:
            # hardcoding 50 for now, should probably scale this later
            self.hp = min(self.max_hp, self.hp + 50)
            self.flasks -= 1
            print(f"{self.name} drinks estus. 50 HP restored. ({self.flasks} left)")
            return True
        return False

class Dragon(Entity):
    def __init__(self, name, health, min_dmg, max_dmg, scales):
        super().__init__(name, health, min_dmg, max_dmg)
        self.scales = scales
        
    def take_damage(self, hit):
        mitigated = max(1, hit - self.scales)
        super().take_damage(mitigated)
        return mitigated

def run_encounter():
    player = Knight("Arthur", health=120, min_dmg=18, max_dmg=28, crit=0.25, flasks=2)
    boss = Dragon("Smaug", health=350, min_dmg=15, max_dmg=25, scales=6)
    
    round_idx = 1
    while player.is_alive() and boss.is_alive():
        print(f"\n--- Round {round_idx} ---")
        
        if player.hp <= 45 and player.flasks > 0:
            player.drink_flask()
        else:
            swing = player.roll_attack()
            actual_dmg = boss.take_damage(swing)
            print(f"{player.name} slashes {boss.name} for {actual_dmg}. ({boss.name}: {boss.hp})")
            
        if not boss.is_alive():
            print(f"\n{boss.name} goes down.")
            break
            
        boss_hit = boss.roll_attack()
        player.take_damage(boss_hit)
        print(f"{boss.name} tail swipes for {boss_hit}. ({player.name}: {player.hp})")
        
        if not player.is_alive():
            print(f"\n{player.name} died.")
            
        round_idx += 1

if __name__ == "__main__":
    run_encounter()
