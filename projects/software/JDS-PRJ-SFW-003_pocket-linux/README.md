# Pocket Linux — Custom Linux Distro for the Sony Vaio P

| Field | Value |
|-------|-------|
| **Document No.** | JDS-PRJ-SFW-003 |
| **Revision** | D |
| **Date** | 2026-07-22 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

A custom, reproducible Linux distribution ("Pocket Linux") for the **Sony Vaio P**
8-inch pocket laptop. The Vaio P is severely underpowered by modern standards and
unusable with any stock desktop distro. Pocket Linux is built specifically around
its four hard constraints instead of fighting them:

| Constraint | Consequence for the OS |
|------------|------------------------|
| Intel Atom Z5xx is **32-bit only**, in-order, 1.33–2.13 GHz | Must be an i686 distro — modern x86-64 distros will not even boot |
| **GMA 500 (PowerVR)** graphics, no open 3D driver | 2D-only desktop, no compositing, no GL, no video decode help |
| **2 GB RAM**, soldered | Compressed swap in RAM (zram), no heavy desktop environment |
| 1.8" **PATA disk** (4200 rpm) + 1600×768 @ 222 DPI screen | Minimise disk writes; scale console and X fonts up ~1.5× |

The distro is not a hand-configured one-off: it is a **Debian live-build
configuration**. Running one script produces a bootable/installable hybrid ISO,
so the image can be rebuilt from scratch at any time and every tuning decision
lives in version control.

> **Doc says:** the machine isn't slow because Linux is heavy — it's slow because
> stock distros assume hardware the Vaio P doesn't have. Remove those assumptions
> and 2 GB with a 1.6 GHz Atom is genuinely usable for writing, SSH, music, and
> light browsing.

## Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Base | **Debian 12 "bookworm" i386** | Last Debian with an i386 kernel/installer; LTS until mid-2028; live-build gives a real installable distro, not a script pile |
| Kernel | `linux-image-686-pae` | Z5xx Atoms have PAE + NX; PAE flavour enables the NX bit |
| Graphics | Kernel `gma500_gfx` KMS + Xorg `modesetting` (2D, no GL) | The only working open driver for GMA 500; compositing and GL are avoided entirely |
| Desktop | **IceWM** + PCManFM, no display manager (`startx`) | Full desktop in ~120 MB RAM; a DM would burn RAM to show one login box |
| Memory | **zram** (zstd, 50 % RAM) + `earlyoom` + tuned sysctls | Compressed swap in RAM beats swapping to a 4200 rpm PATA disk by an order of magnitude |
| CPU | `mitigations=off` boot flag | In-order Bonnell Atoms lose disproportionate performance to speculative-execution mitigations they mostly don't need |
| HiDPI | Console `TER16x32` font, `Xft.dpi: 144` (1.5×) | 1600×768 on 8" is 222 DPI — unreadable at 1×, too cramped at 2× |
| Browsers | **NetSurf** (daily) + Firefox ESR (fallback) | Honest split: NetSurf is instant on light pages; Firefox ESR works everywhere but is the heaviest thing on the machine |
| Audio | ALSA + PulseAudio | Realtek ALC262 over Intel HDA — fully supported |
| Look & feel | Greybird theme + elementary-xfce icons + DMZ-White 32 px cursor (all DFSG-free, from Debian main) | Light, high-contrast, cheap to draw; no downloads from asset sites, so licensing is clean by construction |

## Usability Layer

Everything is reachable two ways — a labelled menu entry **and** a shortcut —
and every default is chosen so the obvious action is the right one:

| Feature | How it works |
|---------|--------------|
| Start menu | Plain-English entries, one per task ("Web Browser", "Files", "Wi-Fi and Network", "Help"); auto-generated "All Programs" catches later installs |
| Taskbar | Three quick-launch buttons (browser, files, terminal) + network and volume tray icons started automatically |
| Shortcuts | `Super+Enter` terminal, `Super+E` files, `Super+W` browser, `Super+H` help; Fn volume keys mapped |
| Built-in help | `pocket-help` (or Menu > Help) opens a one-page guide: Wi-Fi, apps, shortcuts, online video via mpv, font-size adjustment, update command |
| Sane defaults | Links open in NetSurf, media in mpv, images in GPicView, text in Mousepad — set via `mimeapps.list`, no "choose an application" dialogs |
| Trackpoint scrolling | Hold the middle button + move the stick to scroll (ThinkPad-style), configured in Xorg |
| Hardware self-test | `pocket-check` (or Menu > Hardware Self-Test): one PASS/FAIL line per device with a fix hint — proves every driver on the actual unit |
| Full driver coverage | Bluetooth userspace (BlueZ + blueman + PA module), brightness Fn keys (`brightnessctl`), FAT32/exFAT/NTFS media, Intel microcode, `lspci`/`lsusb`/`rfkill` diagnostics |
| Wallpaper | Original 5 KB navy-gradient PNG (CC0, generated in-project), drawn once by icewmbg — zero runtime cost |
| HiDPI pointer | 32 px DMZ-White cursor — a stock 24 px pointer is a speck at 222 DPI |

