# Design study: charging an Apple Watch while it tracks your sleep

*November 2026. The supporting evidence, with sources and verified/inferred/unverified tags, is in [`research/notes.md`](research/notes.md). Section numbers like (§14) point there.*

## Verdict first

1. **A charger that sits on top of the watch (over the screen) cannot work.** Apple Watch only takes in power through the coil on its back. From the top, the field would have to pass through the battery, logic board and metal case. In published smartwatch measurements, a metal layer in the path cut coupling from 0.417 to 0.008, and a coil around an unbroken metal rim got 0.042 (§15). No accessory can change that.
2. **The only route that might work is a thin ring-shaped charging coil *under* the watch, with a hole in the middle for the sensors**, powered by a battery that rides on top of the band like WHOOP's pack. The physics allows it: Apple's own patent puts the watch's receiving coil in a ring *around* the heart-rate sensor (§14). Apple itself patented this exact "battery band with holes for the sensor windows" idea (§6).
3. **Apple has never shipped it, and its accessory rules forbid it**: "Watch bands shall not integrate magnetic chargers" (§13). So there's no official charging chip for it, and unofficial chips have been broken by watchOS updates before (§10).
4. **Three unknowns could kill it, and only physical tests can answer them**:
   - Does the watch keep wrist detection on with a ring covering part of its back?
   - Does watchOS keep measuring heart rate while it's charging?
   - Can it stay cool enough against sleeping skin?

   The first and biggest can be tested for **about $0 in one night** (Test 1 below).

**Honest rating.**
- **As a product to sell: poor.** It's banned from MFi, likely covered by an active Apple patent (Google Patents lists it as expiring around 2036), exposed to watchOS updates breaking it, and carries burn and LiPo liability.
- **As a DIY project: plausible but unproven.** I can't give you an honest probability. The early tests below will tell you quickly and cheaply.
- **As a solution to "I want sleep data and a charged watch":** a 5-minute top-up before bed already gets you ~10 h of sleep tracking on current models, for free. This project only pays off if never taking the watch off matters to you specifically.

---

## Why WHOOP can do it and Apple Watch can't (yet)

| | WHOOP 4.0 / 5.0 | Apple Watch |
|---|---|---|
| Where power enters | Wirelessly from the pack that slides onto the module, on the face away from the skin (going by photos; not stated in text) (§1) | **Back** of the watch, the skin side (§2, §14) |
| Where the sensors are | Bottom (skin side) | Bottom, **inside the same ring** as the charging coil (§13, §14) |
| Conflict between charging and sensing? | None. They use opposite faces | Yes. Both need the back |
| Battery to refill | About 0.7 Wh (§16) | 1.27–2.31 Wh (Series 10 → Ultra 3) (§9) |
| Official wear-while-charging accessory | Yes. 4.0: ~2 h on-wrist. 5.0/MG: ~$49, IP68, ~110 min (§1) | **Banned** by Apple's band guidelines (§13) |

WHOOP solved this when it designed the device, by putting the power receiver where the pack slides on, away from the sensors. On Apple Watch, the only face that can take power in is the same face that has to touch your skin.

---

## Options considered

| # | Idea | Verdict | Why |
|---|---|---|---|
| A | Pad on top of the watch (over the display) | ❌ Dead | No receiver on that side, and metal parts block the field (§3, §15) |
| B | Coil wrapped around the case sides | ❌ Dead | A closed metal rim acts like a shorted loop. Measured k = 0.042 vs 0.46 with a factory-slotted rim (§15) |
| C | Wired charging through the hidden port | ❌ Dead | Disabled in software in 2016 and removed from Series 7 onward (§2) |
| D | Electrical contacts in the band slots | ❌ Dead | Apple has never put contacts there |
| E | Normal puck under the watch while worn | ❌ Dead | Covers the sensors, so no heart rate and probably wrist detection fails (§4, §13) |
| **F** | **Thin ring-shaped coil under the watch + battery pod on the band** | ⚠️ **Only candidate** | Matches the ring-shaped receiver coil (§14) and Apple's own patent (§6). Untested |

