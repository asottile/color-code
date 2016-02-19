#!/usr/bin/env python
import argparse
import io
import sys
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('output')
    parser.add_argument('--widths', action='store_true')
    args = parser.parse_args()

    with io.open(args.output, 'wb') as output:
        subprocess.check_call(
            (sys.executable, '-m', 'color_code'),
            env={'FILENAME': args.filename, 'WIDTHS': str(args.widths)},
            stdout=output,
        )

if __name__ == '__main__':
    exit(main())
