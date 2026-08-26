# Veragensia overlay (on top of stock Omarchy)

This directory is the **Focusa layer** that installs *on top of* an untouched Omarchy base.
Keeping it separate is the maintainability key: Omarchy stays upstream and updates merge for free;
Veragensia adds only branding + services + GUI.

- `themes/` — Focusa-branded Hyprland theme (colors, logo, cursor, splash), waybar styling.
- `services/` — systemd units: Focusa daemon, UIAI Engine, IPC bus, notification/audit daemons.
- `gui/` — QML Focusa shell (start page / wall / command panel as native desktop surfaces).

Nothing here patches upstream Omarchy files.
