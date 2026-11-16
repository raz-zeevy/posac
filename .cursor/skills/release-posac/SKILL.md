---
name: release-posac
description: Ship a new POSAC version - bump the version, build the installer, commit it, push to main, and notify users by email. Use when the user asks to release, deploy, publish, ship a version, bump the version, or send the update email.
disable-model-invocation: true
---

# Releasing POSAC

Publishing is done through the git repository itself: the committed
`releases/PosacSetupDebug.exe` is what users download, so **pushing to `main`
is the deployment**. The notification email is generated from the version
commit, which is why its wording matters.

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

Run it from the repository root. It produces `releases/PosacSetupDebug.exe`,
the console build, which is what is distributed during the beta - the console
is currently the only channel through which a user can see a crash, so it
stays until testing is done.

Confirm `releases/PosacSetupDebug.exe` changed size and timestamp before
continuing. The script exits non-zero on failure but check anyway.

Then publish the two names users actually download. Do this from the build
just produced, not from an older `dist`:

```
copy /Y releases\PosacSetupDebug.exe releases\POSAC-WIN-26P.exe
```

Rebuild `releases/POSAC-WIN-26Z.zip` from `dist\PosacDebug`: the zip's top
folder is `POSAC-WIN-26Z`, and it includes `releases/POSAC-WIN-26Z.txt`.
Commit both new files together with `PosacSetupDebug.exe`. The old installer
name stays in the repository so links already sent keep working.

| Download | File |
|---|---|
| Installer | `releases/POSAC-WIN-26P.exe` |
| Installer guide | `releases/POSAC-WIN-26P.txt` |
| Portable ZIP | `releases/POSAC-WIN-26Z.zip` |
| Portable guide | `releases/POSAC-WIN-26Z.txt` |
| Previous installer link | `releases/PosacSetupDebug.exe` |

`scripts/build.bat` builds the windowed customer version (`Posac.exe` ->
`releases/PosacSetup.exe`) and works, but is **not** distributed yet. Before
switching to it, two things must be settled: the error reporter is disabled
(`Controller.__init__` has `ErrorReporter` and `install_tk_exception_handler`
commented out, and `report_manual_error` would raise `AttributeError`), so a
windowed build discards every unhandled error silently; and the two installers
share an `AppId`, so Windows treats them as the same application.

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
| Distributed build | `scripts/build_debug.bat` -> `releases/PosacSetupDebug.exe` |
| Windowed build (not distributed yet) | `scripts/build.bat` -> `releases/PosacSetup.exe` |
| Download links | `releases/POSAC-WIN-26P.exe` and `releases/POSAC-WIN-26Z.zip` (old name `PosacSetupDebug.exe` still served) |
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
