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
            print(f"** {self.name} lands a critical strike! **")
            return int(base_hit * 1.5)
        return base_hit
        
    def drink_flask(self):
        if self.flasks > 0:
            self.hp = min(self.max_hp, self.hp + 50)
            self.flasks -= 1
            print(f"{self.name} chugs a flask. 50 HP restored. ({self.flasks} left)")
            return True
        return False

class Dragon(Entity):
    def __init__(self, name, health, min_dmg, max_dmg, scales):
        super().__init__(name, health, min_dmg, max_dmg)
        self.scales = scales  # flat damage reduction
        
    def take_damage(self, hit):
        mitigated = max(1, hit - self.scales)
        super().take_damage(mitigated)
        return mitigated

def run_encounter():
    arthur = Knight("Arthur", health=120, min_dmg=18, max_dmg=28, crit=0.25, flasks=2)
    smaug = Dragon("Smaug", health=350, min_dmg=15, max_dmg=25, scales=6)
    
    turn = 1
    while arthur.is_alive() and smaug.is_alive():
        print(f"\n--- Turn {turn} ---")
        
        # heal if low, otherwise attack
        if arthur.hp <= 45 and arthur.flasks > 0:
            arthur.drink_flask()
        else:
            swing = arthur.roll_attack()
            actual_dmg = smaug.take_damage(swing)
            print(f"{arthur.name} hits {smaug.name} for {actual_dmg}. ({smaug.name}: {smaug.hp})")
            
        if not smaug.is_alive():
            print(f"\n{smaug.name} is defeated.")
            break
            
        boss_hit = smaug.roll_attack()
        arthur.take_damage(boss_hit)
        print(f"{smaug.name} tail swipes for {boss_hit}. ({arthur.name}: {arthur.hp})")
        
        if not arthur.is_alive():
            print(f"\n{arthur.name} died.")
            
        turn += 1

if __name__ == "__main__":
    run_encounter()
