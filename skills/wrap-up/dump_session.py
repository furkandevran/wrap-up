# Dump one session's full transcript (including compacted parts) as readable text.
# Usage:
#   python dump_session.py <session-id | first 8 chars of the id> <output.txt>
#   python dump_session.py --find "<a distinctive phrase from this session>" <output.txt>
# Output: user messages in full, assistant messages shortened; file writes (✎) and
# git/gh commands (⚙) on separate lines. Tool results and sub-agent transcripts are skipped.
import json, glob, os, sys, datetime

root = os.path.expanduser("~/.claude/projects/")
args = sys.argv[1:]
if len(args) < 2:
    sys.exit('usage: dump_session.py <id> <output>  |  dump_session.py --find <phrase> <output>')

if args[0] == "--find":
    phrase, output = args[1], args[2]
    today = datetime.date.today()
    candidates = []
    for p in glob.glob(root + "*/*.jsonl"):
        if datetime.date.fromtimestamp(os.path.getmtime(p)) < today - datetime.timedelta(days=2):
            continue
        with open(p, encoding="utf-8", errors="replace") as f:
            if phrase in f.read():
                candidates.append(p)
    if len(candidates) != 1:
        sys.exit(f"{len(candidates)} sessions matched, narrow the phrase: "
                 + ", ".join(os.path.basename(c)[:8] for c in candidates))
    path = candidates[0]
else:
    session_id, output = args[0], args[1]
    matches = glob.glob(root + f"*/{session_id}*.jsonl")
    if len(matches) != 1:
        sys.exit(f"{len(matches)} files matched: {session_id}")
    path = matches[0]

lines = []
for raw in open(path, encoding="utf-8", errors="replace"):
    try:
        o = json.loads(raw)
    except Exception:
        continue
    if o.get("isSidechain") or o.get("type") not in ("user", "assistant"):
        continue
    ts = o.get("timestamp", "")[5:16].replace("T", " ")
    c = (o.get("message") or {}).get("content")
    blocks = [{"type": "text", "text": c}] if isinstance(c, str) else (c or [])
    for b in blocks:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "text":
            txt = (b.get("text") or "").strip()
            if not txt or txt.startswith("<") or "Base directory" in txt[:60]:
                continue
            if txt.startswith("This session is being continued"):
                lines.append(f"[{ts}] --- session compacted here ---")
                continue
            if o["type"] == "user":
                lines.append(f"[{ts}] USER: {txt[:2000]}")
            else:
                lines.append(f"[{ts}] claude: {txt.replace(chr(10), ' ')[:900]}")
        elif b.get("type") == "tool_use":
            name, inp = b.get("name"), b.get("input") or {}
            if name in ("Edit", "Write", "NotebookEdit"):
                lines.append(f"[{ts}]   ✎ {inp.get('file_path', '')}")
            elif name in ("Bash", "PowerShell"):
                cmd = inp.get("command", "")
                if any(k in cmd for k in ("git commit", "git push", "gh issue", "gh pr")):
                    lines.append(f"[{ts}]   ⚙ {cmd.replace(chr(10), ' ')[:200]}")

with open(output, "w", encoding="utf-8") as f:
    f.write(f"session {os.path.basename(path)[:8]} — {path}\n\n" + "\n".join(lines))
print(len(lines), "lines ->", output)
