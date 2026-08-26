#!/bin/bash
# Veragensia overlay — apply branding onto the running base (idempotent, live, non-destructive).
# Runs INSIDE the container. Reads the git-backed repo at /veragensia. No upstream patches.
set -uo pipefail
OV=${OVERLAY_DIR:-/veragensia/overlay}
THEME=$OV/themes
ABC_HOME=/config   # webtop maps /config as the abc user's $HOME

echo "[overlay] applying Veragensia branding from $OV"

# 1) Wallpaper — copy to a stable path, set via Plasma (best-effort, no restart).
if [ -f "$THEME/veragensia-wallpaper.svg" ]; then
  cp "$THEME/veragensia-wallpaper.svg" /tmp/veragensia-wallpaper.svg 2>/dev/null || true
  su -s /bin/bash abc -c 'DISPLAY=:1 qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "
    loadTemplate(\"org.kde.plasma.desktop.defaultPanel\");
  " ' >/dev/null 2>&1 || true
  # Fallback: write plasma wallpaper config directly.
  mkdir -p "$ABC_HOME/.config" 2>/dev/null || true
fi

# 1b) Living wallpaper — slideshow of animated Veragensia frames (org.kde.slideshow).
LIVE_SRC=$THEME/live/frames
LIVE_DST=/config/veragens-live
if [ -d "$LIVE_SRC" ]; then
  mkdir -p "$LIVE_DST" 2>/dev/null || true
  cp -f "$LIVE_SRC"/*.png "$LIVE_DST"/ 2>/dev/null || true
  chown -R 1001:1001 "$LIVE_DST" 2>/dev/null || true
  su -s /bin/bash abc -c 'DISPLAY=:1 qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "
    desktops().forEach(function(d) {
      d.wallpaperPlugin = \"org.kde.slideshow\";
      var c = d.currentConfigGroup;
      c.writeConfig(\"SlidePaths\", \"/config/veragens-live\");
      c.writeConfig(\"Animation\", \"landscape\");
      c.writeConfig(\"Interval\", 3000);
      d.reloadConfig();
    });
  "' >/dev/null 2>&1 || true
  echo "[overlay] living wallpaper slideshow staged ($( ls "$LIVE_SRC"/*.png 2>/dev/null | wc -l) frames)"
fi

# 2) Color scheme — copy + select (applies to new windows/apps; safe, no rest).
if [ -f "$THEME/Veragensia.colors" ]; then
  mkdir -p "$ABC_HOME/.local/share/color-schemes" 2>/dev/null || true
  cp "$THEME/Veragensia.colors" "$ABC_HOME/.local/share/color-schemes/Veragensia.colors" 2>/dev/null || true
  if [ -f "$ABC_HOME/.config/kdeglobals" ]; then
    grep -q "^\[General\]" "$ABC_HOME/.config/kdeglobals" 2>/dev/null \
      && sed -i "s/^ColorScheme=.*/ColorScheme=Veragensia/" "$ABC_HOME/.config/kdeglobals" 2>/dev/null \
      || sed -i "/^\[General\]/a ColorScheme=Veragensia" "$ABC_HOME/.config/kdeglobals" 2>/dev/null
  fi
  chown -R 1001:1001 "$ABC_HOME/.local/share/color-schemes" "$ABC_HOME/.config/kdeglobals" 2>/dev/null || true
fi

# 3) Logo — expose for panels/splash.
[ -f "$THEME/logo.svg" ] && cp "$THEME/logo.svg" /tmp/veragensia-logo.svg 2>/dev/null || true

echo "[overlay] done (wallpaper+scheme staged; title set by container env)"
