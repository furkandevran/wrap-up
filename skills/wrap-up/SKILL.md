---
name: wrap-up
description: End-of-session close-out. Reads the full session transcript (including compacted parts), finds decisions nobody wrote down, tasks promised but never filed, abandoned threads, memory candidates and unpushed commits; presents them as one short list, writes everything after a single approval, and hands over a prompt for the next session if work continues. Use when the user says "wrap up", "close the session", "can I close this?", "let's stop here", or similar.
---

# /wrap-up — empty the session into your records before you close it

A long session leaves things behind: decisions that never reached the task tracker, work
someone said "let's do" without a ticket, a thread opened and forgotten, a commit never pushed.
When the session closes, they are gone. This skill has one job: **get what is still only in the
session into the places where it will be found.**

Rule: **list first, then one approval, then write.** Nothing is written before the user approves.

## 0. Configure once: where does each kind of thing live?

Before the first run, make sure the project's `CLAUDE.md` / `AGENTS.md` (or this section) names
the user's real targets. If it does not, ask once and offer to save the answer there.

| Kind | Typical target |
|---|---|
| Tasks / to-do | issue tracker, `TODO.md`, task files |
| Decisions | decision log, ADR folder, the task the decision belongs to |
| Daily log | a journal or changelog file |
| Memory | the assistant's memory folder / `CLAUDE.md` |
| Hygiene | every repo the session touched: `git status -sb`, unpushed commits, stray branches |

Respect each repo's own rules for commits and pushes (identity, branch, whether to push at all).
Do not move private information into a shared place; if a rule says a kind of data stays local,
it stays local.

## 1. Read the full transcript — do not trust the summary

If the session was compacted, the summary in context has already lost threads. Dump the real
transcript:

```
python <skill-dir>/dump_session.py <session-id> <scratchpad>/session.txt
```

- **Session id:** the last folder name of the scratchpad path in the system prompt (the
  `xxxxxxxx-xxxx-…` before `\scratchpad`). If you cannot find it, search by a distinctive
  sentence: `--find "<a phrase from this session>"`.
- Output: user messages in full, assistant messages shortened, `✎` for files written,
  `⚙` for git/gh commands, `--- session compacted here ---` markers.
- Read a large dump in parts. Timestamps are UTC.
- If the session ran for days, scan only **after the last wrap-up**.

## 2. Extract

Pull five kinds of item from the transcript. One line each, with the time as its source.

| Kind | What to look for |
|---|---|
| **decision** | "let's do it this way", "X, not Y", a change of scope/deadline/owner, any correction by the user |
| **task** | "let's do it", "we'll look at that later", "add this too" — a promise without a ticket |
| **thread** | A topic opened and left unfinished; an unanswered question (the user's or yours) |
| **memory** | A lasting working preference ("from now on…", "always…", a repeated objection) |
| **pending approval** | Something you asked the user to decide and they never answered (a live write, a send, a merge) |

Technical intermediate steps, work already recorded, and one-off questions are not items.

## 3. Compare with the records

Search for each item in the records. Not found = **missing**. Found but stale = **outdated record**.
Then check hygiene: in every repo touched, `git status -sb` for uncommitted files, unpushed commits
and open branches.

## 4. One list, in plain language

Count already-recorded items as a number only ("14 items already recorded ✓"). List only what is
missing. **Write for a reader who did not see the session** — the list must stand on its own, and
the user should not have to work out "what will you do, where, and why does it matter".

### Language rules (more important than the list itself)

- **No jargon.** No "hygiene", "thread", "record target". Say "work left hanging", "a decision
  nobody wrote down", "changes that were never pushed".
- **Every item has three parts:** what is there (1 sentence) → what you will do (which file/task
  gets what) → why (what happens if it is not written). Three lines at most per item.
- **A task id never stands alone.** Give the task title and a link to it.
- **Questions for the user first, then what you will do on your own.** Items that need an answer
  go first under "Your decision needed"; the rest under "I will write".
- **State your recommendation and the default:** "My suggestion: X. If you say nothing, I do X."
- **Spell out numbers and abbreviations.** Use "order", "refund", "backup", not internal codes,
  unless the code is genuinely needed — and say what it is.
- **Do not leak restricted data into the list.** Amounts, names and other data that must not
  leave its home are not written in the summary either; say "N orders".
- **A short summary on top:** "What happened in this session" in 2–3 sentences, then one line:
  "Nothing written yet — waiting for your approval."

### Format

```
## Wrap-up — <topic of the session>

**What happened:** <2–3 sentences>. **Nothing has been written yet**; I will write the items
below once you approve.

**Your decision needed**
1. <One-sentence question.> My suggestion: <…>. (If you say nothing, I do this.)

**I will write** (if you approve)
2. <What is there.> → <What goes where.> If not written: <consequence>.
3. ...

**Later (not in this session, handed to the next one):** <1–3 items>.

Reply: **"ok"** does everything · **"all except 2"** skips an item · or write a correction.
```

- Propose the target yourself: an existing task gets a note; otherwise a new task (suggest an owner
  and a date).
- A topic that was dropped on purpose does not become a task; ask "drop it?" with "drop" as the
  suggestion.
- If the list is empty: "Everything is recorded." plus the hand-over prompt if needed. Nothing more.

## 5. After approval — write everything

When the user says "ok" (or sends corrections), proceed without asking again:

1. Task files and the to-do list **in the same operation**; commit and push per the repo's rules.
2. Memory files and the memory index.
3. Today's block in the daily log: what was done, what is unfinished.
4. Hygiene: commit/push each repo by its own rules (never touch a protected branch the rules
   forbid).
5. Give a link to every task opened or updated.

Say each step in one short sentence as you go; no silent batch operations.

**When finished**, give one plain report: **Done** (one line per item: what was written where, with
the task link) · **Could not do** (if any: what, and what the user can do) · **Left for you**
(things only the user can do, such as a bank action or a merge).

## 6. Hand-over prompt — if work continues

If the topic is not finished, after writing, give a prompt for the next session in a code block:

- **Read first:** the task file, the rule files, the source documents (with paths)
- **Current state:** short bullets, measured results
- **Pending approvals:** say explicitly "no approval given — do not act without asking"
- **Order:** numbered steps
- **Rules:** only those that matter for this topic (live writes, personal data, which repo)
- **First step:** one sentence

The prompt must stand alone: the new session cannot see this one.

Then one line: **"You can close the session."**

## Do not

- Write before approval — including the daily-log line.
- List items that are already recorded; the user is here to read what is missing.
- Pressure the user to approve a pending item during wrap-up. It stays in the list and in the
  hand-over prompt.
- Scan other sessions' transcripts.
- Write an unclear list and ask for approval. If the user says "I did not understand what you did",
  the list failed: rewrite it by the language rules above, and write nothing while asking again.
