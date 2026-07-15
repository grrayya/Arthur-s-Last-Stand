import statistics
from oop import Knight, Dragon

def simulate_battles(trials=1000):
    wins = 0
    
    for _ in range(trials):
        arthur = Knight("Arthur", health=120, min_dmg=18, max_dmg=28, crit=0.25, flasks=2)
        smaug = Dragon("Smaug", health=350, min_dmg=15, max_dmg=25, scales=6)
        
        while arthur.is_alive() and smaug.is_alive():
            if arthur.hp <= 45 and arthur.flasks > 0:
                arthur.drink_flask()
            else:
                smaug.take_damage(arthur.roll_attack())
                
            if smaug.is_alive():
                arthur.take_damage(smaug.roll_attack())
                
        if arthur.is_alive():
            wins += 1
            
    return (wins / trials) * 100

if __name__ == "__main__":
    print("Running 10,000 headless encounters...")
    win_rate = simulate_battles(10000)
    print(f"Hero win rate: {win_rate:.2f}%")
