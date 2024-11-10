class Colour:
    # Block Colours:
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    # Theme Colours
    kaycee_red = (144, 42, 53)
    kaycee_scarlet = (209, 52, 78)
    light_red = (142, 21, 51)
    dark_red = (101, 28, 58)
    light_orange = (225, 146, 38)
    orange = (237, 112, 35)
    light_brown = (113, 68, 49)
    brown = (85, 56, 47)
    dark_brown = (58, 45, 45)
    light_green = (193, 208, 128)
    green = (83, 170, 115)
    light_blue = (18, 124, 107)
    blue = (15, 92, 93)
    dark_blue = (10, 56, 71)
    light_grey = (62, 75, 80)
    grey = (49, 64, 70)
    dark_grey = (31, 44, 49)
    ink = (46, 61, 66)
    
    # Cost Colours
    blood_red = (129, 27, 56)
    light_blood = (159, 63, 51)
    bone_white = (215, 226, 163)
    greyed_bone = (160, 170, 124)
    dark_bone = (108, 117, 89)
    onyx_black = (48, 59, 82)
    dark_onyx = (31, 37, 51)
    emerald_green = (156, 191, 85)
    dark_emerald = (97, 149, 50)
    ruby_orange = (228, 127, 45)
    dark_ruby = (190, 74, 42)
    sapphire_blue = (87, 160, 112)
    dark_sapphire = (50, 103, 99)
    light_teal = (180, 255, 236)
    energy_teal = (149, 254, 217)
    dark_teal = (102, 178, 157)
    metal_grey = (79, 79, 79)
    dark_metal = (51, 51, 51)
    light_gold = (255, 232, 128) 
    gold = (240, 192, 48)
    dark_gold = (188, 126, 16)
    
class ColourPalette:
    Leshy = {'Dark Trim': Colour.orange, 'Light Trim': Colour.light_orange, 'Block': Colour.brown, 'Light Block': Colour.light_brown, 'Dark Block': Colour.dark_brown, 'Background': Colour.dark_brown}
    Grimora = {'Dark Trim': Colour.green, 'Light Trim': Colour.light_green, 'Block': Colour.blue, 'Light Block': Colour.light_blue, 'Dark Block': Colour.dark_blue, 'Background': Colour.dark_blue}
    #Magnificus = {'Dark Trim', 'Light Trim', 'Block', 'Light Block', 'Dark Block', 'Background'}
    P03 = {'Dark Trim': Colour.energy_teal, 'Light Trim': Colour.light_teal, 'Block': Colour.grey, 'Light Block': Colour.light_grey, 'Dark Block': Colour.dark_grey, 'Background': Colour.dark_grey}
    Moon = {'Dark Trim', 'Light Trim', 'Block', 'Light Block', 'Dark Block', 'Background'}
    by_index = {1: Leshy,
                2: Grimora,
                #3: Magnificus,
                4: P03,
                #5: Galliard,
                6: Moon}
