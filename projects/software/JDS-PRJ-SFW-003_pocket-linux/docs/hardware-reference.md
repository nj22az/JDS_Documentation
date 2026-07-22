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
| Bluetooth | Alps/generic USB BT 2.1 | `btusb` + BlueZ userspace | Works — pairing via Menu > Bluetooth (blueman); audio routing via `pulseaudio-module-bluetooth` |
| WWAN | Qualcomm Gobi 2000 (option) | `qcserial`/`qmi_wwan` + ModemManager | Works after a one-time firmware install from the owner's Windows discs — run `pocket-gobi-firmware` (see below) |
| GPS | Via Gobi module (option) | via WWAN stack | Available once the Gobi firmware is installed (NMEA port) |
| Audio | Realtek ALC262 on Intel HDA | `snd_hda_intel` | Works (playback, mic, headphone jack) |
| Ethernet | — (none; USB or dongle only) | — | Use any USB 2.0 adapter (`asix`, `r8152` supported) |
| SD slot | Internal reader | `sdhci-pci` / USB storage | Works — FAT32/exFAT/NTFS userspace tools included for cards and Windows-formatted USB disks |
| Memory Stick slot | Sony MS reader | `memstick` | Works for MS; largely irrelevant today |
| Webcam | Sony Visual Communication Camera | `uvcvideo` | Works |
| Keyboard/pointer | Matrix keyboard + trackpoint stick | `atkbd`, `psmouse` | Works. Trackpoint speed tunable via `libinput` |
| USB | 2× USB 2.0 (EHCI) | `ehci-pci` | Works |
| Battery/ACPI | Sony notebook ACPI | `sony-laptop` | Battery status works; brightness Fn keys are mapped to `brightnessctl` in the IceWM keys file |

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

## Mobile Broadband: Firmware from Your Own Windows Discs

Windows driver *code* (`.sys`/`.dll`) cannot run on Linux and is never
needed — every device in the matrix above has a native Linux driver. The
single exception is a *data* dependency: the Gobi 2000 WWAN/GPS module boots
from three firmware files (`amss.mbn`, `apps.mbn`, `UQCN.mbn`) that Sony
ships only inside the Windows driver package. Extracting them from the discs
you own, for the machine they came with, is the standard route; they are
licensed per-machine and must never be redistributed (the repo ignores
`*.mbn` as a guard).

One-time setup, entirely on Linux:

1. The Vaio P has no optical drive — mount the disc via a USB DVD drive, or
   copy its contents to a USB stick on any other computer.
2. Run `sudo pocket-gobi-firmware /media/<disc-or-folder>`. It finds the
   three files anywhere under that path (case-insensitive), lets you pick
   the carrier variant of `UQCN.mbn` if there are several, and installs
   them to `/lib/firmware/gobi/`.
3. If the disc only holds installer `.exe`/`.cab` files, unpack first:
   `7z x WWAN_DRIVER.EXE -ounpacked`, then point the tool at `unpacked/`.
4. Reboot. `gobi-loader` uploads the firmware automatically; check with
   `mmcli -L`, then connect via the network tray icon → Mobile Broadband.

## Verifying Drivers on the Real Machine

Driver support cannot be proven from a build machine — it is proven on the
Vaio P itself. The image ships a self-test for exactly this:

```
pocket-check          # or: Menu > Hardware Self-Test
```

It prints one PASS/FAIL line per device (graphics, panel mode, backlight,
sound, keyboard, trackpoint, Fn keys, Wi-Fi, radio kill switch, Bluetooth,
webcam, battery, disk, zram, earlyoom) with a fix hint on every FAIL, and
exits non-zero if anything is broken. Run it once after first boot; if
everything passes, every driver in the support matrix above is confirmed
working on your unit.

## Boot Parameters Used by the Image

| Parameter | Purpose |
|-----------|---------|
| `mitigations=off` | Recover syscall/context-switch performance on in-order Atom (see quirk 4) |
| `fbcon=font:TER16x32` | Readable 32-px console font on the 222 DPI panel |
| `quiet` | Skip console spam; ~1 s faster boot on slow disk |

---

*This file is project support documentation; the controlled project record is
the README (JDS-PRJ-SFW-003) and CHANGELOG.*
