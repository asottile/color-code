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
    'venv/lib/python2.7/copy_reg.pyc',
    'venv/lib/python2.7/site-packages/_cheetah.so',
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


def run(filename, output_dir, output_name):
    print('Making ' + output_name)
    out_fname = output_name.replace('/', '_')
    subprocess.check_call((
        sys.executable, 'color-code.py', '--name', output_name,
        filename, os.path.join(output_dir, out_fname + '.htm'),
    ))
    subprocess.check_call((
        sys.executable, 'color-code.py', '--name', output_name, '--widths',
        filename, os.path.join(output_dir, out_fname + '_widths.htm'),
    ))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir')
    args = parser.parse_args()

    mkdirp(args.output_dir)

    with tempdir() as tmpdir:
        path = os.path.join(tmpdir, 'tmpfile')
        for name, url in DOWNLOAD:
            resp = urllib.urlopen(url)
            with open(path, 'wb') as f:
                f.write(resp.read())
            run(path, args.output_dir, name)

        random.seed(0)
        some_bytes = b''.join(chr(random.getrandbits(8)) for _ in range(2400))
        with open(path, 'wb') as f:
            f.write(some_bytes)
        run(path, args.output_dir, 'random')

    for filename in ON_DISK:
        run(filename, args.output_dir, filename)


if __name__ == '__main__':
    exit(main())
