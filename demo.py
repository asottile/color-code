import argparse
import contextlib
import os.path
import random
import shutil
import subprocess
import sys
import tempfile
import urllib


DOWNLOAD = (
    (
        'dumb-init',
        'https://github.com/Yelp/dumb-init/releases/download/v1.0.0/'
        'dumb-init_1.0.0_amd64',
    ),
    (
        'pip_faster.py',
        'https://raw.githubusercontent.com/Yelp/pip-faster/'
        '275da8/pip_faster.py',
    ),
    (
        'yelp.com-logo.png',
        'https://s3-media2.fl.yelpcdn.com/assets/srv0/yelp_styleguide/'
        'e0bcd848f6ae/assets/img/logos/header_logo.png',
    ),
    (
        'pre-commit-favicon',
        'http://pre-commit.com/favicon.ico',
    )
)

ON_DISK = (
    '/bin/echo',
    '/bin/cat',
    'venv/lib/python2.7/site.pyc',
)


@contextlib.contextmanager
def tempdir():
    tmp = tempfile.mkdtemp()
    try:
        yield tmp
    finally:
        shutil.rmtree(tmp)


def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.exists(path):
            raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir')
    args = parser.parse_args()

    mkdirp(args.output_dir)

    with tempdir() as tmpdir:
        for name, url in DOWNLOAD:
            resp = urllib.urlopen(url)
            path = os.path.join(tmpdir, 'tmpfile')
            with open(path, 'wb') as f:
                f.write(resp.read())

            subprocess.check_call((
                sys.executable, 'color-code.py',
                path, os.path.join(args.output_dir, name + '.htm'),
            ))
            subprocess.check_call((
                sys.executable, 'color-code.py', '--widths',
                path, os.path.join(args.output_dir, name + '_widths.htm'),
            ))

    for filename in ON_DISK:
        subprocess.check_call((
            sys.executable, 'color-code.py',
            filename,
            os.path.join(args.output_dir, filename.replace('/', '_') + '.htm'),
        ))
        subprocess.check_call((
            sys.executable, 'color-code.py', '--widths',
            filename,
            os.path.join(
                args.output_dir, filename.replace('/', '_') + '_widths.htm',
            ),
        ))

    random.seed(0)
    some_bytes = b''.join(chr(random.getrandbits(8)) for _ in range(1200))
    proc = subprocess.Popen(
        (
            sys.executable, 'color-code.py',
            '/dev/stdin', os.path.join(args.output_dir, 'random.htm'),
        ),
        stdin=subprocess.PIPE,
    )
    proc.communicate(some_bytes)
    proc = subprocess.Popen(
        (
            sys.executable, 'color-code.py', '--widths',
            '/dev/stdin', os.path.join(args.output_dir, 'random_widths.htm'),
        ),
        stdin=subprocess.PIPE,
    )
    proc.communicate(some_bytes)


if __name__ == '__main__':
    exit(main())
