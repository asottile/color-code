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
    parser.add_argument('--name')
    args = parser.parse_args()
    args.name = args.name or args.filename

    with io.open(args.output, 'wb') as output:
        subprocess.check_call(
            (sys.executable, '-m', 'color_code'),
            env={
                'FILENAME': args.filename, 'WIDTHS': str(args.widths),
                'NAME': args.name,
            },
            stdout=output,
        )

if __name__ == '__main__':
    exit(main())
