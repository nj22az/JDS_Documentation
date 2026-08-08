# The Venture — Step 19 Prose Pass Report

Status: source-level prose pass materially advanced; Chapter Five compression complete and wired into final assembly. Full contiguous-manuscript read remains dependent on materialising the generated assembly.

## What changed in this step

### 1. Chapter Five pacing problem isolated

The chapter's storm, illness, pay-table and Arthur movements remain structurally necessary.

The excess was concentrated in Section III, where routine shipboard life repeated several already-established ideas before the flux begins.

The revision therefore does **not** cut:

- Jack's first climb;
- the buntline incident and Tom striking him out of danger;
- Pritchard's marline-spike mistake;
- the half-wage/full-ration dispute;
- the beetle joke;
- the water-shortage entry;
- the onset of the flux;
- nineteen deaths;
- the white-hook storm;
- Jack saving Tom;
- Pritchard's injury;
- the inquiry;
- the shorter-mast repair;
- Bantam arrival;
- the later pay-table conflict;
- Jack's refusal of a second voyage;
- Arthur's parallel development.

### 2. Finished replacement prose written

Created:

`manuscript-editorial/11-1613-pay-table-section-iii-natural-compression.md`

The compressed section keeps the necessary daily-life beats while removing extended repetitions of:

- waking/dressing congestion;
- beakhead routine;
- multiple passes through deck scrubbing;
- prolonged oakum practical joke;
- repeated serving practice;
- heat/coil/watch-change detail already established elsewhere.

The new movement is:

Tom's voice -> Pritchard's punishment -> half-wage ration dispute -> bad beer/water -> beetle joke -> water shortage -> compact routine montage -> belonging -> one serving lesson -> sick sailor says he is cold -> flux.

This preserves the reader's sense of shipboard life while reaching the chapter's next irreversible event sooner.

### 3. Final assembly entrypoint created

Created:

`scripts/assemble_venture_natural_final.py`

This wrapper applies the finished Chapter Five replacement on top of the existing deterministic natural-revision assembly logic.

### 4. Protected workflow updated

`.github/workflows/assemble-venture-natural.yml` now runs:

`scripts/assemble_venture_natural_final.py`

and watches both assembly scripts plus manuscript-editorial sources.

### 5. Branch state

At the end of the source-level pass, `agent/venture-natural-opening` is **36 commits ahead of `main` and 0 behind**.

No deployed/live canon file has been overwritten.

## Editorial result

The largest remaining pacing problem in Book One has now been handled in prose rather than left as a recommendation.

The chapter remains deliberately long because the reader must live through the voyage before the Company's later arithmetic has emotional weight. The revision cuts repetition, not duration of consequence.

## Remaining Step 19 work

The deterministic assembler already encodes the major approved cuts in Chapters Four, Seven, Eight, Nine, Ten and Eleven.

What cannot be honestly completed until the contiguous generated manuscript is materialised is the final cover-to-cover sentence pass for:

- accidental repetition created at chapter joins;
- remaining clusters of `machine`, `account`, `entry`, `paper`, `truth` and `room` language;
- repeated aphoristic sentence shapes;
- local rhythm after chapter compression;
- exact revised total word count.

The repository workflow did not execute from connector-authored commits during this session, so the generated `assembled/the-venture-natural-revision.md` is not being claimed as present.

## Step 19 judgement

The prose revision is now structurally ready for a single-manuscript read. The remaining pass is copyedit/echo control, not another redevelopment of the novel.
