# CHANGELOG — JDS-PRJ-SFW-003 Pocket Linux

Master change log for the Pocket Linux project (custom Linux distro for the
Sony Vaio P). Every change to the build system, overlay, or documentation is
recorded here.

---

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
