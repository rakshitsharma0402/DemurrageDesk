"""Pure-Python charge calculator. The model never does this maths.

Tiers use absolute day numbers on the clock (day 1 = first day counted).
Days 1..free_days are free; each later day is charged at the rate of the tier it falls in.
A tier with no end day runs until the next tier starts, so [{8, None, 40}, {15, None, 80}]
means days 8-14 at 40 and day 15 onward at 80.
`days_held` must already follow the contract's counting rule (calendar vs working days).
"""


def _resolve(tiers: list[dict]) -> list[dict]:
    tiers = sorted(tiers, key=lambda t: t["from_day"])
    out = []
    for i, t in enumerate(tiers):
        end = t.get("to_day")
        if end is None and i + 1 < len(tiers):
            end = tiers[i + 1]["from_day"] - 1
        out.append({**t, "to_day": end})
    return out


def charge(days_held: int, free_days: int, tiers: list[dict]):
    tiers = _resolve(tiers)
    breakdown = {}
    for day in range(free_days + 1, days_held + 1):
        for i, t in enumerate(tiers):
            if t["from_day"] <= day and (t["to_day"] is None or day <= t["to_day"]):
                label = f"day {t['from_day']}" + (f"-{t['to_day']}" if t["to_day"] else "+")
                row = breakdown.setdefault(i, {"tier": label, "rate": t["rate"], "days": 0})
                row["days"] += 1
                break
    rows = [{**r, "subtotal": r["days"] * r["rate"]} for r in breakdown.values()]
    return sum(r["subtotal"] for r in rows), rows