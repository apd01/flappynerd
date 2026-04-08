# FlappyNerd

A joke Flappy Bird clone where your friend is the bird.  
Built with **Expo + React Native + TypeScript**, runs on iOS and Android in portrait and landscape.

---

## Current Status

| Thing | Done? |
|-------|-------|
| Planning docs | ✅ `MANUAL_STEPS.md`, `CODE_STEPS.md` |
| Placeholder images | ✅ `assets/images/` — smiley face, sky, pipe tile, ground strip |
| Expo project scaffold | ⬜ Not yet |
| Game code | ⬜ Not yet |
| Real friend photo | ⬜ Waiting on Photoshop |

---

## Next Steps (in order)

1. **Scaffold the Expo project** — see [MANUAL_STEPS.md](MANUAL_STEPS.md) § 2  
2. **Install deps** — `npx expo install expo-screen-orientation expo-asset expo-image`  
3. **Write game code** — follow the 14-step build order in [CODE_STEPS.md](CODE_STEPS.md)  
4. **Test with Expo Go** — scan QR code from `npx expo start` on the same Wi-Fi  
5. **Swap in the real photo** — replace `assets/images/friend.png` with the Photoshopped PNG (150×150 px, transparent background)

---

## Project Structure (current)

```
FlappyNerd/
├── assets/
│   └── images/
│       ├── friend.png          placeholder smiley (replace with real photo)
│       ├── background.png      sky gradient
│       ├── pipe.png            green pipe tile
│       └── ground.png          grass + dirt strip
├── scripts/
│   └── generate_placeholders.py   regenerates placeholder PNGs (pure Python, no deps)
├── CODE_STEPS.md               full code architecture + 14-step build order
├── MANUAL_STEPS.md             installs, image prep, device testing, prod builds
└── README.md                   this file
```

---

## Quick Reference

```bash
# Regenerate placeholder images at any time
python3 scripts/generate_placeholders.py

# (After scaffold) Start dev server
cd FlappyNerd   # the Expo project subfolder, if you created one inside here
npx expo start

# (After scaffold) Add dependencies
npx expo install expo-screen-orientation expo-asset expo-image
```

---

## Image Requirements (for the real photo)

- Format: PNG with **transparency** (alpha channel)
- Size: 150 × 150 px (optionally also `@2x` 300×300 and `@3x` 450×450)
- Drop it at: `assets/images/friend.png`
- The transparent background means the sky shows through — no extra config needed

---

## Docs

- [MANUAL_STEPS.md](MANUAL_STEPS.md) — what **you** do (installs, image prep, device testing, prod builds)
- [CODE_STEPS.md](CODE_STEPS.md) — full code plan (architecture, components, game loop, collision, orientation)
