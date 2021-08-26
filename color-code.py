#!/usr/bin/env python
import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('output')
    parser.add_argument('--widths', action='store_true')
    parser.add_argument('--name', required=True)
    parser.add_argument('--seed-color')
    args = parser.parse_args()
    args.name = args.name or args.filename

    with open(args.output, 'wb') as output:
        return subprocess.call(
            (sys.executable, '-m', 'color_code'),
            env={
                'FILENAME': args.filename,
                'NAME': args.name,
                'SEED_COLOR':  str(args.seed_color),
                'WIDTHS': str(args.widths),
            },
            stdout=output,
        )


if __name__ == '__main__':
    exit(main())
