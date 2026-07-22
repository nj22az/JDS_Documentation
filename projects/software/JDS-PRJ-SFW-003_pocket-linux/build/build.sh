#!/bin/sh
# Pocket Linux ISO builder — JDS-PRJ-SFW-003
#
# Builds a BIOS-bootable hybrid ISO (live session + Debian installer) for the
# Sony Vaio P using Debian live-build. Run as root on any Debian/Ubuntu host
# (amd64 hosts build i386 images natively — no emulation needed).
#
# Usage:  sudo ./build.sh          build the ISO into this directory
#         sudo ./build.sh clean    remove all build artifacts
set -eu

# ---- Build configuration (all tunables live here) ---------------------------
DISTRO_NAME="pocket-linux"
DISTRO_VERSION="1.0"
DEBIAN_SUITE="bookworm"            # last Debian release with an i386 kernel
TARGET_ARCH="i386"
KERNEL_FLAVOUR="686-pae"           # Atom Z5xx has PAE+NX; PAE enables NX
ARCHIVE_AREAS="main contrib non-free-firmware"
DEBIAN_MIRROR="http://deb.debian.org/debian/"
# Live-session kernel command line (mirrors /etc/default/grub.d/pocket.cfg in
# the overlay, which covers the installed system):
LIVE_BOOTAPPEND="boot=live components quiet mitigations=off fbcon=font:TER16x32"
ISO_NAME="${DISTRO_NAME}-${DISTRO_VERSION}-${TARGET_ARCH}.iso"
# -----------------------------------------------------------------------------

build_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$build_dir"

require_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "error: live-build needs root — run with sudo" >&2
        exit 1
    fi
}

require_live_build() {
    if ! command -v lb >/dev/null 2>&1; then
        echo "error: live-build is not installed — run: apt install live-build" >&2
        exit 1
    fi
}

clean_build() {
    lb clean --purge
    rm -f "$ISO_NAME" live-image-*.iso
}

configure_build() {
    # 'config/' already holds our package list, overlay and hooks; lb config
    # fills in the rest of the live-build tree around them.
    lb config \
        --architecture "$TARGET_ARCH" \
        --distribution "$DEBIAN_SUITE" \
        --archive-areas "$ARCHIVE_AREAS" \
        --mirror-bootstrap "$DEBIAN_MIRROR" \
        --linux-flavours "$KERNEL_FLAVOUR" \
        --binary-images iso-hybrid \
        --debian-installer live \
        --debian-installer-gui false \
        --bootappend-live "$LIVE_BOOTAPPEND" \
        --iso-application "$DISTRO_NAME" \
        --iso-volume "$DISTRO_NAME $DISTRO_VERSION" \
        --memtest none
}

run_build() {
    lb build
    mv live-image-"$TARGET_ARCH".hybrid.iso "$ISO_NAME"
    echo "OK: built $ISO_NAME"
    echo "Write to USB:  dd if=$ISO_NAME of=/dev/sdX bs=4M status=progress conv=fsync"
}

require_root
require_live_build
case "${1:-build}" in
    clean) clean_build ;;
    build) configure_build && run_build ;;
    *)     echo "usage: $0 [build|clean]" >&2; exit 1 ;;
esac
