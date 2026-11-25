# Research notes (running log)

Goal: design a charger that attaches to an Apple Watch while it's worn, so the watch keeps tracking sleep while it charges, the way the WHOOP battery pack does.

Each point is tagged:
- **[verified]**: a source says it directly (linked).
- **[inferred]**: my reasoning from verified facts.
- **[unverified]**: from a weak source or memory. Treat with caution.

---

## 1. How WHOOP does it

- **[verified] WHOOP 4.0 Battery Pack:** it charges the sensor **wirelessly**, and the pack itself charges over a waterproofed USB-C port. Quotes: "They've ditched the charging contact points on the side for wireless charging", "You simply slide the battery pack onto the Whoop 4.0, and it snaps in place", "means you never have to take your device off your wrist to charge", and "Whoop says 2 hours to transfer wirelessly from battery pod to Whoop 4.0, and my testing puts that virtually spot on." ([DC Rainmaker review, Nov 2021](https://dcrainmaker.com/2021/11/whoop-platform-review.html))
- **[unverified]** That the pack sits on the **top** face (away from the skin) is my understanding from product photos. The review text doesn't say which face. A search summary credited WHOOP with saying it went wireless to make the pack waterproof, but WHOOP's page blocks automated fetches, so I couldn't confirm it. ([WHOOP CTO article](https://whoop.com/thelocker/chief-technology-officer-whoop-4-0-accuracy), not read)
- **[verified] WHOOP 5.0 / MG "Wireless PowerPack":** you slide it onto the device while wearing it. It's IP68, takes about 110 min to charge the device on your wrist, holds its own charge for up to 30 days, and costs about $49. It is not compatible with WHOOP 4.0. ([the5krunner spec page](https://the5krunner.com/specs/whoop/5-0-mg/), [Best Buy listing](https://www.bestbuy.com/site/product/6621757.p))
- **[inferred] Why it works:** WHOOP put the power receiver on the face the pack slides over, which (per the photos, see above) is the side facing away from the skin, and the sensors on the bottom. Charging and sensing use opposite faces, so they never compete for space. This was a design decision made at the hardware level, which no accessory can add later.
- **[inferred]** WHOOP also has no screen and a 14+ day battery, so there's plenty of room under the top surface for a receiver coil. Apple Watch has a display there.

## 2. How Apple Watch charges

- **[verified]** The inductive charging coil and an alignment magnet sit in the **rear cover**, the side against your skin. On Series 4 and later, the optical heart-rate sensor is in the middle of the back, with a ring-shaped ECG electrode around it. The magnet and coil share the same rear assembly. ([iFixit Series 4 teardown](https://www.ifixit.com/teardown/apple-watch-series-4-teardown/113044), [iFixit original Watch teardown](https://www.ifixit.com/Teardown/Apple+Watch+Teardown/40655). A Series 2 teardown with the same finding came up in search, but I don't have its exact URL.)
- **[verified]** Series 7 and later have **no hidden diagnostic port**. Earlier models had one in the bottom band slot, and it was replaced by a 60.5 GHz wireless module used for servicing. ([MacRumors, Oct 2021](https://macrumors.com/2021/10/13/apple-watch-series-7-lacks-diagnostic-port))
- **[verified]** On older watches that still had the port, Apple disabled charging through it in software (watchOS 2.0.1 and later), which ended the Reserve Strap in 2016. ([MacRumors](https://www.macrumors.com/2016/04/18/reserve-strap-suspends-shipments/))
- **[unverified]** The charging protocol is proprietary and not Qi. The frequency is reported as about 320–327 kHz (Qi uses 105–205 kHz). The 326.5 kHz figure comes from a 2015 forum post, and the 320 kHz figure from an Alibaba buying guide. Neither is a primary source. ([AppleInsider forum](https://forums.appleinsider.com/discussion/185958/apple-watch-found-to-be-compliant-with-qi-wireless-charging-standard), [Qi standard (Wikipedia)](https://en.wikipedia.org/wiki/Qi_(standard)))

## 3. First conclusion on charging from the top

- **[inferred] A charger on top of the watch (over the screen) cannot charge an Apple Watch.** There's no power receiver on that side, and the battery, logic board and display all sit between the top face and the rear coil. A magnetic field from the top would have to pass through metal and lithium cells, which mostly turns into heat in those parts instead of charge. *Still to confirm: whether any model has a second coil or front-side receiver (I'm not aware of one).*
- **[inferred]** That leaves three possible routes:
  1. Charge through the **back** while worn: a thin transmitter between the watch and your wrist.
  2. Charge through a **port**: gone since Series 7.
  3. Charge through the **band slots**: no electrical contacts on any shipping model, as far as I know.

## 4. Sleep tracking while on a charger

- **[verified]** Wrist Detection controls background heart-rate recording. With it off, overnight heart-rate readings used for sleep stages stop. ([Tom's Guide](https://www.tomsguide.com/wellness/sleep-tech/6-apple-watch-settings-you-should-change-now-for-more-accurate-sleep-tracking))
- **[verified]** Apple's overnight Vitals require wearing the watch, and a loose fit hurts accuracy. ([Apple Support](https://support.apple.com/120142))
- **[unverified, anecdotal]** One Ultra 2 owner reported sleep stages logged while the watch sat on its charger all night, with no explanation. One Series 11 owner reported heart rate taking 15–30 min to resume after charging. ([Apple Community thread on sleep logged while charging](https://discussions.apple.com/thread/256109552), [Apple Community thread on Series 11 after charging](https://discussions.apple.com/thread/256223269))

## 5. Apple's own battery band patents

- **[verified, secondary coverage]** Apple has patented a battery band that would power the watch **through its existing inductive charging coil**. The coverage also describes sensors on the charging plate that check whether the watch is being worn, so power can be limited to avoid overheating your wrist. There's also a separate "modular functional band links" patent with battery modules. None of this has shipped. ([Macworld](https://www.macworld.com/article/229543/apple-has-just-patented-an-apple-watch-battery-band.html), [GSMArena](https://m.gsmarena.com/apple_patents_a_wearable_battery_charger_integrated_in_the_band-blog-23179.php), [Digital Trends](https://www.digitaltrends.com/wearables/apple-watch-modular-bands/))
- *To do: read the actual patent text and get patent numbers.* **Done, see §6.**

## 6. Apple patent US 10,020,668 B2: "Charging apparatus for wearable electronic device"

Source: [Google Patents](https://patents.google.com/patent/US10020668B2/en). This is the closest thing on record to what we want to build.

- **[verified]** Filed 2015-07-27 and granted 2018-07-10, assigned to Apple Inc. Google Patents lists it as **"Active, expires 2036-03-15"**, which Google itself labels an assumption rather than a legal conclusion.
- **[verified, quoted]** The external unit "couples (such as magnetically) to a surface of the wearable electronic device". It attaches to the band's "underside or inner surface", and magnets pull the coils into alignment to "maximize inductive power transfer efficiency".
- **[verified, quoted] It handles the sensor problem directly:** "the external power apparatus 703 defines apertures 716 to accommodate sensor windows 104", and the apertures "may align with the sensor windows 104 when the power transfer component 705 is coupled to the body". As an alternative, the "sensor windows may be configured in the power transfer component 705 instead", made from "optically translucent materials".
- **[verified, quoted] Heat:** charging "may increase the temperature" of the watch. It "may not be enough to damage components, but may result in discomfort for a user". Circuitry may cut power "only when the wearable electronic device 101 is worn", and "a thermal insulator may be positioned on the power transfer component" where it touches skin. No numeric limits are given in the part read.
- **[verified, quoted] Wear detection:** three methods are described: skin-contact plates that complete a circuit, the watch's own optical sensor reporting over Bluetooth, and conductive plates in the band clasp ("assume that the wearable electronic device 101 is worn when the band 102 is clasped"). Power changes "depending on whether or not" the watch is worn.
- **[unverified]** The claim summaries came from a model-extracted summary of the page, not the verbatim claim text. Read the PDF before relying on the exact claim scope.
- **[inferred] What it means for us:**
  1. Apple's own engineers judged the "thin charger under the watch with holes for the sensors" idea workable enough to patent. That's encouraging for feasibility.
  2. **If you ever sell it, this patent is a real legal risk.** Its claims cover a magnetically attached inductive coil plus wear sensing plus temperature-limiting control, attached to the band, which is the natural design. Talk to a patent attorney before selling anything. (This is not legal advice. I'm not qualified to judge infringement.)
  3. Apple has never shipped it. That hints the real-world problems (heat, sensor accuracy, fit, cost) were bad enough that Apple didn't think it was worth releasing.

## 7. Existing "charge on your wrist" products (crowdfunded)

- **[verified, secondary] EnergyLink / EnergyLink Gen 2 (Nexxtpercent, Kickstarter):** wireless charging "built into the band". You "fold the band to align the charger, let the magnets click into place, then plug into any USB-C port". It claims 4.8 W and 20→80% in about 38 min on a Series 10, and comes with a separate 5000 mAh power bank. **Nothing says it charges while worn or keeps the sensors working.** Folding the band to line up the charger suggests the watch is off your wrist while it charges. ([BackerCrew write-up, May 2026](https://backercrew.com/energylink-gen-2-titanium-2-in-1-apple-watch-charger-band/); the Kickstarter page returned 403 to my fetcher)
- **[verified, secondary] AUDX "Apple Watch charger, always on your wrist" (Kickstarter):** a puck built into a band accessory, about 12 g, up to 5 W, USB-C, and "Users still need access to a USB-C power source". It's a way to carry a charger, not a battery pack, and it says nothing about sensors or sleep. ([KickstartNew review](https://www.kickstartnew.com/apple-watch-charger-5w-charging-built-into-your-band-kickstarter-review/))
- **Smarger ("World's First Wearable Apple Watch Charger", Kickstarter):** the page returned 403, so I couldn't check it. About 50 backers.
- **[inferred]** None of these appears to solve the actual problem (charging while worn **with working sensors**). They make the charger easier to carry. The gap is real.

## 8. Does the watch measure heart rate while charging? (critical unknown)

- **[unverified, mixed anecdotes]** Some users report no heart-rate readings while on the charger. Others report readings, or sleep stages logged, while it charged off-wrist, which were probably junk. One forum user claims the watch "knows when it is connected to its charger and will not trigger the sensor", but that's a guess. ([Apple Community 8150719](https://discussions.apple.com/thread/8150719), [Apple Community 8202274](https://discussions.apple.com/thread/8202274))
- **[verified]** Low Power Mode turns off background heart-rate measurement. ([Apple Support](https://support.apple.com/en-us/108320))
- **[inferred] This is the biggest risk in the whole project.** If watchOS pauses wrist detection or background heart rate whenever it's charging, no hardware can fix that, because it's Apple's software. I found no Apple documentation either way. **It has to be tested with a prototype** (see the test plan in the design doc).

## 9. Battery sizes (for the energy budget)

- **[verified]** Series 4 (44 mm) holds 1.113 Wh / 291.8 mAh. ([iFixit](https://www.ifixit.com/teardown/apple-watch-series-4-teardown/113044))
- **[verified]** Series 10 (46 mm) holds 1.266 Wh / 327 mAh. ([MacRumors on iFixit teardown](https://www.macrumors.com/2024/10/07/ifixit-shares-apple-watch-series-10-teardown))
- **[verified, secondary]** Series 11 46 mm GPS is 1.403 Wh, Series 11 42 mm cellular is 1.245 Wh, and Ultra 3 49 mm is 2.313 Wh. ([Macwelt](https://www.macwelt.de/article/2907329/apple-watch-series-11-und-se-3-deutlich-grosere-batterien-als-bei-den-vorgangern.html))
- **[verified]** Ultra 1 is 542 mAh. ([MacRumors on iFixit](https://www.macrumors.com/2022/09/26/APPLE-WATCH-ULTRA-TEARDOWN-IFIXIT/))
- I found nothing for Series 12 or Ultra 4. Assume they're close to Series 11 and Ultra 3.

## 10. Charging protocol

- **[verified]** Third-party chargers that aren't MFi have repeatedly **stopped working after watchOS updates** (watchOS 6, 8.3, 10, and a watchOS 11 beta). Apple's position is to use only Apple or MFi "Made for Apple Watch" chargers. ([MacRumors, watchOS 8.3](https://www.macrumors.com/2021/12/22/apple-watch-charging-issues-watchos-8-3/), [Apple Support 118474](https://support.apple.com/118474), [MacRumors 2023 warning](https://www.macrumors.com/2023/12/15/non-certified-apple-watch-charger-warning/))
- **[inferred]** So there's a handshake or authentication layer that Apple can change at will. A DIY transmitter built on a clone chip could break after any update. The robust route is Apple's licensed MFi charging module, but that needs a registered company in the MFi program. Hobbyists can't get it.
- **[verified]** nok9, a test-equipment maker, published a reverse-engineered "Rainbow" spec of the Apple Watch charging interface in Nov 2016, covering Series 1 and 2 only. The press release gives no technical details, which are in paid documents. ([PRWeb](https://www.prweb.com/releases/wireless_charging_interface_of_the_apple_watch_reverse_engineered_new_rainbow_specification_available_for_nok9_customers/prweb13828874.htm))
- **[verified]** I found no public open-source implementation of the Apple Watch charging protocol. The best-known reverse-engineering work, WatchWitch, covers the watch's data protocols, not charging. ([arXiv 2507.07210](https://arxiv.org/pdf/2507.07210))

## 11. Coil and sensor layout (Series 4 teardown, exact wording)

- **[verified]** "the back sports an all-new optical sensor in the middle, surrounded by a new electrode." Then: "We spot a magnet in the middle for holding the Watch to the charger, the charging coil itself, and some new silicon". iFixit gives **no coil shape, position or dimensions.** ([iFixit Series 4](https://www.ifixit.com/teardown/apple-watch-series-4-teardown/113044))
- **[inferred]** Both the magnet and the optical sensor are "in the middle". A ring-shaped charger with a hole in the centre has no centre magnet to snap onto, so alignment would have to come from the band or a ring of magnets. Whether the receiving coil sits in a ring around the sensors or as a flat spiral under them decides how well a ring-shaped transmitter could couple. **Still unknown. An X-ray or teardown photo would settle it.**

## 12. Skin temperature limits

- **[verified, secondary]** IEC 62368-1 touch-temperature limits for devices worn on the body: about **43–48 °C for more than 8 h** of contact, depending on material, and 48 °C for 1 min to 8 h. Comfort targets are stricter, around 40 °C. IEC 63203-406-1 has an annex on **low-temperature burns from wearables** (skin damage from long contact at only moderately warm temperatures). ([Advanced Energy on IEC limits](https://www.advancedenergy.com/en-us/about/news/blog/design-considerations-for-maximum-temperature-per-iec-safety-standards/), [Electronics Cooling 2025](https://www.electronics-cooling.com/2025/07/thermal-design-for-externally-worn-wearable-electronics/), [IEC 63203-406-1 preview](https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec63203-406-1{ed1.0}b.pdf))
- **[inferred]** An overnight charger is exactly the "more than 8 hours of skin contact" case, which has the **strictest** limit. Low-temperature burns matter because the wearer is asleep and won't notice slow heating.
- **[verified]** IEC 62368-1 table, as reproduced by Electronics Cooling: devices worn on the body in direct contact for more than 8 h are limited to **43–48 °C**, and for 1 min to 8 h to **48 °C**. Comfort is "often on the order of 40 °C" for metals. The article gives **no heat-flux limit** and no rule for how many milliwatts raise skin temperature by how much. ([Electronics Cooling, Jul 2025](https://www.electronics-cooling.com/2025/07/thermal-design-for-externally-worn-wearable-electronics/))
- **[inferred, stable physiology]** At rest the body sheds roughly 80 W over about 1.8 m² of skin, about **4–5 mW/cm²**. A charger ring putting 12–47 mW/cm² into the skin (see §16) is **3–10× that**, so expect noticeable local warming. The actual temperature has to be measured, not guessed.

## 13. Apple's own accessory rules (primary source, current)

Source: Apple, *Accessory Design Guidelines for Apple Devices*, **Release R32 Update 1, dated 2026-10-30**, chapter 20 "Watch Bands". ([PDF](https://developer.apple.com/accessories/Accessory-Design-Guidelines.pdf))

- **[verified, quoted] "Watch bands shall not integrate magnetic chargers."** (§20.1)
- **[verified, quoted]** "Watch bands shall enable the user to maintain direct skin contact with Apple Watch heart sensors and the back of Apple Watch … Failure to do so may interfere with Apple Watch wrist detect and Apple Pay features." (§20.1)
- **[verified]** Apple's dimensional drawings for cases list "CASE DOES NOT OBSTRUCT THE WATCH CHARGING INTERFACE", "…OPTICAL SENSORS", "…EXTEND INTO WATCH SENSOR WINDOWS" and "…CONTACT ELECTRICAL SENSORS" as rules. ([Apple Watch Ultra dimensional drawing](https://developer.apple.com/download/files/accessories/dimensional-drawings/apple-watch-ultra.pdf). The drawing is marked proprietary, so I'm linking it rather than copying its dimensions. Download it yourself for exact geometry.)
- **[verified, from the drawing]** On the back, the **charging interface is a circle in the centre, and the four optical sensor windows sit inside it**. The electrical sensor (electrode) areas are on the back crystal around them.
- **[inferred] What this means:**
  - A charger band can **never be MFi-approved**, so you can't buy Apple's official charging module for it. Any version, DIY or commercial, would rely on a non-Apple charging chip, which watchOS updates have broken before (§10).
  - A ring under the watch would cover the electrode areas. Apple warns that blocking skin contact with the back "may interfere with … wrist detect". **Wrist detection must be tested**, because sleep tracking and background heart rate need it on (§4).
- **[unverified]** The Ultra drawing has a callout "DO NOT OBSTRUCT PORT IN BANDSLOT". An Apple Community thread mentions a small hole in an Ultra band slot. I found no evidence it's an electrical port (Series 4 had a pressure-equalisation vent in a band slot). Don't count on it. ([Apple Community 254313285](https://discussions.apple.com/thread/254313285), [iFixit Series 4](https://www.ifixit.com/teardown/apple-watch-series-4-teardown/113044))

## 14. Receiver coil geometry: a ring around the sensors (Apple patent)

Source: Apple patent US 10,381,881 B2, "Architecture of portable electronic devices with wireless charging receiver systems", priority 2017-09-06, granted 2019-08-13. It describes a smart watch. ([Google Patents](https://patents.google.com/patent/US10381881B2/en))

- **[verified, quoted]** "sensor module 1636 can be mounted on an inner surface of window 2204 and positioned within an inner diameter of receiver system 1618". "Sensor module 1636 can include a thin heart rate sensor 2502 and one or more photo diodes 2504". The alignment module and magnet are also "positioned within an inner diameter of receiver system 1618".
- **[verified]** The receiver coil is described as having "an inner diameter and an outer diameter" (a ring), with a ferromagnetic shield covering part of it.
- **[unverified, from a model summary of the page]** Secondary-coil frequency "between 300 to 400 kHz" (~326 kHz), which matches the 326.5 kHz forum figure in §2. Ferrite: Mn-Zn shield, permeability > 3000.
- **[inferred] This is the key physical enabler.** The watch's receiving coil is a **ring around the heart-rate sensor and magnet**. A **ring-shaped transmitter** lined up over that coil could couple to it **while leaving the centre open for the sensors**, which is exactly what Apple's other patent (§6) shows with its "apertures … to accommodate sensor windows". Caveat: a patent doesn't prove the shipping product is built this way, though it fits the iFixit and drawing evidence.

## 15. Why "from the top" or "around the side" doesn't work (measured physics)

Source: Zhu, Ban, Zhang, Yan, Xu, Mi, "Metal-rim-connected inductive coupler for smartwatch applications", *IET Power Electronics* 13(15):3428–3434, 2020, doi:10.1049/iet-pel.2020.0208. ([PDF](https://chrismi.sdsu.edu/publications/190.pdf))

- **[verified]** "the receiving coil (Rx coil) must be located at the very bottom of the smartwatch to ensure that no metallic components (… lithium-ion battery …) are embedded between the transmitting coil (Tx coil) and Rx coil."
- **[verified, Table 2]** A transmitter coil around a watch with an **unbroken metal rim** gave a coupling coefficient **k = 0.042**. Cutting a 1 mm slot in the rim and wiring it into the receiver raised it to **0.467**. That modification has to be built into the watch. Apple Watch rims aren't made that way, as far as I know.
- **[verified, Table 4]** With a metal layer (bottom metal cover or battery pack) in the field, a conventional coupler fell from **k = 0.417 to 0.008**.
- **[verified]** It also cites an earlier smartwatch-**strap** wireless charging system at **1.4 W output and 30 % DC-DC efficiency** (Jeong et al., IEEE Trans.). That's a real-world efficiency reference for coils in a band.
- **[inferred] Conclusion:** charging from the **top** (through the display, battery and logic board) or from **around the side** (through a closed metal case) is physically a non-starter, with coupling roughly 10–50× worse plus eddy-current heating of the case. **The power has to go in through the back.** The battery can sit on top or on the band like WHOOP's, but the coil has to sit under the watch.

## 16. Energy and heat budget (my calculation)

Script: [`calc/energy_budget.py`](../calc/energy_budget.py). Run `python3 calc/energy_budget.py`. Inputs are labelled. Assumptions: 8 h night, 20 % → 100 %, ~20 mW sleep draw (derived from Apple's "5 min ≈ 10 h of sleep tracking"), and 30–60 % end-to-end efficiency.

| Watch (battery) | Energy into watch overnight | Pack needed at 30 / 45 / 60 % efficiency | Heat near skin (half of losses) |
|---|---|---|---|
| Series 10 46 mm (1.27 Wh) | 1.17 Wh (avg ~147 mW) | ~1,060 / 700 / 530 mAh | ~170 / 90 / 50 mW |
| Series 11 46 mm (1.40 Wh) | 1.28 Wh (avg ~160 mW) | ~1,150 / 770 / 580 mAh | ~190 / 100 / 55 mW |
| Ultra 3 49 mm (2.31 Wh) | 2.01 Wh (avg ~251 mW) | ~1,810 / 1,210 / 910 mAh | ~290 / 150 / 85 mW |

- **[inferred]** A full overnight refill needs a pack of roughly **0.6–1.8 Ah**. For comparison, WHOOP 4.0's own battery is about 0.72 Wh (2.8 g × 258 Wh/kg, per TechInsights), so its pack can be tiny. **An Apple Watch pack would be several times bigger**, about the size of a small LiPo pouch, roughly 15–30 g. That's an estimate.
- **[inferred]** **"Maintenance mode"** (just cover the night's tracking, ~0.16 Wh, and keep the battery from dropping) needs only **~70–145 mAh**, which is small. It doesn't refill the watch, though. You'd still top it up during the day.
- **[inferred]** Spreading the charge over 8 h means low average power (~150–250 mW into the watch). That's **much gentler than Apple's puck**, which fast-charges at several watts. Heat is still the main safety question, because it's skin contact while you're asleep.
- **[verified]** Apple Watch "will regulate its internal temperature… charging times might increase, or charging might stop", and Ultra's ambient range while charging is 0–35 °C. ([Apple Support 108766](https://support.apple.com/108766)) **[inferred]** On a wrist, the back sits near skin temperature (low-to-mid 30s °C), so the watch may pause charging because of heat. Another reason to charge slowly.
- **[verified]** Series 8 and later and the Ultra have a temperature sensor **in the back crystal** that samples every 5 s during sleep to produce nightly wrist-temperature deviations. ([Apple Support 102674](https://support.apple.com/102674)) **[inferred]** A warm charging ring under the watch would **skew wrist-temperature data**, which also affects cycle-tracking estimates. You'd have to accept losing or corrupting that metric on charging nights.

## 17. Apple's puck and what's buildable

- **[verified]** Original Apple Watch charger: a cradle 28 mm across and 6.7 mm thick. It aligns with a single centring magnet (MagSafe for iPhone uses a ring of magnets instead). ([iFixit original Watch teardown](https://www.ifixit.com/Teardown/Apple+Watch+Teardown/40655), [MacRumors MagSafe teardown](https://www.macrumors.com/2020/10/23/magsafe-charger-teardown-reveals-magnets-and-coil/))
- **[verified]** Parts list for Apple's Series 7 fast-charge puck: "Wireless Charging Controller: STM32L433RC", "Dual MOSFET driver: TI TPS51604", and a custom "338S00810-A0" voltage regulator. The page doesn't describe the coil. ([ChargerLAB, Oct 2021](https://chargerlab.com/teardown-of-apple-watch-series-7-magnetic-fast-charger-to-usb-c-cable-1m))
  - **[inferred]** The controller is a general-purpose STMicro microcontroller, so the charging protocol lives in Apple's **firmware**, not in an off-the-shelf charger chip you could buy. That fits the "clone chips break after watchOS updates" pattern (§10).
- **[verified]** Fast charging on Series 7 needs a USB-C PD adapter of 5 W or more. ([MacRumors](https://www.macrumors.com/2021/10/14/apple-watch-series-7-fast-charge-adapter/))
- **[verified, absence]** I found **no Apple Watch–specific transmitter board** sold for DIY. Generic Qi transmitter boards are common, but Apple Watch charging isn't Qi (§2). ([example generic Qi board on Newegg](https://www.newegg.com/p/2S7-07JP-1M1B1))
  - **[inferred]** The practical prototype route is to **take apart a cheap third-party Apple Watch charger** and reuse its board with a new ring-shaped coil.
- **[verified, absence]** I found **no ring-shaped ("donut") Apple Watch charger**, product or prototype. Search hits were stands with a cable hole, plus a leaked Series 10 prototype with an unusual ring **sensor** (not a charger). ([Notebookcheck](https://www.notebookcheck.net/Leak-reveals-Apple-Watch-Series-10-prototype-with-ring-shaped-sensor.990653.0.html))
- **[unverified]** Gap tolerance: one retailer lists the Apple charging dock's maximum case thickness as 0 mm, and one MacRumors user found a case made charging "barely" work. No measured numbers exist, so Test 2 in DESIGN.md measures it. ([Coolblue](https://www.coolblue.nl/en/support/product/854347/apple-magnetic-charging-dock-for-apple-watch.html), [MacRumors forum](https://forums.macrumors.com/threads/recommendation-for-apple-watch-charging-stand-that-works-with-a-watch-case.2421964))
- **[verified]** Wrist detection relies on "the sensor on the back of the watch" making skin contact, and turning wrist detection off disables heart-rate and sleep tracking. ([Apple Support 111819](https://support.apple.com/en-us/111819))

## 18. Where research stops

The remaining unknowns can't be settled by searching. They need the cheap physical tests in [`DESIGN.md`](../DESIGN.md):
1. Does a thin ring under the watch keep wrist detection and heart rate working? (Test 1)
2. How much gap does the watch's receiver tolerate? (Test 2)
3. Does watchOS keep measuring heart rate while charging? (Test 4)
4. How hot does the ring get against skin? (Tests 3–4)
