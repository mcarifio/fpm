# fpm: The Federated Package Manager

## Summary

fpm, the federated package manager, can install "applications" from multiple repositories and with multiple packaging formats: rpm, apt, npm, cargo, AppImage, flatpak and snap.

## Usage:

```
python -m pip install -U pip
python -m pip install -U setuptools wheel
python -m pip install -U pipx
python -m pipx install --python 3.10 --fetch-missing-python git+https://github.com/mcarifio/fpm
```
