def format_population(population):
    if population > 1_000_000:
        population_m = population / 1_000_000
        return f'{population_m:1.1f}M'
    if population > 1_000:
        population_k = population / 1_000
        return f'{population_k:2.0f}K'
    return population
