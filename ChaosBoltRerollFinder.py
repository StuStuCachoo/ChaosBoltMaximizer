from random import randrange


def roll(level: int, max_rolls: int, d8_reroll_values: list, d6_reroll_values: list, armor_class: int, to_hit: int):
    d1 = randrange(1, 9, 1)
    d2 = randrange(1, 9, 1)
    final = 0
    rerolls = max_rolls
    rerollable = []
    for i in range(level):
        cur_roll = randrange(1, 7, 1)
        # while rerolls > 0 and cur_roll <d6_reroll_values[rerolls-1]:
        #	cur_roll = randrange(1,7,1)
        #	rerolls=rerolls-1
        final += cur_roll
        if cur_roll < 4:
            rerollable.append([cur_roll, 6])
    while rerolls > 0 or d1 == d2:
        if d1 != d2:
            if d1 > d8_reroll_values[rerolls - 1] and d2 > d8_reroll_values[rerolls - 1]:
                break
            elif d1 < d2:
                d1 = randrange(1, 9, 1)
            else:
                d2 = randrange(1, 9, 1)
            rerolls -= 1
        else:
            final += d1 + d2
            if randrange(1, 21, 1) + to_hit >= armor_class:
                for i in range(0, level):
                    cur_roll = randrange(1, 7, 1)
                    final += cur_roll
                    if cur_roll < 4:
                        rerollable.append([cur_roll, 6])
                d1 = randrange(1, 9, 1)
                d2 = randrange(1, 9, 1)
            else:
                break
    while rerolls > 0 and rerollable:
        max_under_average = [(rerollable[0][1] + 1) / 2 - rerollable[0][0], 0]
        for i in range(len(rerollable)):
            if (rerollable[i][1] + 1) / 2 - rerollable[i][0] > max_under_average[0]:
                max_under_average = [(rerollable[i][1] + 1) / 2 - rerollable[i][0], i]
        dice_type = rerollable[max_under_average[1]][1]
        final -= rerollable[max_under_average[1]][0]
        rerollable.pop(max_under_average[1])
        rerolls -= 1
        cur_roll = randrange(1, dice_type + 1, 1)
        final += cur_roll
        if cur_roll < 4 and dice_type == 6 or cur_roll < 5 and dice_type == 8:
            rerollable.append([cur_roll, dice_type])
    final += d1 + d2
    return final


def reroll_arrays(die_min: int, die_max: int, rerolls: int):
    base = [die_min] * rerolls
    return_array = [base.copy()]
    while base != [die_max] * rerolls:
        base = increment(base, die_max, rerolls - 1)
        if sorted(base) == base:
            return_array.append(base.copy())
    return return_array


def increment(in_list: list, die_max: int, column: int):
    if in_list[column] == die_max:
        in_list[column] = 0
        return increment(in_list, die_max, column - 1)
    in_list[column] = in_list[column] + 1
    return in_list


def sim_rolls(level: int, max_rerolls: int, armor_class: int, to_hit: int, num_simulations: int) -> None:
    d8_arrays = reroll_arrays(5, 8, max_rerolls)
    d6_arrays = reroll_arrays(1, 4, max_rerolls)
    for i in range(len(d8_arrays)):
        for j in range(len(d6_arrays)):
            sum = 0  # type: int
            for k in range(num_simulations):
                sum += roll(level, max_rerolls, d8_arrays[i], d6_arrays[j], armor_class, to_hit)
            sum = sum / num_simulations
            print('{0]-{1}: {2}'.format(d8_arrays[i], d6_arrays[j], sum))
