# luhn-card-validator
A small, dependency-free Python module that checks whether a card number
passes the **Luhn algorithm** (mod 10 checksum) and identifies the likely
issuer from its prefix and length.It does not confirm that a
card exists, is active, or belongs to anyone.

Supported issuers: Visa, Mastercard, American Express, Discover,
Diners Club, JCB and UnionPay.
