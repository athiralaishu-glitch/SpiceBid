from decimal import Decimal

def calculate_suggested_bid(current_bid):
    min_increment = max(int(current_bid * Decimal("0.02")), 100)

    suggested_bid = current_bid + min_increment
    suggested_bid = round(suggested_bid / 100) * 100

    if suggested_bid <= current_bid:
        suggested_bid = current_bid + min_increment

    return suggested_bid