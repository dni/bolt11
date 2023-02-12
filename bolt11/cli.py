""" lnurl CLI """
import sys
import click

from .decode import decode as bolt11_decode

# disable tracebacks on exceptions
# sys.tracebacklimit = 0


@click.group()
def command_group():
    """
    Python CLI for Bolt11
    decode and encode bolt11 invoices"""


@click.command()
@click.argument("url", type=str)
def encode(url):
    """
    encode a URL
    """
    click.echo(url)


@click.command()
@click.argument("bolt11", type=str)
def decode(bolt11):
    """
    decode a bolt11 invoice
    """
    click.echo(bolt11_decode(bolt11).json())


def main():
    """main function"""
    command_group.add_command(encode)
    command_group.add_command(decode)
    command_group()


if __name__ == "__main__":
    main()
