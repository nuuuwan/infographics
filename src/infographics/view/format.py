

def format_population(population):
    if population > 1_000_000:
        population_x = population / 1_000_000
        return f'{population_x:1.1f}M'
    if population > 100_000:
        population_x = population / 10_000
        return f'{population_x:2.0f}0K'

    if population > 10_000:
        population_x = population / 1_000
        return f'{population_x:2.0f}K'

    if population > 1_000:
        population_x = population / 1_000
        return f'{population_x:1.1f}K'

    if population > 1_00:
        population_x = population / 10
        return f'{population_x:2.0f}0'

    return f'{population:2.0f}'
