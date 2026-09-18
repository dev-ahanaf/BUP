"""Centralized time expression parser and hour converter.

Enforces official GridWise whole-hour semantics:
- 24 hours: integers 0 through 23
- Time windows are start-inclusive and end-exclusive:
  "1 PM to 3 PM" -> [13, 14]
  "noon until 2 PM" -> [12, 13]
  "10 AM until noon" -> [10, 11]
  "2 AM until 5 AM" -> [2, 3, 4]
  "6 PM until 9 PM" -> [18, 19, 20]
- Returns sorted, unique lists of integer hours in range [0, 23].
"""
import re
from typing import List, Optional, Tuple

WORD_TO_HOUR = {
    "midnight": 0,
    "noon": 12,
    "midday": 12,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}


def normalize_hour_to_24(val: int, period: Optional[str] = None, context_hint: Optional[str] = None) -> int:
    """Convert an hour integer and optional AM/PM period to a 24-hour integer (0..23)."""
    val = int(val)
    if period:
        period = period.upper()
        if period == "AM":
            return 0 if val == 12 else val
        elif period == "PM":
            return 12 if val == 12 else val + 12

    # If no period is specified:
    if val >= 24:
        val = val % 24
    elif val <= 12 and context_hint:
        hint = context_hint.upper()
        if "PM" in hint or "EVENING" in hint or "AFTERNOON" in hint or "NIGHT" in hint:
            if val < 12:
                val += 12
        elif "AM" in hint or "MORNING" in hint:
            if val == 12:
                val = 0
    return val


def parse_hour_token(token: str, default_period: Optional[str] = None) -> Optional[int]:
    """Parse a single hour token like '1 PM', '13:00', 'noon', '3', 'midnight'."""
    token = token.strip().lower()
    if not token:
        return None

    if token in WORD_TO_HOUR:
        h = WORD_TO_HOUR[token]
        if default_period and token not in ("noon", "midnight", "midday"):
            return normalize_hour_to_24(h, default_period)
        return h

    # Match 24-hour format: 14:00, 14.00, 14h
    m24 = re.match(r"^(\d{1,2})(?::00|\.00|h)?$", token)
    if m24:
        h = int(m24.group(1))
        if default_period:
            return normalize_hour_to_24(h, default_period)
        return h if 0 <= h <= 23 else None

    # Match 12-hour format: 2pm, 2:00pm, 2 am
    m12 = re.match(r"^(\d{1,2})(?::00|\.00)?\s*(am|pm)$", token)
    if m12:
        h = int(m12.group(1))
        period = m12.group(2)
        return normalize_hour_to_24(h, period)

    return None


def extract_hour_range_from_text(text: str) -> Optional[List[int]]:
    """Extract standard start-inclusive, end-exclusive hours from natural text.

    Examples:
      "1 PM to 3 PM" -> [13, 14]
      "between 11 AM and 2 PM" -> [11, 12, 13]
      "from noon until 2 PM" -> [12, 13]
      "13:00 - 15:00" -> [13, 14]
      "from one until three" -> [13, 14] (in PM maintenance context) or [1, 2]
    """
    cleaned = text.lower().replace("–", "-").replace("—", "-")

    # Pattern 1: Explicit 24-hour range: 13:00 to 15:00, 13:00-15:00, 13-15
    p1 = re.search(r"\b(\d{1,2})(?::00)?\s*(?:-|to|until|through)\s*(\d{1,2})(?::00)?\s*(am|pm)?\b", cleaned)
    if p1:
        start_raw, end_raw, period = p1.group(1), p1.group(2), p1.group(3)
        start_h = int(start_raw)
        end_h = int(end_raw)

        # Check if PM is mentioned later or earlier in sentence
        is_pm = bool(period and period.lower() == "pm") or ("evening" in cleaned or "afternoon" in cleaned or "pm" in cleaned)
        is_am = bool(period and period.lower() == "am") or ("morning" in cleaned or "am" in cleaned)

        # If numbers are like 13..15, they are already 24-hour
        if start_h >= 12 or end_h >= 12:
            pass
        elif is_pm and not is_am:
            if start_h < 12:
                start_h += 12
            if end_h <= 12 and end_h <= start_h:
                end_h += 12
            elif end_h < 12 and end_h > start_h:
                end_h += 12
        elif is_am:
            if start_h == 12:
                start_h = 0
            if end_h == 12:
                end_h = 0

        if 0 <= start_h < end_h <= 24:
            return list(range(start_h, min(end_h, 24)))

    # Pattern 2: "from X [am|pm] to/until/and Y [am|pm]" or "between X [am|pm] and Y [am|pm]"
    time_token_pattern = r"(?:noon|midnight|\d{1,2}(?::00)?\s*(?:am|pm)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
    p2 = re.search(
        rf"(?:from|between)?\s*({time_token_pattern})\s*(?:to|until|and|-)\s*({time_token_pattern})",
        cleaned
    )
    if p2:
        t1, t2 = p2.group(1).strip(), p2.group(2).strip()
        # Determine inherited period if only t2 has am/pm
        p2_period = None
        if "pm" in t2:
            p2_period = "pm"
        elif "am" in t2:
            p2_period = "am"
        elif "evening" in cleaned or "afternoon" in cleaned or "night" in cleaned:
            p2_period = "pm"
        elif "morning" in cleaned:
            p2_period = "am"

        h1 = parse_hour_token(t1, default_period=p2_period)
        h2 = parse_hour_token(t2, default_period=p2_period)

        if h1 is not None and h2 is not None:
            # Handle start/end order
            if h2 < h1 and h2 <= 12 and p2_period == "pm":
                h2 += 12
            if 0 <= h1 < h2 <= 24:
                return list(range(h1, min(h2, 24)))

    return None


def validate_and_normalize_hours(hours: List[int]) -> Tuple[bool, List[int]]:
    """Validate that hours is a list of integers within [0, 23], deduplicate and sort in ascending order.

    Returns:
        (is_valid, normalized_hours)
    """
    if not isinstance(hours, list) or len(hours) == 0:
        return False, []

    cleaned = []
    for h in hours:
        if not isinstance(h, int):
            try:
                h = int(h)
            except (ValueError, TypeError):
                return False, []
        if 0 <= h <= 23:
            cleaned.append(h)
        else:
            return False, []

    # Sort and remove duplicates
    sorted_unique = sorted(list(set(cleaned)))
    if not sorted_unique:
        return False, []

    return True, sorted_unique
