#!/usr/bin/env python
from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('output')
    parser.add_argument('--widths', action='store_true')
    parser.add_argument('--name', required=True)
    args = parser.parse_args()
    args.name = args.name or args.filename

    with open(args.output, 'wb') as output:
        return subprocess.call(
            (sys.executable, '-m', 'color_code'),
            env={
                'FILENAME': args.filename, 'WIDTHS': str(args.widths),
                'NAME': args.name,
            },
            stdout=output,
        )


if __name__ == '__main__':
    raise SystemExit(main())
