# CONTINUE - Stock Cars (working title)

Stamped: 16 Nov 2026 21:37 SAST. Machine: Claude cloud container (no local machine). Commit: the one that adds this file (see git log -1).
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
2. Replace the track with the oval (tools/make_world.py makes the world, waypoints and mini-map).
3. Add the hammer and the spin behind a build switch; make a trial tape for Grant to drive.
4. Then: the other weapons, defence, the build-your-truck screen (src/choose.asm is the starting point).
Read docs/reference/OPTIMISATION-PLAN.md before adding anything: Breakfast Run ended with about 23 bytes free.

## Waiting on Grant
- What happens to a truck with no armour left; how you win; one or two players; the name.
- Notion Workstreams row: not created (this session is on the TTRO account; the row belongs under Personal).
