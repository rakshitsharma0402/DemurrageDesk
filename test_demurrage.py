from demurrage import charge

TIERS = [{"from_day": 8, "to_day": 14, "rate": 40}, {"from_day": 15, "to_day": None, "rate": 80}]
# What the model actually extracted in testing: the first tier's end day was missing
TIERS_OPEN = [{"from_day": 8, "to_day": None, "rate": 40}, {"from_day": 15, "to_day": None, "rate": 80}]

for t in (TIERS, TIERS_OPEN):
    assert charge(5, 7, t)[0] == 0                   # inside free time
    assert charge(10, 7, t)[0] == 120                # days 8-10 at 40
    assert charge(16, 7, t)[0] == 7 * 40 + 2 * 80    # crosses into the second tier
assert charge(16, 7, list(reversed(TIERS_OPEN)))[0] == 440  # order shouldn't matter
print("demurrage tests passed")