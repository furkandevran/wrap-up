# wrap-up

A [Claude Code](https://claude.com/claude-code) skill that closes a working session properly.

Long sessions leave things behind: decisions nobody wrote down, work promised without a ticket,
threads opened and dropped, commits never pushed. `/wrap-up` reads the **full** session transcript
(including parts lost to compaction), compares it with your records, and shows one short,
plain-language list of what is missing. After a single approval it writes everything, and — if the
work continues — gives you a self-contained prompt for the next session.

**List first, one approval, then write.** Nothing is written before you say so.

## Install

Copy the skill folder into your personal skills directory:

```
# macOS / Linux
cp -r skills/wrap-up ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse skills\wrap-up $HOME\.claude\skills\
```

Or put it in a project's `.claude/skills/` to share it with the team. Requires Python 3 for the
transcript dump script.

## Use

Say "wrap up", "close the session", "can I close this?", or type `/wrap-up`.

## Make it yours

The skill is deliberately generic. In section 0 of [SKILL.md](skills/wrap-up/SKILL.md) it asks
where your tasks, decisions, daily log and memory live; tell it once (or write it in your
`CLAUDE.md`) and it uses those targets. Adapt the language rules to your own readers.

## What it does not do

- It does not scan other sessions' transcripts.
- It does not write anything before approval.
- It does not re-list work that is already recorded.
