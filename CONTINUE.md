# CONTINUE - Stock Cars (working title)

Stamped: 16 Nov 2026 21:32 SAST. Machine: Claude cloud container (no local machine). Commit: the one that adds this file (see git log -1).
Repository: GitHub grant-cmyk/stockcars (private), branch main. Identity: Personal. Classification: Internal.

## What this is
Weapon trucks racing on a scrolling oval, ZX Spectrum 48K, built on a copy of the Breakfast Run engine.

## State
- Mock-ups approved by Grant: docs/design/mockups/ (first_look.html holds all of them; also published as the
  Claude artifact "Weapon Trucks First Look", https://claude.ai/artifact/CtdUDu4nhiX9xPkeNJWh9F).
- Engine baseline copied in, UNCHANGED and UNBUILT here: it is still Breakfast Run (its tracks, cars, title).
- Decided: oval with short straights, bigger than the screen; smooth scrolling; a hit spins the victim; each
  truck has a weapon and a defence; black road / green grass look.

## Next, in order
1. Get the toolchain into the session: the retro plugin's zxspectrum build script (GitHub
   grant-cmyk/claude-plugins-personal) and the zxdev emulator (GitHub grant-cmyk/zx-emulator). Build the
   baseline and run tests/run_all.sh to prove the copy works before changing anything.
2. Replace the track with the oval (tools/make_world.py makes the world, waypoints and mini-map).
3. Add the hammer and the spin behind a build switch; make a trial tape for Grant to drive.
4. Then: the other weapons, defence, the build-your-truck screen (src/choose.asm is the starting point).
Read docs/reference/OPTIMISATION-PLAN.md before adding anything: Breakfast Run ended with about 23 bytes free.

## Waiting on Grant
- What happens to a truck with no armour left; how you win; one or two players; the name.
- Notion Workstreams row: not created (this session is on the TTRO account; the row belongs under Personal).
