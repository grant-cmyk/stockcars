# CONTINUE - Stock Cars (working title)

Stamped: 17 Nov 2026 06:36 SAST. Machine: Claude cloud container (no local machine). Commit: the one that adds this file (see git log -1).
Repository: GitHub grant-cmyk/stockcars (private), branch main. Identity: Personal. Classification: Internal.

## What this is
Weapon trucks racing on a scrolling oval, ZX Spectrum 48K, built on a copy of the Breakfast Run engine.

## State
- Mock-ups approved by Grant: docs/design/mockups/ (first_look.html holds all of them; also published as the
  Claude artifact "Weapon Trucks First Look", https://claude.ai/artifact/CtdUDu4nhiX9xPkeNJWh9F).
- Engine baseline copied in, unchanged, built and tested: it is still Breakfast Run (its tracks, cars, title).
- Decided: oval with short straights, bigger than the screen; smooth scrolling; a hit spins the victim; each
  truck has a weapon and a defence; black road / green grass look.

## Next, in order
1. DONE: the baseline builds (same bytes as Breakfast Run) and four suites pass. In a new cloud session:
   clone grant-cmyk/claude-plugins-personal and grant-cmyk/zx-emulator beside this repository, run
   sh build-linux.sh in zx-emulator, then bash build.sh here.
2. STARTED: the oval is track 6, 88 px road, loose grip behind SKID=1. Trial tape
   build/stockcars_oval_trial1.tap (TRACK=6 SKID=1 bash build.sh) - waiting for Grant to drive it. Still to do:
   the black road / green grass look, remove the cereal O's and breakfast things, look into the two failing checks.
3. Add the hammer and the spin behind a build switch; make a trial tape for Grant to drive.
4. Then: the other weapons, defence, the build-your-truck screen (src/choose.asm is the starting point).
Read docs/reference/OPTIMISATION-PLAN.md before adding anything: Breakfast Run ended with about 23 bytes free.

## Latest tape
build/stockcars_oval_trial7.tap: the oval, black road, grass edge with NO limit line (decided), 20 x 20 hammer trucks,
loose grip, Breakfast Run's speed work, the title's trucks fixed.
(TRUCKS=1 RACETRACK=1 TRACK=6 SKID=1 RT_NOLINE=1 BDIR=oval_rt_b OUT=stockcars_oval_trial7 bash build.sh big)
Known faults and what is next: the last entries of PROJECT-LOG.md. Next piece of work: the hammer and the spin.

## Waiting on Grant
- Drive trial 7: truck size, any more drawing faults. (Skid: "good" on trial 3 - keep SKID=1.)
- Truck art: 24 x 24, ONE shared body + weapon drawings (agreed). Grant to redraw Claude's drafts in the editor
  (https://claude.ai/artifact/CjLeN5LA5Ky7xm1JuS72nt) and paste the text back -> tools/truck_art.txt.
- Drive build/stockcars_oval_trial2.tap (black road, green grass; RACETRACK=1 TRACK=6 SKID=1 BDIR=oval_rt
  OUT=stockcars_oval_trial2 bash build.sh): the look, and is the skid enough? Road width: agreed, 88 px.
- Known: about 7 pictures a second with the race-track look (12.6 without) on ANY track - it comes from the look as
  Breakfast Run built it. Next: find where the unlisted T-states go (tests/stage_profile.py), and take any speed-up
  the Breakfast Run session makes to src/racetrack.asm.
- Weapon ideas he raised, to be offered as options on the build screen: oil dropped behind, a shot at the car in front.
- What happens to a truck with no armour left; how you win; one or two players; the name.
- Notion Workstreams row: not created (this session is on the TTRO account; the row belongs under Personal).
