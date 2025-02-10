from settings import *

def load_existing_save(savefile):
    with open(os.path.join(savefile), 'r+') as file:
        data = json.load(file)
        
    return data

def write_save(data, path):
    with open(os.path.join(os.getcwd(),f"JSONS\{path}"), 'w') as file:
        json.dump(data, file)
        
def create_save():
    new_save = {
    "SurfaceOrderShop": {
        "Floor" : 3,
        "Decor"  : 4,
        "Interact" : 2,
        "Collisions" : 1,
        "SpawnPoints" : 0,
    },
    "SurfaceOrderCombat" : {
        "Collisions" : 0,
        "Spawns" : 1,
        "Decor" : 4,
        "Surface" : 3,
        "Background" : 2, 
    },
    "controls":
        {
        "Navigation" :{
            "Left": pygame.K_a, "Right": pygame.K_d, "Up": pygame.K_w, "Down": pygame.K_s, 
            "Start": pygame.K_RETURN, "Return": pygame.K_BACKSPACE},
        #ovdje se nalaze moguci potezi i njihov keybinds
        "Movement" : {
            #ovo je za generalno kretanje, ukljucuje i borbu i lika u exploraciji
            "Left" : pygame.K_a, "Right" : pygame.K_d, "Up" : pygame.K_w, "Down" : pygame.K_s, "Interact" : pygame.K_f,
            #ovo je dodatno za combat
            "Jump" : pygame.K_SPACE, "Sprint" : pygame.K_LCTRL, "Crouch" : pygame.K_LSHIFT, "Dash" : pygame.K_v
            },
        "Attacks" : 
            {
                "Normal" : pygame.K_0, "Ability" : pygame.K_1, "Special" : pygame.K_e, "Domain" : pygame.K_r},
            },

            


    
    "gameData": 
        {
        "Coins" : 0,

        "Player" : "PlayerSpawn",

        "Monsters" : {
            "Flying eye" : {"ATK" : 2, "HP" : 50, "Level" : 5},
            "Goblin" : {"ATK" : 2, "HP" : 50, "Level" : 5},
            "Mushroom" : {"ATK" : 2, "HP" : 50, "Level" : 5},
            "Skeleton" : {"ATK" : 2, "HP" : 50, "Level" : 5},
        },
        
        "Characters":
        {
            "Vergil" : {"ATK" : {"Val" : 10, "Price" : 20, "CE" : 10}, "HP" : {"Val" : 100, "Price" : 20}, "CE" : {"Val" : 100, "Price" : 20}, "ceRegen" : {"Val" : 1, "Price" : 20} , "Obtained" : {"Val" : False, "Price" : 1000}, "Level" : 10},
            "Wizard" : {"ATK" : {"Val" : 10, "Price" : 20, "CE" : 10}, "HP" : {"Val" : 100, "Price" : 20}, "CE" : {"Val" : 100, "Price" : 20}, "ceRegen" : {"Val" : 1, "Price" : 20} , "Obtained" : {"Val" : False, "Price" : 1000}, "Level" : 10},
            "LiuKang" : {"ATK" : {"Val" : 10, "Price" : 20, "CE" : 10}, "HP" : {"Val" : 100, "Price" : 20}, "CE" : {"Val" : 100, "Price" : 20}, "ceRegen" : {"Val" : 1, "Price" : 20} , "Obtained" : {"Val" : True, "Price" : 0}, "Level" : 10}
            },  
        "Wawe" : 10
        },
    }

    
    write_save(new_save, "Data\save.json")
    return new_save

def load_save():
    try:
    # Save is loaded 
        save = load_existing_save('JSONS\Data\save.json')
    except:
    # No save file, so create one
        save = create_save()
        write_save(save, "Data\save.json")
    return save

def reset_keys(actions):
    for action in actions:
        actions[action] = False
    return actions