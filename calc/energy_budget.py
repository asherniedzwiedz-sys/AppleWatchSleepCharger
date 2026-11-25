"""Rough overnight energy and heat budget for a wear-while-charging Apple Watch pack.

Every input is labelled with where it came from. Change them and re-run:
    python3 calc/energy_budget.py
"""

# --- Watch battery capacities (Wh) -------------------------------------------
# Series 11 46mm GPS and Ultra 3 49mm: Macwelt table (secondary source).
# Series 10 46mm: iFixit teardown via MacRumors.
WATCHES = {
    "Series 10 46mm": 1.266,
    "Series 11 46mm": 1.403,
    "Ultra 3 49mm": 2.313,
}

# --- Assumptions (ESTIMATES, not measured) ----------------------------------
NIGHT_HOURS = 8.0
START_SOC = 0.20          # battery level when you go to bed
END_SOC = 1.00            # battery level you want in the morning
SLEEP_DRAW_W = 0.020      # watch draw while sleep-tracking. Estimate:
                          # Apple says ~5 min of fast charge ~= 10 h of sleep
                          # tracking; 5 min at ~80%/30 min is ~13% of ~1.4 Wh
                          # = ~0.19 Wh / 10 h = ~19 mW. Treat as rough.
EFFICIENCIES = [0.30, 0.45, 0.60]   # pack-battery -> watch-battery, end to end.
                          # 30% = measured for a smartwatch *strap* charging
                          # system (Jeong et al., cited in IET Power Electron.
                          # 2020 13(15):3428). Higher values are optimistic.
PACK_V = 3.7              # nominal LiPo cell voltage
SHARE_OF_LOSS_AT_SKIN = 0.5  # guess: fraction of losses dissipated in the coil
                             # ring + watch (against skin) vs. in the pack.
RING_AREA_CM2 = 4.0       # guess: skin-contact area of a ~1 cm wide ring.

def main():
    for name, wh in WATCHES.items():
        refill = (END_SOC - START_SOC) * wh
        sleep_use = SLEEP_DRAW_W * NIGHT_HOURS
        into_watch = refill + sleep_use
        avg_into_watch_w = into_watch / NIGHT_HOURS
        print(f"\n{name}: battery {wh:.3f} Wh")
        print(f"  energy into watch overnight: {into_watch:.2f} Wh "
              f"(refill {refill:.2f} + sleep use {sleep_use:.2f}); "
              f"avg {avg_into_watch_w*1000:.0f} mW over {NIGHT_HOURS:.0f} h")
        for eff in EFFICIENCIES:
            pack_wh = into_watch / eff
            pack_mah = pack_wh / PACK_V * 1000
            loss_w = (pack_wh - into_watch) / NIGHT_HOURS
            skin_w = loss_w * SHARE_OF_LOSS_AT_SKIN
            flux = skin_w / RING_AREA_CM2 * 1000
            print(f"  eff {eff:.0%}: pack >= {pack_wh:.2f} Wh (~{pack_mah:.0f} mAh @3.7V), "
                  f"avg loss {loss_w*1000:.0f} mW, ~{skin_w*1000:.0f} mW near skin "
                  f"(~{flux:.0f} mW/cm2 over {RING_AREA_CM2:.0f} cm2)")

    # Maintenance-only mode: just cover the night's sleep tracking.
    print("\nMaintenance mode (only offset the night's sleep tracking, no refill):")
    sleep_use = SLEEP_DRAW_W * NIGHT_HOURS
    for eff in EFFICIENCIES:
        pack_wh = sleep_use / eff
        print(f"  eff {eff:.0%}: pack >= {pack_wh:.2f} Wh (~{pack_wh/PACK_V*1000:.0f} mAh)")

if __name__ == "__main__":
    main()
