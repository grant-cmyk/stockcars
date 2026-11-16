# Project log - Stock Cars (working title)

## 16 Nov 2026 21:32 SAST - project started (cloud session, Claude; Grant's TTRO Claude account, Personal work)
- Grant's brief, in order: a new stock car game for the 48K, "inspired by the ideas behind" Breakfast Run; an arena
  with a few obstacles where you build a truck with a special power ("a spike, a hammer, a tipper, you can build
  it") to stop the others; then: "lets go for a track ... each car is designed to have defence and weapons ...
  The track is oval shaped, with a short straight"; then: "This will need scrolling the whole track is not
  available in one screen".
- Decisions by Grant: the mock-ups' look ("I love the mockups"); scrolling option A, smooth, a pixel at a time
  ("A is good"); a weapon hit spins the victim ("I like the spin"); start from the Breakfast Run engine
  ("breakfast run engine is good"); repository private, named stockcars.
- Look carried over from Breakfast Run's racetrack work: black road, dashed white limit line, black run-off,
  green grass, each truck in its own colour.
- Done: mock-ups (docs/design/mockups, drawn by tools/mockups/*.py; run make_arena_mock.py, make_oval_mock.py,
  make_scroll_mock.py from that folder). Engine baseline copied from grant-cmyk/breakfastrun commit d2f8edf:
  src/, tools/, tests/, build.sh, docs/reference/OPTIMISATION-PLAN.md, docs/sound/TRANCE-SOUND-GUIDE.md.
  Not copied: Breakfast Run's docs (124 MB of pictures and sound) and its history.
- NOT VERIFIED: the baseline has not been built or run here. This container has pasmo but not the retro
  plugin's zxspectrum build script nor the zxdev emulator (the session is on the TTRO account, where the
  Personal plugins are not synced), so build.sh stops before assembling. No game code has been changed yet.
- Open (Grant): what happens to a truck with no armour left (out, or stopped then back); how you win (assumed:
  first to finish the laps); one or two players; the game's name.
- Version: 0.1.0, the baseline (first commit; minor numbers until there is a tape Grant has driven).

## 16 Nov 2026 21:37 SAST - the copied engine builds and passes (cloud session, Claude)
- Toolchain brought into the session by cloning beside this repository: grant-cmyk/claude-plugins-personal
  (the tape maker, plugins/retro/skills/zxspectrum/scripts/build.sh) and grant-cmyk/zx-emulator (built with
  sh build-linux.sh -> ../zx-emulator/zxdev).
- build.sh changed: it no longer dies when the retro plugin is not synced into Claude; it also looks in
  ../claude-plugins-personal, and says so plainly if it finds no tape maker.
- Added what the build and tests read: build/*.txt and *.json inputs, docs/design/tracks.
- VERIFIED: bash build.sh makes build/racer.tap byte for byte the same as Breakfast Run's (d2f8edf);
  tests/drive_test.py, lapcount_test.py, finish_test.py, damage_test.py all RESULT: PASS. The other suites not run.
- Version: 0.1.1 (patch: build fix only, the game unchanged).
