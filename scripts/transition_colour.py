def transition_colour(colour_a, colour_b, deci=0.5):
    x = len(colour_b) - len(colour_a)
    if x > 0: colour_a = (colour_a[0], colour_a[1], colour_a[2], 255)
    elif x < 0: colour_b = (colour_b[0], colour_b[1], colour_b[2], 255)
    colour = []; inv = 1 - deci
    for i in range(len(colour_a)):
        colour.append(int(colour_a[i] * deci + colour_b[i] * inv))
    return colour