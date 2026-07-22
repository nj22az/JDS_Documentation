# Sony Vaio P — Hardware Reference & Linux Support Matrix

Part of project **JDS-PRJ-SFW-003 (Pocket Linux)** — see the project
[README](../README.md) for the design decisions built on top of this data.

Covers both generations: **VGN-P** (2009, Atom Z520/Z530/Z540) and
**VPCP11** (2010, Atom Z530/Z560). They share the same platform (Intel
Menlow: Atom Z5xx + US15W "Poulsbo" chipset), so one image serves both.

---

## Support Matrix

| Component | Hardware | Kernel driver | Status |
|-----------|----------|---------------|--------|
| CPU | Intel Atom Z520–Z560 (Silverthorne) | — | Works. **32-bit only** (no Intel 64). Has PAE + NX → use the `686-pae` kernel flavour. 2 threads (Hyper-Threading) |
| Chipset | Intel SCH US15W "Poulsbo" | `intel_sch`, `sdhci` | Works |
| Graphics | Intel GMA 500 (PowerVR SGX 535) | `gma500_gfx` (KMS) | **2D modesetting only.** No 3D, no video decode acceleration — the PowerVR core is undocumented and will never have an open driver |
| Display | 8.0" 1600×768 LVDS (~222 DPI) | via `gma500_gfx` | Works, native resolution. Needs font scaling (console `TER16x32`, X at 144 DPI) |
| RAM | 1–2 GB DDR2, soldered | — | Not upgradeable. zram is mandatory for comfort |
| Storage | 1.8" PATA ZIF: 4200 rpm HDD or SSD | `ata_piix` / `libata` | Works. HDD is the single worst bottleneck in the machine — a ZIF SSD (or CF/mSATA adapter) is the best money you can spend on it |
| Wi-Fi | Atheros AR9285 (802.11n) | `ath9k` | Works out of the box, **no firmware blob needed** |
| Bluetooth | Alps/generic USB BT 2.1 | `btusb` | Works |
| WWAN | Qualcomm Gobi 2000 (option) | `qcserial`/`qmi_wwan` | Needs proprietary firmware extracted from Windows drivers (`gobi-loader`). Out of scope for the base image |
| GPS | Via Gobi module (option) | — | Same firmware caveat as WWAN |
| Audio | Realtek ALC262 on Intel HDA | `snd_hda_intel` | Works (playback, mic, headphone jack) |
| Ethernet | — (none; USB or dongle only) | — | Use any USB 2.0 adapter (`asix`, `r8152` supported) |
| SD slot | Internal reader | `sdhci-pci` / USB storage | Works |
| Memory Stick slot | Sony MS reader | `memstick` | Works for MS; largely irrelevant today |
| Webcam | Sony Visual Communication Camera | `uvcvideo` | Works |
| Keyboard/pointer | Matrix keyboard + trackpoint stick | `atkbd`, `psmouse` | Works. Trackpoint speed tunable via `libinput` |
| USB | 2× USB 2.0 (EHCI) | `ehci-pci` | Works |
| Battery/ACPI | Sony notebook ACPI | `sony-laptop` | Battery status, brightness keys work via `sony-laptop` |

## Known Quirks

1. **Early console can blank or come up in a wrong mode** until `gma500_gfx`
   loads. Fix baked into the image: the module is listed in
   `/etc/initramfs-tools/modules` so KMS starts in early boot.
2. **Suspend/resume is fragile with gma500** — some units resume to a black
   screen. Test yours; if it misbehaves, prefer shutdown (boot is ~20–40 s).
   `s2idle` vs `deep` can be experimented with via `/sys/power/mem_sleep`.
3. **Never install the old proprietary "psb" (EMGD) driver** from 2009-era
   guides — it only worked with ancient kernels/X servers. The mainline
   `gma500_gfx` + Xorg `modesetting` path is the only maintained route.
4. **Speculative-execution mitigations** cost in-order Atoms real performance
   (syscall-heavy work) while the microarchitecture is immune to most of the
   attacks (no out-of-order speculation). The image boots with
   `mitigations=off`; remove it from the GRUB drop-in if the machine will face
   hostile local code.
5. **PATA HDD models:** the disk seeks are the pain, not the interface. The
   overlay lowers dirty ratios and mounts with relatime; an SSD swap transforms
   the machine.
6. **Do not enable a compositor** (picom etc.) — every window pixel is pushed
   by the CPU through the unaccelerated framebuffer; compositing doubles the
   work for zero benefit at this DPI.

## Boot Parameters Used by the Image

| Parameter | Purpose |
|-----------|---------|
| `mitigations=off` | Recover syscall/context-switch performance on in-order Atom (see quirk 4) |
| `fbcon=font:TER16x32` | Readable 32-px console font on the 222 DPI panel |
| `quiet` | Skip console spam; ~1 s faster boot on slow disk |

---

*This file is project support documentation; the controlled project record is
the README (JDS-PRJ-SFW-003) and CHANGELOG.*
