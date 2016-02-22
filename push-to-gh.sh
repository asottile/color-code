#!/usr/bin/env bash
set -e

[ "$TRAVIS_BRANCH" == "master" -a "$TRAVIS_PULL_REQUEST" == "false" ] || exit

git clone "https://${GH_TOKEN}@${GH_REF}" demo >& /dev/null

pushd demo
git checkout gh-pages
git config user.name "Travis-CI"
git config user.email "asottile@umich.edu"
git rm *
popd

./venv/bin/python demo.py demo
cp .travis.yml demo/

cd demo
git add .
git commit -m "Deployed ${TRAVIS_BUILD_NUMBER} to Github Pages"
git push -q origin HEAD >& /dev/null
