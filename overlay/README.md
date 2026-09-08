# Veragensia overlay (on top of stock Omarchy)

This directory is the **Focusa layer** that installs *on top of* an untouched Omarchy base.
Keeping it separate is the maintainability key: Omarchy stays upstream and updates merge for free;
Veragensia adds only branding + services + GUI.

- `themes/` — Focusa-branded Hyprland theme (colors, logo, cursor, splash), waybar styling.
- `services/` — systemd units: Focusa daemon, UIAI Engine, IPC bus, notification/audit daemons.
- Native Work presentation uses the verified upstream interface, currently Waybar via `scripts/veragens status --waybar` and the inert `config/waybar-work.jsonc` example. No separate QML shell is supplied or assumed; Doc 182b §A.4 governs future adjustments.

Nothing here patches upstream Omarchy files.
