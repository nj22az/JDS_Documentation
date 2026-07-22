#!/bin/sh
# Vaio P tuner for an existing Debian 12 i386 install — JDS-PRJ-SFW-003
#
# Path B: instead of building the Pocket Linux ISO, apply the identical
# package set and tuning overlay to a minimal Debian 12 (bookworm) i386
# system already installed on the Vaio P.
#
# The overlay in ../build/config/includes.chroot/ is the single source of
# truth — this script copies it verbatim, so ISO and tuned-install stay in
# sync by construction.
#
# Usage:  sudo ./tune-vaio-p.sh
set -eu

# ---- Locations (all tunables live here) -------------------------------------
project_root="$(cd "$(dirname "$0")/.." && pwd)"
OVERLAY_DIR="$project_root/build/config/includes.chroot"
PACKAGE_LIST="$project_root/build/config/package-lists/pocket.list.chroot"
EXPECTED_SUITE="bookworm"
EXPECTED_ARCH="i386"
# -----------------------------------------------------------------------------

require_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "error: run with sudo" >&2
        exit 1
    fi
}

check_target_system() {
    arch="$(dpkg --print-architecture)"
    if [ "$arch" != "$EXPECTED_ARCH" ]; then
        echo "error: this system is '$arch', expected $EXPECTED_ARCH (the Vaio P cannot run 64-bit)" >&2
        exit 1
    fi
    if ! grep -q "$EXPECTED_SUITE" /etc/os-release; then
        echo "warning: expected Debian $EXPECTED_SUITE — proceeding, but the package set is untested here" >&2
    fi
}

enable_nonfree_firmware() {
    # firmware-atheros/-misc-nonfree live in non-free-firmware
    if ! grep -Rqs "non-free-firmware" /etc/apt/sources.list /etc/apt/sources.list.d/; then
        sed -i 's/^\(deb .*bookworm.* main\)$/\1 contrib non-free-firmware/' /etc/apt/sources.list
    fi
}

install_packages() {
    # The chroot list is plain package names + comments — usable directly.
    apt-get update
    grep -v '^\s*#' "$PACKAGE_LIST" | grep -v '^\s*$' | xargs apt-get install -y
}

apply_overlay() {
    # Verbatim copy of the image overlay: Xorg, sysctl, zram, GRUB, initramfs.
    cp -rv "$OVERLAY_DIR/etc/." /etc/
    # skel only helps future users — also offer it to the invoking user
    invoking_user="${SUDO_USER:-}"
    if [ -n "$invoking_user" ] && [ "$invoking_user" != "root" ]; then
        invoking_home="$(getent passwd "$invoking_user" | cut -d: -f6)"
        cp -rnv "$OVERLAY_DIR/etc/skel/." "$invoking_home/"
        chown -R "$invoking_user:$invoking_user" \
            "$invoking_home/.xinitrc" "$invoking_home/.Xresources" "$invoking_home/.icewm"
    fi
}

activate_changes() {
    sysctl --system >/dev/null
    systemctl restart zramswap.service
    systemctl enable earlyoom.service
    update-initramfs -u
    update-grub
}

require_root
check_target_system
enable_nonfree_firmware
install_packages
apply_overlay
activate_changes
echo "OK: Vaio P tuning applied. Reboot, log in on the console, and run: startx"
