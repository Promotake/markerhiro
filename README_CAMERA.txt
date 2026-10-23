LR4 CAMERA FIX - GITHUB PAGES

ROOT PAGES
- index.html: full-screen live camera in AR.js video-texture mode.
- hiro_preset.html: same page, retained for backward compatibility.
- camera_fallback.html: alternative live camera layer if an iPhone browser
  fails to show the video texture. This page also has no UI controls.

The custom black-and-white square marker is unchanged.
Both pages use marker/square_marker.patt and assets/models/astrabot.glb.

TO UPDATE AN EXISTING REPOSITORY
1. Upload the three HTML files from this patch into the repository root.
2. Commit changes (existing model and marker files remain untouched).
3. Open https://promotake.github.io/markerhiro/?v=camerafix4
4. Point the phone toward the NEW square marker, not the old HIRO.
5. If camera footage is still black on this device, try:
   https://promotake.github.io/markerhiro/camera_fallback.html?v=camerafix4

The page displays no headings, buttons, menus or overlays.
HTTPS and camera permission are required.
