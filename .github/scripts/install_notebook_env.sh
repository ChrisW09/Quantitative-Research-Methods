#!/usr/bin/env bash
# Install everything needed to execute Lab_Notebooks/, for CI or for a local
# check. One script rather than four workflow steps, so the pinned and floating
# jobs cannot drift apart.
#
#   .github/scripts/install_notebook_env.sh            current ecosystem
#   .github/scripts/install_notebook_env.sh --pinned    plus constraints.txt
# No -u: under it, bash 3.2 (which is what /bin/bash still is on macOS) treats
# the expansion of an *empty* array as an unbound variable, and CONSTRAINTS is
# empty on the unpinned path. Nothing else here reads an unset variable.
set -eo pipefail

cd "$(dirname "$0")/../.."

CONSTRAINTS=()
if [ "${1:-}" = "--pinned" ]; then
  if [ -f constraints.txt ]; then
    CONSTRAINTS=(-c constraints.txt)
  else
    # Not fatal: constraints.txt is a record of a verified build, and the check
    # is still worth running without it — but say so loudly, because a "pinned"
    # run that silently floated would make a drift report meaningless.
    echo "::warning::--pinned was asked for but constraints.txt is missing; installing unpinned"
  fi
fi

# torch first, from the CPU index. requirements.txt asks for torch>=2.1 and
# constraints.txt pins an exact version, both of which the +cpu build satisfies,
# so installing it here stops the line below pulling the default CUDA wheels:
# roughly 2.5 GB of nvidia-* packages onto a runner with no GPU.
pip install --index-url https://download.pytorch.org/whl/cpu "${CONSTRAINTS[@]}" torch

pip install -r requirements.txt "${CONSTRAINTS[@]}"

# nbclient drives the kernel; ipykernel is what the notebooks run in, and it
# provides the inline matplotlib backend the stored outputs were made with.
# Deliberately unconstrained: the notebook front end does not affect results.
pip install nbclient nbformat ipykernel
