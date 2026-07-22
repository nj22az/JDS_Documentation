# CHANGELOG — JDS-PRJ-SFW-003 Pocket Linux

Master change log for the Pocket Linux project (custom Linux distro for the
Sony Vaio P). Every change to the build system, overlay, or documentation is
recorded here.

---

## Rev D — 2026-07-22 — WWAN via owner's Windows-disc firmware

**Scope:** make the optional Gobi 2000 mobile-broadband/GPS module work,
using firmware from the owner's original Windows driver discs.

- Clarified the principle in the docs: Windows driver *code* is never used —
  all drivers are native Linux. The Gobi module is a pure *data* dependency:
  three firmware files (`amss.mbn`, `apps.mbn`, `UQCN.mbn`) that Sony ships
  only inside the Windows package.
- Added the WWAN stack to the image: `modemmanager`, `usb-modeswitch`,
  `gobi-loader` (uploads firmware at boot), `p7zip-full` (unpacks installer
  `.exe`/`.cab` archives on the disc).
- New **`pocket-gobi-firmware`** tool: point it at the mounted disc or an
  extracted driver folder; it locates the three files case-insensitively,
  prompts for the carrier variant of `UQCN.mbn` when several exist, and
  installs to `/lib/firmware/gobi/` with next-step instructions (`mmcli -L`,
  connect via the network tray icon).
- Licensing guard: firmware is per-machine and never redistributable —
  `*.mbn` added to the repository `.gitignore` so it can never be committed
  by accident; warning printed by the tool and stated in README/reference.
- Help page and hardware reference updated (WWAN/GPS rows now "works after
  one-time firmware install"; step-by-step extraction guide added, including
  the no-optical-drive note: use a USB DVD drive or copy the disc to USB).

## Rev C — 2026-07-22 — Driver completeness & hardware self-test

**Scope:** close every driver/userspace gap found in a full audit of the
support matrix, and make driver health verifiable on the real machine.

- **Gaps found and closed:**
  - Bluetooth had the kernel driver (`btusb`) but **no userspace** — added
    `bluez`, `blueman` (Menu > Bluetooth), and `pulseaudio-module-bluetooth`
    so headphones/mice/phones pair and audio routes automatically.
  - Brightness Fn keys did nothing in X — added `brightnessctl` and mapped
    `XF86MonBrightness*` in the IceWM keys file.
  - SD/SDXC cards and Windows USB disks — added `dosfstools`, `exfatprogs`,
    `ntfs-3g`.
  - Added `intel-microcode`, `firmware-realtek` (for future USB dongles —
    the machine has no built-in ethernet), and diagnostics (`pciutils`,
    `usbutils`, `rfkill`).
- **New `pocket-check` hardware self-test** (Menu > Hardware Self-Test):
  read-only sysfs checks, one PASS/FAIL line per device — graphics/KMS,
  native panel mode, backlight, HDA sound + PCM device, keyboard,
  trackpoint, sony-laptop hotkeys, ath9k + wlan interface, radio kill
  switch, Bluetooth adapter, webcam, battery, PATA disk, zram, earlyoom —
  each FAIL carries a fix hint; exit code = number of failures. Verified
  the script runs cleanly (18/18 checks correctly FAIL on a cloud VM with
  none of the hardware).
- Help page: new "Is all my hardware working?" and Bluetooth sections;
  brightness keys documented.
- Hardware reference: Bluetooth/storage/backlight rows updated; new
  "Verifying Drivers on the Real Machine" section.

## Rev B — 2026-07-22 — Usability layer & free assets

**Scope:** make the desktop clear and straightforward out of the box.

- **Free assets, sourced from Debian main only** (DFSG-licensed — no third-party
  asset sites, so provenance and licences are clean by construction):
  Greybird GTK theme, elementary-xfce icon theme, DMZ-White cursors (32 px for
  the 222 DPI panel), murrine engine for GTK2 apps.
- **Original wallpaper**: 1600×768 navy-gradient PNG (5.3 KB) generated
  in-project with pure-Python PNG encoding; released CC0. Drawn once by
  icewmbg — zero runtime cost.
- **Clear navigation**: custom IceWM start menu with plain-English task-first
  entries + auto-generated "All Programs" fallback; taskbar quick-launch
  (browser / files / terminal); nm-applet + volumeicon tray applets
  autostarted.
- **Keyboard shortcuts**: Super+Enter/E/W/H (terminal, files, browser, help)
  and Fn volume keys.
- **Built-in help**: `pocket-help` command + Menu > Help + Super+H opens
  `/usr/share/doc/pocket-linux/help.txt` (Wi-Fi, apps, shortcuts, mpv video
  streaming, font-size adjustment, updates).
- **Sane app defaults** via skel `mimeapps.list`: links → NetSurf, media → mpv,
  images → GPicView, text → Mousepad, folders → PCManFM.
- **Trackpoint scrolling**: middle-button + stick scrolling (ThinkPad-style)
  via libinput Xorg InputClass.
- **Consistent look**: GTK2 + GTK3 settings mirrored in skel; animations off
  (every frame is CPU-rendered).
- `tune-vaio-p.sh` now copies the whole overlay root (`/etc` **and** `/usr`)
  and chowns all skel entries generically, so Path B stays byte-identical to
  the ISO.

## Rev A — 2026-07-22 — Initial release

**Scope:** first complete, reproducible build system.

- Chose **Debian 12 "bookworm" i386 + live-build** as the base after surveying
  the 2026 i686 landscape:
  - Debian 13 "trixie" dropped the i386 kernel/installer → bookworm is the last
    mainstream base with LTS coverage (to ≈ June 2028).
  - antiX 23 / Void i686 remain viable and are the designated **rebase
    candidates** when bookworm LTS ends.
  - Tiny Core / Alpine rejected: too much daily friction (musl/glibc gaps,
    manual persistence) for a daily-driver goal.
- Created `build/build.sh` — one-command hybrid ISO build (BIOS-bootable,
  includes the Debian installer for hard-disk installation).
- Created the package manifest (`pocket.list.chroot`): IceWM desktop,
  NetSurf + Firefox ESR, cmus, mpv, PCManFM, NetworkManager, zram-tools,
  earlyoom — no display manager, no compositor, no desktop environment.
- Created the tuning overlay (`build/config/includes.chroot/`), the single
  source of truth for all machine-specific configuration:
  - Xorg pinned to `modesetting` with glamor (GL) disabled — GMA 500 safe path
  - zram at 50 % RAM with zstd; sysctls tuned for zram-first swapping
    (`swappiness=180`, `page-cluster=0`) and a slow PATA disk (low dirty ratios)
  - GRUB drop-in: `mitigations=off`, `TER16x32` console font for the 222 DPI panel
  - `/etc/skel` dotfiles: `startx` → IceWM session, `Xft.dpi: 144` (1.5× scale)
  - `gma500_gfx` added to initramfs for early KMS (native console resolution
    from the first second of boot)
- Created `install/tune-vaio-p.sh` — applies the identical overlay + package
  set to an existing Debian 12 i386 installation (Path B, no ISO rebuild).
- Wrote `docs/hardware-reference.md` — full Vaio P hardware support matrix
  (kernel module per device, status, quirks), including the WWAN/Gobi firmware
  caveat and suspend/resume fragility note.
- Registered JDS-PRJ-SFW-003 in the document register; added the missing
  Software Projects section to `projects/index.md`.
