#!/bin/bash

virtualenv --system-site-package .envs/venv
source .envs/venv/bin/activate
pip install requests

