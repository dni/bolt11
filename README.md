Bolt11 implementation for Python
================================

[![tests](https://github.com/dni/bolt11/actions/workflows/tests.yml/badge.svg)](https://github.com/dni/bolt11/actions/workflows/tests.yml)
[![tests](https://github.com/dni/bolt11/actions/workflows/mypy.yml/badge.svg)](https://github.com/dni/bolt11/actions/workflows/mypy.yml)


### resources
* [Bolt11 Spec](https://github.com/lightning/bolts/blob/master/11-payment-encoding.md )
* [bolt11.org](https://www.bolt11.org/)
* [lightningdecoder](https://lightningdecoder.com/)


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
