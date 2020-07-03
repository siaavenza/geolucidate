import re


"""List of Minutes/Seconds Characters for normalization

Was generated with unicodedata.name and unicodedata.char
and searched for names that include "QUOTATION" and "PRIME"
"""
MINUTE_CHARACTERS = {
    # Quotations
    "LEFT SINGLE QUOTATION MARK": "‘",
    "RIGHT SINGLE QUOTATION MARK": "’",
    "HEAVY SINGLE TURNED COMMA QUOTATION MARK ORNAMENT": "❛",
    "HEAVY SINGLE COMMA QUOTATION MARK ORNAMENT": "❜",
    "SINGLE HIGH-REVERSED-9 QUOTATION MARK": "‛",
    # Primes
    "PRIME": "′",
    "MODIFIER LETTER PRIME": "ʹ",
    "REVERSED PRIME": "‵",
}
SECOND_CHARACTERS = {
    # Quotations
    "LEFT DOUBLE QUOTATION MARK": "“",
    "RIGHT DOUBLE QUOTATION MARK": "”",
    "REVERSED DOUBLE PRIME QUOTATION MARK": "〝",
    "DOUBLE HIGH-REVERSED-9 QUOTATION MARK": "‟",
    "HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT": "❝",
    "HEAVY DOUBLE COMMA QUOTATION MARK ORNAMENT": "❞",
    "DOUBLE PRIME QUOTATION MARK": "〞",
    "FULLWIDTH QUOTATION MARK": "＂",
    # Primes
    "MODIFIER LETTER DOUBLE PRIME": "ʺ",
    "DOUBLE PRIME": "″",
    "REVERSED DOUBLE PRIME": "‶",
}

# Use above dicts to generate RegEx character group string
# Example Output: MINUTE_CHARACTERS_RE >> "[‘’❛❜‛′ʹ‵]"
MINUTE_CHARACTERS_RE = '[{}]'.format(re.escape(''.join(MINUTE_CHARACTERS.values())))
SECOND_CHARACTERS_RE = '[{}]'.format(re.escape(''.join(SECOND_CHARACTERS.values())))
