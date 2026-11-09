# Subtitle Toolkit

A small command-line utility to validate, shift, and clean SubRip (`.srt`) subtitle files.

## Commands
```bash
python subtitle_tool.py validate captions.srt
python subtitle_tool.py shift captions.srt --milliseconds 750 --output captions-shifted.srt
python subtitle_tool.py clean captions.srt --output captions-clean.srt
```

- `validate` checks cue numbering, timestamps, and basic cue structure.
- `shift` moves all cue times forward/backward without allowing negative timestamps.
- `clean` removes blank cues and normalizes numbering.

Python 3.10+, standard library only. Review Hindi Unicode output in your target video editor before publishing.