---

## Concept F: "sleep band"

```
          ┌─────────────── display (top) ───────────────┐
          │   battery · logic board · metal case        │  ← no power gets in from here
          │                                             │
          └───[ receive coil (ring) ]──( sensors )──────┘  ← back crystal, domed
   ══[ TX ring coil + ferrite, ~0.3–1 mm ]═══ HOLE ═══[ TX ring ]══
                                    skin   ↑ sensor dome touches skin through the hole
   battery pod ─── thin flex lead ─────────┘
   (on the band, outside of wrist: the "WHOOP-style" part)
```

You'd swap your normal band for this one at bedtime, which takes a few seconds with Apple's band slots. The band holds:

1. **A flat ring-shaped transmitter coil under the watch.** It sits over the watch's receiving ring, with a centre hole sized so the domed sensor area pokes through and touches skin. The dome in the hole also centres the ring, so there's no need for the usual centre magnet (which would block the sensors).
2. **A ferrite sheet on the skin side of the coil**, to push the field up into the watch instead of into your wrist, plus a thin insulating cover.
3. **A battery pod on the band**: LiPo cell, USB-C charging, the transmitter electronics, and a temperature cut-off.
4. **A thin flex lead** from the pod to the ring.

**Power target:** charge *slowly* across the night, about 150–250 mW into the watch on average, not Apple's multi-watt fast charge. That keeps heat down and refills a Series 10/11 from about 20 % → 100 % in 8 h.

**Battery size** (from [`calc/energy_budget.py`](calc/energy_budget.py), at 30–60 % end-to-end efficiency):

| Mode | Series 10/11 | Ultra 3 |
|---|---|---|
| Full refill overnight (20→100 %) | ~530–1,150 mAh | ~900–1,800 mAh |
| Just cover the night's tracking | ~70–145 mAh | ~70–145 mAh |

A full-refill pod would be noticeably bigger than WHOOP's pack, roughly a small 1S LiPo pouch.

### Non-negotiable safety features (for anything worn while asleep)

- A thermistor **on the ring, against the skin side**, with a hardware cut-off that kills power above about **40 °C**. IEC 62368-1 allows 43–48 °C for worn devices over 8 h, but comfort and low-temperature burns argue for staying below 40 °C (§12).
- A **protected** LiPo cell (with a built-in protection circuit) in a hard enclosure, never bare.
- Power that is capped in hardware, so a firmware bug can't push full current.
- Nothing worn overnight until awake tests pass (Test 4).

---

## Test plan: cheapest, most decisive first. Stop at the first hard fail.

| # | Test | Cost / time | Pass | If it fails |
|---|---|---|---|---|
| 0 | **Baseline.** 2–3 normal nights. Note in Health how much overnight heart-rate data you get, sleep stages, wrist temperature, and whether the watch ever locked. | Free | — | — |
| 1 | **Passive spacer ring.** Cut rings from thin plastic (e.g. 0.25 mm and 0.5 mm PET or polyimide; try 1 mm last). Outer edge matches the back of the watch, centre hole just clears the sensor dome (measure your own watch). Wear under the watch with a normal band, one night per thickness. | ~$0–5, 1–3 nights | Watch **never locks** overnight. Heart-rate samples and sleep stages look like baseline. | **Stop.** If wrist detection or heart rate fails with an unpowered 0.25 mm ring, a powered one won't do better. Apple's guideline warning about wrist detection (§13) is the most likely reason. |
| 2 | **Gap tolerance.** On a table, put non-metal shims (paper or plastic) of 0.25 / 0.5 / 1.0 mm between Apple's puck and the watch, taped in place. Note whether it charges and how many % it gains in 15 min. | Free, 1 h | Still charges at the thickness Test 1 passed | A ring needs the coil to sit closer, which rules out thicker covers |
| 3 | **Bench prototype.** Open a cheap third-party Apple Watch charger, measure its coil's inductance, wind or order a flat ring coil with similar inductance, and fit a ferrite ring behind it. Charge the watch **on the table** and log ring temperature. | ~$40–100 plus an LCR meter and thermocouple | It charges, and the ring stays below 40 °C at your target power | Try different turns or wire, or accept it's not workable for a hobbyist |
| 4 | **Awake on-wrist test.** Wear the bench prototype for 30–60 min while awake, with a thermocouple between ring and skin. | Same hardware | Wrist detection stays on, heart rate keeps logging *while charging*, no "charging on hold", skin below 40 °C | **This is the watchOS question (§8).** If heart rate stops while charging, no hardware can fix it |
| 5 | **Supervised overnight.** Add the hardware thermal cut-off and protected cell first. | — | Sleep stages, heart rate and charge all look normal | — |

