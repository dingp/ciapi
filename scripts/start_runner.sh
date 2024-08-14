#!/bin/bash

repo=$1
runner_dir=$SCRATCH/gh_runner

mkdir -p ${runner_dir}
gh_dir=$(mktemp -d -p ${runner_dir})
cd ${gh_dir}

gh release download --repo actions/runner -p "*linux-x64*"
tar xvf actions-runner-linux-x64*.tar.gz

runner_token=$(gh api --method POST -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" /repos/${repo}/actions/runners/registration-token |jq -r '.token')

./config.sh --unattended --url https://github.com/${repo} --token ${runner_token} --ephemeral
nohup ./run.sh &
