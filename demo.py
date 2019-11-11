import copyreg
import json
import os.path
import random
import subprocess
import sys
import tempfile
import urllib.request


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
        'https://raw.githubusercontent.com/pre-commit/pre-commit.github.io/'
        '8135597/favicon.ico',
    ),
)

ON_DISK = ('/bin/echo', '/bin/cat', os.path.relpath(copyreg.__cached__))


def to_filename(name: str) -> str:
    return name.replace('/', '_').lstrip('_')


def run(filename: str, output_name: str) -> None:
    print(f'Making {output_name}')
    out_fname = to_filename(output_name)
    subprocess.check_call((
        sys.executable, 'color-code.py', '--name', output_name,
        filename, f'out/{out_fname}.html',
    ))
    subprocess.check_call((
        sys.executable, 'color-code.py', '--name', output_name, '--widths',
        filename, f'out/{out_fname}_widths.html',
    ))


def main() -> int:
    os.makedirs('out', exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'tmpfile')
        for name, url in DOWNLOAD:
            resp = urllib.request.urlopen(url)
            with open(path, 'wb') as f:
                f.write(resp.read())
            run(path, name)

        random.seed(0)
        some_bytes = bytes(random.getrandbits(8) for _ in range(2400))
        with open(path, 'wb') as f:
            f.write(some_bytes)
        run(path, 'random')

    for filename in ON_DISK:
        run(filename, filename)

    names = [name for name, _ in DOWNLOAD] + list(ON_DISK) + ['random']
    names_fnames = [
        (name.rpartition('/')[2], to_filename(name)) for name in names
    ]
    with open('index.html', 'wb') as f:
        subprocess.check_call(
            (sys.executable, 'index.py'),
            stdout=f,
            env={'NAMES_FNAMES': json.dumps(names_fnames)},
        )

    return 0


if __name__ == '__main__':
    exit(main())
