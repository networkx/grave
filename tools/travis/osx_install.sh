#!/usr/bin/env bash
set -ex

# set up Python and virtualenv on OSX
git clone https://github.com/matthew-brett/multibuild
source multibuild/osx_utils.sh
get_macpython_environment $TRAVIS_PYTHON_VERSION venv

set +ex
