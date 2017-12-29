import argparse
import json
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
    'venv/lib/python3.6/copy_reg.pyc',
)


def run(filename, output_dir, output_name):
    print('Making ' + output_name)
    out_fname = output_name.replace('/', '_').lstrip('_')
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

    os.makedirs(args.output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
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

    names = [name for name, _ in DOWNLOAD] + list(ON_DISK) + ['random']
    names_fnames = [
        (name.rpartition('/')[2], name.replace('/', '_').lstrip('_'))
        for name in names
    ]
    with open(os.path.join(args.output_dir, 'index.htm'), 'wb') as f:
        subprocess.check_call(
            (sys.executable, 'index.py'),
            stdout=f,
            env={'NAMES_FNAMES': json.dumps(names_fnames)},
        )

    shutil.copy('index.css', args.output_dir)


if __name__ == '__main__':
    exit(main())
