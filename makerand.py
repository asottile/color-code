import random


def n() -> int:
    val = random.normalvariate(110, 45)
    val = max(0, val)
    val = min(255, val)

    if val > 127:
        val = 127 + (255 - val)
    else:
        val = 127 - val

    return int(val)


def main() -> int:
    with open('f2', 'wb') as f:
        f.write(bytes(n() for _ in range(2048)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
