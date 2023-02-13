""" Bolt11 test helpers """

# from decimal import Decimal

# import pytest

# from bolt11.helpers import shorten_amount, unshorten_amount


# class TestHelpers:
#     @pytest.mark.parametrize(
#         "amount",
#         [
#             (
#                 1,
#                 10,
#                 0.001,
#                 0.000_000_000_1,
#             ),
#         ],
#     )
#     def test_helper_amount(self, amount):
#         shortened = shorten_amount(Decimal(amount))
#         unshortened = unshorten_amount(shortened)
#         assert amount == unshortened
