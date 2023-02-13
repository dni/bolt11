Bolt11 implementation for Python
================================

[![tests](https://github.com/dni/bolt11/actions/workflows/tests.yml/badge.svg)](https://github.com/dni/bolt11/actions/workflows/tests.yml)
[![tests](https://github.com/dni/bolt11/actions/workflows/mypy.yml/badge.svg)](https://github.com/dni/bolt11/actions/workflows/mypy.yml)


# Bolt11 En- and Decoder
inspired by https://github.com/rustyrussell/lightning-payencode


### installing
```console
git clone https://github.com/dni/bolt11
cd bolt11
poetry install
```

### running CLI
```console
poetry run bolt11 --help
poetry run bolt11 decode
poetry run bolt11 encode
```

### run all checks and tests
```console
make
```

### using pre-commit as git hook
```console
poetry run pre-commit install
```
