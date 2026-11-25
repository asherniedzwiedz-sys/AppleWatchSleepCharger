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
- *To do: read the actual patent text and get patent numbers.*
