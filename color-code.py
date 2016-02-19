#!/usr/bin/env python
import argparse
import io
import sys
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('output')
    args = parser.parse_args()

    with io.open(args.output, 'wb') as output:
        subprocess.check_call(
            (sys.executable, '-m', 'color_code'),
            env={'FILENAME': args.filename},
            stdout=output,
        )

if __name__ == '__main__':
    exit(main())
