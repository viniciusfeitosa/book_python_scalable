def divided_by_two(values: list) -> list:
    resp = []
    for num in values:
        if num % 2 == 0:
            resp.append(num)
    return resp


def sum_num(values: list) -> int:
    resp = 0
    for value in values:
        resp += value
    return resp


def main() -> None:
    values = list(range(1_000_001))
    values = divided_by_two(values)
    value = sum_num(values)
    print('final value', value)


if __name__ == '__main__':
    import cProfile
    import pstats
    with cProfile.Profile() as p:
        main()
    stats = pstats.Stats(p)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    # stats.dump_stats('out.prof')
