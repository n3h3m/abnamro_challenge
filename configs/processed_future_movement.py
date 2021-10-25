"""
This file contains the field specification for future movement trade entries that were exxecuted.
The field names ane the positions were derived from "System A File Specification.pdf" Page:5

If the spec changes in future adjust the start and end positions accordingly
Also spec change
"""

future_movement_config = [
    ("record_code", 1, 3),
    ("client_type", 4, 7),
    ("client_number", 8, 11),
    ("account_number", 12, 15),
    ("subaccount_number", 16, 19),
    ("opposite_party_code", 20, 25),
    ("product_group_code", 26, 27),
    ("exchange_code", 28, 31),
    ("symbol", 32, 37),
    ("expiration_date", 38, 45),
    ("currency_code", 46, 48),
    ("movement_code", 49, 50),
    ("buy_sell_code", 51, 51),
    ("quantity_long_sign", 52, 52),
    ("quantity_long", 53, 62),
    ("quantity_short_sign", 63, 63),
    ("quantity_short", 64, 73),
    ("exch_broker_fee_dec", 74, 85),
    ("ech_broker_fee_d_c", 86, 86),
    ("exch_broker_fee_cur_code", 87, 89),
    ("clearing_fee_dec", 90, 101),
    ("clearing_fee_d_c", 102, 102),
    ("clearing_fee_cur_code", 103, 105),
    ("commission", 106, 117),
    ("commission_d_c", 118, 118),
    ("commission_cur_code", 119, 121),
    ("transaction_date", 122, 129),
    ("future_reference", 130, 135),
    ("ticket_number", 136, 141),
    ("external_number", 142, 147),
    ("transaction_price_dec", 148, 162),
    ("trader_initials", 163, 168),
    ("opposite_trader_id", 169, 175),
    ("open_close_code", 176, 176),
]
