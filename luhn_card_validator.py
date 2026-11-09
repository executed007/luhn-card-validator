_STRIP = str.maketrans("", "", " -")
_DOUBLE = str.maketrans("0123456789", "0246813579")  # digit -> doubled, minus 9 if > 9

# (issuer, valid lengths, prefix ranges)
_RULES = (
    ("Visa", (13, 16, 19), (("4", "4"),)),
    ("Mastercard", (16,), (("51", "55"), ("2221", "2720"))),
    ("American Express", (15,), (("34", "34"), ("37", "37"))),
    ("Discover", range(16, 20), (("6011", "6011"), ("644", "649"), ("65", "65"), ("622126", "622925"))),
    ("Diners Club", range(14, 20), (("300", "305"), ("36", "36"), ("38", "39"))),
    ("JCB", range(16, 20), (("3528", "3589"),)),
    ("UnionPay", range(16, 20), (("62", "62"),)),
)

# Expand every prefix range once: "51".."55" -> {"51": ..., "52": ..., ...}
_PREFIXES = {
    str(p): (name, lengths)
    for name, lengths, ranges in _RULES
    for lo, hi in ranges
    for p in range(int(lo), int(hi) + 1)
}
_SIZES = sorted({len(p) for p in _PREFIXES}, reverse=True)  # longest prefix first


def luhn_valid(n: str) -> bool:
    # Every second digit from the right is doubled (via the translate table).
    total = sum(map(int, n[::-2])) + sum(map(int, n[-2::-2].translate(_DOUBLE)))
    return total % 10 == 0


def issuer(n: str) -> str:
    for size in _SIZES:
        hit = _PREFIXES.get(n[:size])
        if hit and len(n) in hit[1]:
            return hit[0]
    return "Unknown"


def check_card(number: str) -> str | None:
    """Return the issuer name if the number passes the Luhn check, else None."""
    n = number.translate(_STRIP)
    if 12 <= len(n) <= 19 and n.isascii() and n.isdigit() and luhn_valid(n):
        return issuer(n)
    return None


if __name__ == "__main__":
    result = check_card(input("Enter a card number: "))
    print(f"Valid - {result}" if result else "Invalid")