## Project Structure

| Path | Purpose |
|------|---------|
| `build/build.sh` | One-command ISO builder (wraps Debian live-build; all settings as constants at the top) |
| `build/config/package-lists/pocket.list.chroot` | The complete package manifest of the distro |
| `build/config/includes.chroot/` | File overlay baked into the image — Xorg, sysctl, zram, GRUB, skel dotfiles. **Single source of truth for all tuning** |
| `install/tune-vaio-p.sh` | Applies the same overlay + packages to an *existing* Debian 12 i386 install (no ISO rebuild needed) |
| `docs/hardware-reference.md` | Per-component hardware support matrix, kernel modules, and known quirks |
| `CHANGELOG.md` | Master change log for this project |

## Quick Start

### Path A — Build the ISO (on any Debian/Ubuntu machine, root)

```
sudo apt install live-build
cd build && sudo ./build.sh          # produces pocket-linux-*.iso (~1 GB)
```

Write it to USB with `dd`, boot the Vaio P from USB (F11), try the live session,
then run the installer from the boot menu. The Vaio P is BIOS-only; the ISO is
BIOS-bootable hybrid, no UEFI needed.

### Path B — Tune an existing Debian 12 i386 install

Already have minimal Debian 12 (i386, no desktop task) on the machine?

```
sudo ./install/tune-vaio-p.sh
```

This installs the same package set and copies the same overlay files, then
updates GRUB and the initramfs. Log in and run `startx`.

## What to Expect (Performance Budget)

| Workload | Verdict |
|----------|---------|
| Boot to desktop | ~40 s from PATA HDD, ~20 s from SSD |
| Idle RAM (desktop up) | ~150 MB — leaves ~1.8 GB for applications |
| Writing, terminal, SSH, file management, music (cmus) | Excellent — this is the machine's sweet spot |
| Light browsing (NetSurf), email | Good |
| Full web (Firefox ESR) | Workable with 1–3 tabs; heavy sites will crawl |
| Video playback | SD/480p via mpv software decode only; 720p+ is beyond the hardware |
| YouTube in browser | Not realistic — download with `yt-dlp` and play in mpv instead |

## Known Limitations

- **GMA 500 has no 3D acceleration and never will** — the PowerVR core is
  undocumented; anything needing OpenGL is off the table.
- **Suspend/resume** with gma500 is historically fragile — test on your unit;
  the safe habit is shutdown/boot (boot is fast).
- **WWAN (Gobi 2000)** needs a one-time firmware install from your own Windows
  driver discs — run `sudo pocket-gobi-firmware /media/<disc>`; the full ModemManager
  stack is in the image (see hardware reference). The firmware is licensed
  per-machine: never redistribute it or commit it to this repo (`*.mbn` is gitignored).
- **End-of-life horizon:** Debian 12 i386 LTS runs to ≈ June 2028. After that the
  successor plan is an antiX/Void i686 rebase — tracked in the CHANGELOG.

## References

- Hardware detail & quirks: [`docs/hardware-reference.md`](docs/hardware-reference.md)
- Debian live-build manual: <https://live-team.pages.debian.net/live-manual/>
- Kernel gma500 driver: `drivers/gpu/drm/gma500/` (mainline since 3.3)

---

## Revision History

| Rev | Date | Description | Author |
|-----|------|-------------|--------|
| A | 2026-07-22 | Initial release: live-build config, tuning overlay, install script, hardware reference | N. Johansson |
| B | 2026-07-22 | Usability layer: free theme/icon/cursor assets, wallpaper, start menu, shortcuts, tray applets, app defaults, trackpoint scrolling, built-in help | N. Johansson |
| C | 2026-07-22 | Driver completeness: Bluetooth userspace stack, brightness keys, removable-media filesystems, microcode, diagnostics tools, `pocket-check` hardware self-test | N. Johansson |
| D | 2026-07-22 | WWAN support: ModemManager stack + `pocket-gobi-firmware` extractor for owner's Windows-disc firmware; `*.mbn` repo guard | N. Johansson |