Tests 1 and 2 cost almost nothing and answer the biggest unknown. **Do them before buying anything.**

### Rough prototype parts list (prices are unverified guesses)

- A third-party USB-C Apple Watch charger to sacrifice for its controller board. Nobody sells a standalone Apple Watch transmitter board (§10). ~$10.
- Litz wire for a hand-wound flat ring coil, or a small custom flex-PCB coil order. ~$5–40.
- Flexible ferrite sheet (the kind sold for wireless-charging or NFC shielding). ~$5–10.
- Protected 1S LiPo, 500–1,000 mAh, plus a USB-C charge board and 5 V boost (or a tiny power-bank module). ~$10–20.
- NTC thermistor plus a small microcontroller or thermal cut-off. ~$5.
- An LCR meter and a thermocouple thermometer if you don't own them. ~$40–80.
- An elastic band or 3D-printed carrier for the ring and pod.

---

## Risk register

| Risk | Likelihood | Impact | Notes |
|---|---|---|---|
| Ring under the watch breaks wrist detection | Unknown. Apple explicitly warns about it (§13) | Fatal | **Test 1** settles it |
| watchOS stops background heart rate while charging | Unknown. Anecdotes go both ways (§8) | Fatal | **Test 4** settles it |
| Skin heating or low-temperature burn while asleep | Real | Serious injury | Slow charging, ferrite, insulation, hardware cut-off (§12, §16) |
| LiPo damage or fire on the wrist | Low with a protected cell | Serious | Protected cell, enclosure, no charging the pack while worn |
| watchOS update breaks the clone charger chip | Has happened repeatedly (§10) | Project stops working | No official route exists (§13) |
| Charging noise worsens heart-rate accuracy | Unknown | Worse sleep data | Compare against the Test 0 baseline |
| Wrist-temperature data corrupted by charger heat | Likely | Loses one metric | The temperature sensor is in the back crystal (§16) |
| Watch pauses charging when warm | Plausible | Slow or no charge | Apple: "charging might stop" when warm (§16) |
| Patent if sold | Real | Legal | US 10,020,668, Google lists it as expiring ~2036 (§6). **Not legal advice. See a patent attorney before selling anything.** |
| Accidental damage to the watch | Low–medium | Costly | Apple covers defects, not damage caused by accessories |

---

## What I couldn't settle by research (and why)

- **Whether watchOS measures heart rate while charging.** Apple documents nothing on it, and forum reports conflict. Only Test 4 can answer it.
- **The exact size and shape of the receiving coil in current models** (Series 11/12, Ultra 3/4). The patent and drawings show a ring around the sensors, but no public teardown gives dimensions. You'd measure it with the bench prototype in Test 3.
- **The Apple Watch charging protocol.** It's proprietary and runs in firmware on an STM32 chip plus a custom Apple chip in Apple's puck. The only public reverse-engineering is a paid 2016 spec covering Series 1–2 (§10).
- **How hot a ring at 50–300 mW actually gets against skin.** No reliable rule of thumb exists. It has to be measured.

## What to do tonight instead

Put the watch on its charger for 5–10 minutes while you brush your teeth. Apple rates that at about 10 h of sleep tracking on current models. If you have an Ultra, it lasts long enough that you can charge it at any time of day.
