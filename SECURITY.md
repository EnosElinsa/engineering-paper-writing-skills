# Security policy

## Scope

The skills are Markdown instructions read by an agent. The bundled `style_fingerprint.py` uses only the Python standard library, reads the files it is given, and writes only to standard output or to the file named with `--out`. The repository tools under `scripts/` write only inside the repository (`sync_shared.py`, and `calibrate_house_style.py --write`). None of them makes network requests or runs other programs.

A security issue here is, for example, a skill instruction that could lead an agent to leak manuscript content, run an unexpected command, or write outside the files the user named, or a script that reads or writes paths it was not given.

## Reporting

Please report a vulnerability privately through [GitHub security advisories](https://github.com/EnosElinsa/engineering-paper-writing-skills/security/advisories/new) instead of a public issue. Include the affected skill or script, the steps to reproduce, and the impact. You can expect a first answer within a week.

## Supported versions

Only the latest release receives fixes. Update with `npx skills update -g`.
