from memory_profiler import profile


@profile
def main() -> int:
    l1 = [value for value in range(1_000_000)]
    l2 = [value+value for value in range(1_000_000)]
    return sum(l1) + sum(l2)


if __name__ == '__main__':
    main()
