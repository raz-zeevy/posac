---
name: release-posac
description: Ship a new POSAC version - bump the version, build the installer, commit it, push to main, and notify users by email. Use when the user asks to release, deploy, publish, ship a version, bump the version, or send the update email.
disable-model-invocation: true
---

# Releasing POSAC

Publishing is done through the git repository itself: the committed
`releases/PosacSetupDebug.exe` is what users download, so **pushing to `main` is
the deployment**. The notification email is generated from the version commit,
which is why its wording matters.

Run every command from the repository root with `venv\Scripts\python.exe`, not a
bare `python` (the app targets 32-bit Python 3.7).

## Workflow

Track progress with a todo list:

```
- [ ] Step 1: Preflight
- [ ] Step 2: Bump the version
- [ ] Step 3: Build the installer
- [ ] Step 4: Commit
- [ ] Step 5: Push          (needs approval)
- [ ] Step 6: Notify users  (needs approval)
```

Steps 1-4 run unattended. Steps 5 and 6 are irreversible - stop and get an
explicit go-ahead for each.

### Step 1: Preflight

- Show `git status` and summarise what is going out.
- Run the test suite: `venv\Scripts\python.exe -m pytest`.
- If `lib/help/posac.txt` changed since `lib/help/posac_help.bin` was written,
  recompile it: `venv\Scripts\python.exe -m lib.help.help_compiler`.
  The binary is bundled by `app.spec`, so a stale one ships stale help.

### Step 2: Bump the version

`lib/__version__.py` is the single source. Both batch files parse it back out of
that file, and `build.bat` aborts unless it has exactly four components.

Ask which component moves if it is not obvious from the change.

### Step 3: Build the installer

```
cmd /c "scripts\build_debug.bat"
```

Run it from the repository root - its paths are relative to the root, unlike
`build.bat`, which starts with `cd ../` and expects to run from `scripts/`.

Despite the name this is the release build - it is the only script that runs
both PyInstaller and Inno Setup, and it produces `releases/PosacSetupDebug.exe`,
the file users download. `build.bat` has its PyInstaller line commented out and
produces an untracked `PosacSetup.exe` that nothing references; ignore it.

Confirm `releases/PosacSetupDebug.exe` changed size and timestamp before
continuing. The script exits non-zero on failure but check anyway.

### Step 4: Commit

Stage the source changes **and** the rebuilt installer together.

The message format is parsed, not decorative:

```
Version X.Y.Z.W: <summary of what changed>
```

`GitUpdateNotifier.get_latest_commit_info` matches `^Version (\d+\.\d+\.\d+\.\d+)`
against the last commit. The first line becomes the email title and everything
after it becomes the email body, so write it for the customer rather than for
the repository. If the pattern does not match, the email subject silently falls
back to today's date.

Never pass `--no-verify`: `.githooks/commit-msg` strips the agent attribution
trailer that the editor injects after the message is written, and it would
otherwise reach customers in the email body. A fresh clone must enable it once
with `git config core.hooksPath .githooks`.

Show the drafted message before committing.

### Step 5: Push

```
git push origin main
```

Required before the email - the download link serves `main`, so until the push
lands users would get the previous installer.

### Step 6: Notify users

```
venv\Scripts\python.exe scripts/email/send_update_email.py --debug
```

`--debug` sends only to the address in `DEBUG_RECIPIENTS`. Wait for the user to
confirm the test copy reads correctly, then send for real:

```
venv\Scripts\python.exe scripts/email/send_update_email.py
```

The email reads whatever commit is currently `HEAD`, so do not commit anything
else between step 4 and here.

## Reference

| Thing | Where |
|---|---|
| Version | `lib/__version__.py` |
| Release build | `scripts/build_debug.bat` |
| Installer users download | `releases/PosacSetupDebug.exe` (tracked in git) |
| Download link | `raw.githubusercontent.com/raz-zeevy/posac/main/releases/PosacSetupDebug.exe` |
| Email entry point | `scripts/email/send_update_email.py` |
| Email body builder | `scripts/email/git_update_notifier.py` |
| Recipients | `scripts/email/config/email_recipients.py` (gitignored) |
| Gmail credentials | `.env` - `GMAIL_USER`, `GMAIL_APP_PASSWORD` (gitignored) |

The email goes out BCC to four production recipients.

## What the engine actually needs at runtime

The GUI only ever launches `PXPOS.BAT`, which calls `TNWPOSAC_32.exe`,
`SLSA1_32.exe`, `SLSA2_32.exe`, `SSHEMOR_32.exe` and `POSACSEP_32.exe`.
Everything else in `lib/scripts/IdoPosac/` is Fortran source, build output,
documentation, or the pre-GUI DOS shell, so `app.spec` lists those six files
individually rather than globbing the folder. Add a new entry there if the
engine ever gains a step - a missing one only surfaces when a run fails.
