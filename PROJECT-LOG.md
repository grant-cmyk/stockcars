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

## 16 Nov 2026 21:48 SAST - the oval, trial 1 (cloud session, Claude)
- Grant: "the track should be a little wider. And these cars will skid a lot"; ideas for weapons: "you can spit
  out oil behind you. You can shoot the car in front. Options".
- The oval is track 6 (tools/make_track_designs.py, track6_verts): two half-circle bends of radius 146, two
  straights of 132 px, map 72 x 55 tiles, start line at x 336. Road 88 px wide on this track (72 elsewhere).
- SKID=1 (build switch, src/grip.asm): your truck has about 60% of Breakfast Run's grip. A first guess.
- Trial tape: build/stockcars_oval_trial1.tap  (TRACK=6 SKID=1 bash build.sh). Picture: docs/design/trials/oval_trial1.png.
  It still LOOKS like Breakfast Run (tablecloth, cereal O's, mug, logo): only the track shape, width and grip changed.
- VERIFIED: TRACK=6 QUICK=1 python3 tests/track2_test.py - the script laps it in about 14.4 s, on the road 100%,
  three laps counted, podium comes up. Track 1's tape is still byte for byte Breakfast Run's.
- NOT VERIFIED: how the skid feels (not driven by a person); the computer cars' grip is unchanged.
- Two checks in that test FAIL and have not been looked into: "waypoints fit the one-byte progress" and "the
  cereal O's stand along the road's edges" (the test was written for a 72 px road; the O's are to go anyway).
- A lap is only about 14 seconds: races will need more laps, or a bigger oval (map height is free, width is not).
- Version: 0.2.0 (minor: a new track and a new build switch).

## 16 Nov 2026 22:45 SAST - the oval with the black road, trial 2 (cloud session, Claude)
- Grant on trial 1: "road is wide enough - but need the black road and design I am going for in the new breakfast
  run road track design".
- Brought across the Breakfast Run race-track trial (grant-cmyk/breakfastrun, branch claude/breakfast-run-layout-ik0vpe,
  commits 1f3e77e..ddf2236: src/racetrack.asm, rt_world.asm, the RACETRACK=1 switch, its tests). One conflict in
  tools/make_world.py, resolved keeping both the oval and the race track.
- Trial tape: build/stockcars_oval_trial2.tap
  (RACETRACK=1 TRACK=6 SKID=1 BDIR=oval_rt OUT=stockcars_oval_trial2 bash build.sh).
  Pictures from the real tape: docs/design/trials/oval_trial2.gif, oval_trial2_bend.png, oval_trial2_grid.png.
- VERIFIED (tests/rt_laps.py, 60 s race by autopilot): all five cars lap, about 16 s a lap. Track 1's plain tape is
  still byte for byte Breakfast Run's.
- CONCERN: 389 pictures in 60 s, about 6.5 a second - roughly half Breakfast Run's usual 12. Not looked into yet
  (the wider road and the long grass edges of an oval may be why). The game itself keeps its speed.
- NOT VERIFIED: tests/racetrack_test.py not run on the oval; feel and sound. A small notch shows in the grass edge
  on the first bend (see oval_trial2_bend.png). The panel, mug, logo and cars are still Breakfast Run's.
- Version: 0.3.0 (minor: the race-track look on the oval).

## 16 Nov 2026 22:50 SAST - bigger sprites asked for (cloud session, Claude)
- Grant: "I think for the stock car racing we will go for bigger sprites".
- Tried Breakfast Run's 20 x 20 big cars on the black-road oval (bash build.sh big with RACETRACK=1 TRACK=6): it does
  NOT fit - "the room under 0x8000 runs into the data kept at its top". Bigger trucks need a memory plan first.
- Mock-up of 16, 24 and 32 pixel trucks on the 88 px road: docs/design/mockups/truck_sizes.png
  (tools/mockups/make_size_mock.py, SC=1, 1.5, 2); added to the page docs/design/mockups/first_look.html.
  Claude recommends 24. Waiting for Grant to choose.

## 16 Nov 2026 22:51 SAST - truck size decided: 24 x 24 (cloud session, Claude)
- Grant: "24 is fine".
- Sum, not a measurement: a 24 x 24 frame with its mask is 144 bytes; 16 headings is 2,304 bytes a truck. Five
  different trucks would be 11,520 bytes (the small cars take 4,864 today) - too much. Proposal put to Grant: ONE
  truck body shared by all (colour is free: it is the square's colour, not the drawing), with each weapon a small
  separate drawing on the nose. Then the whole set is about 2,304 bytes plus the weapons, less with flipped frames.

## 16 Nov 2026 22:55 SAST - shared truck body agreed; the editor; why trial 2 is slow (cloud session, Claude)
- Grant: "yes" to one truck body shared by all, each weapon a separate drawing over it.
- tools/truck_art.txt: Claude's draft 24 x 24 body and six weapons (spike, hammer, tipper, saw, gun, oil).
  docs/tools/truck_editor.html (tools/make_truck_editor.py builds it from the template): published as the Claude
  artifact "Stock Cars Truck Editor", https://claude.ai/artifact/CjLeN5LA5Ky7xm1JuS72nt . Grant pastes his art back.
- MEASURED (tests/stage_profile.py, SCEN=pack, 8 s): plain engine, track 1: 12.6 pictures a second, 241,000 T a
  picture. Race-track look, track 1: 7.0 a second, 463,000 T. Race-track look, the oval: 7.1 a second, 462,000 T.
  So the slowness comes with the race-track look as Breakfast Run built it, NOT from the oval or the wider road.
  Biggest parts on the oval: screen copy 63,500, tiles 60,400 (15,000 on the plain engine), cars 22,700; the
  listed parts do not add up to the total - where the rest goes has not been found yet.
- NOT DONE: nothing in the game uses the 24 x 24 art yet.

## 16 Nov 2026 22:59 SAST - the 24 x 24 trucks are in the game, trial 3 (cloud session, Claude)
- Grant on Claude's draft trucks: "happy with trucks".
- TRUCKS=1 (tools/make_data.py, with the big cars: bash build.sh big): the truck (BODY + TRUCK_WEAPON, default
  HAMMER, from tools/truck_art.txt) goes through the big cars' pipeline - a 27 x 27 grid, a 24-wide frame - and all
  five trucks' table entries point at ONE set of frames. MEASURED: 1,620 bytes of pictures (the small cars: 4,864).
- src/racetrack.asm: the row of 24 stores is padded onto one page wherever the program puts it (the bigger build
  moved it across a page and the build stopped).
- Trial tape: build/stockcars_oval_trial3.tap
  (TRUCKS=1 RACETRACK=1 TRACK=6 SKID=1 BDIR=oval_rt_trucks OUT=stockcars_oval_trial3 bash build.sh big).
  Pictures from the tape: docs/design/trials/oval_trial3.gif, oval_trial3_grid.png, oval_trial3_bend.png.
- VERIFIED (tests/rt_laps.py, 60 s by autopilot): all five trucks lap, about 15.5 s a lap; 365 pictures = 6.1 a second.
- KNOWN FAULTS: (1) the slanted headings are turned by the computer and the wheels come out as solid lumps - they
  need tidying by hand (a 27 x 27 file like big_car_art_27.txt, or simpler wheels); a pixel or two is cut off the
  widest corners at 45 degrees by the 24-wide frame. (2) The race order on the right has lost its car pictures (it
  draws them from the frames, and 24 x 24 does not fit its 16 x 16 boxes). (3) Every truck has the hammer; nothing
  works as a weapon yet. (4) Trucks that touch share colour squares (one takes the other's colour).
- Version: 0.4.0 (minor: the trucks).
