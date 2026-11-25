# Research notes (running log)

Goal: design a charger that attaches to an Apple Watch while it's worn, so the watch keeps tracking sleep while it charges, the way the WHOOP battery pack does.

Each point is tagged:
- **[verified]**: a source says it directly (linked).
- **[inferred]**: my reasoning from verified facts.
- **[unverified]**: from a weak source or memory. Treat with caution.

---

## 1. How WHOOP does it

- **[verified] WHOOP 4.0 Battery Pack:** it slides onto the top of the sensor module and charges it **wirelessly**. WHOOP says it dropped the older side contacts because those were the hardest part of waterproofing the pack. The pack itself charges over USB-C. ([DC Rainmaker review](https://dcrainmaker.com/2021/11/whoop-platform-review.html), [WHOOP CTO article](https://whoop.com/thelocker/chief-technology-officer-whoop-4-0-accuracy))
- **[verified] WHOOP 5.0 / MG "Wireless PowerPack":** you slide it onto the device while wearing it. It's IP68, takes about 110 min to charge the device on your wrist, holds its own charge for up to 30 days, and costs about $49. It is not compatible with WHOOP 4.0. ([the5krunner spec page](https://the5krunner.com/specs/whoop/5-0-mg/), [Best Buy listing](https://www.bestbuy.com/site/product/6621757.p))
- **[inferred] Why it works:** WHOOP put the power receiver on the top of the device, the side facing away from the skin, and the sensors on the bottom. Charging and sensing use opposite faces, so they never compete for space. This was a design decision made at the hardware level, which no accessory can add later.
- **[inferred]** WHOOP also has no screen and a 14+ day battery, so there's plenty of room under the top surface for a receiver coil. Apple Watch has a display there.

## 2. How Apple Watch charges

- **[verified]** The inductive charging coil and an alignment magnet sit in the **rear cover**, the side against your skin. On Series 4 and later, the optical heart-rate sensor is in the middle of the back, with a ring-shaped ECG electrode around it. The magnet and coil share the same rear assembly. ([iFixit Series 4 teardown](https://www.ifixit.com/teardown/apple-watch-series-4-teardown/113044), [iFixit Series 2 teardown](https://www.ifixit.com/Teardown/Apple+Watch+Teardown/40655), [iFixit original Watch teardown](https://www.ifixit.com/Teardown/Apple+Watch+Teardown/40655))
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
