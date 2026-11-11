---
name: plan-council
description: Builds a development / feature plan by running it through a council of 5 advisors with opposing lenses (Architect, Minimalist, Skeptic, Tester, Maintainer), then a chairman who synthesises one executable plan saved to plans/. Light mode by default (cheap); full mode with anonymous peer review only on explicit request. Use when the user asks for a plan, a design, a breakdown or an approach for a non-trivial feature or change ("fais-moi un plan", "planifie cette feature", "council ce plan", "comment tu l'implémenterais"), even if they don't say "council". Not for trivial changes with an obvious approach.
argument-hint: "<feature description | ticket/issue URL | file> [--full]"
allowed-tools: Bash(git rev-parse:*), Bash(git log:*), Bash(git branch:*), Bash(date:*), Glob
---

# Plan council

Turns a feature request into one decisive, executable plan by confronting five
opposing lenses, then arbitrating. Adapted from the LLM Council idea (Karpathy),
with sub-agents using different thinking lenses, grounded in the codebase.

The plan (and every question asked to the user) is in **French**. Code,
identifiers and paths stay in their original language.

## Arguments (optional)

Received content: `$ARGUMENTS`

| Argument | Meaning |
|---|---|
| free text, a ticket / issue URL or a file path | The feature to plan. A URL or file is read to extract the request. |
| `--full` | **Full mode**: adds the anonymous peer-review round. |
| nothing | Ask what to plan. |

## Modes

| | Light (**default**) | Full |
|---|---|---|
| Triggered by | everything else | `--full`, or the user explicitly asks for « mode complet », « avec peer review », « council complet » |
| Scout (`dev:plan-scout`, Haiku) | 1 | 1 |
| Advisors (`dev:plan-advisor`, Sonnet) | 5, read budget **0–2 files** | 5, read budget **0–3 files** |
| Peer review (`dev:plan-reviewer`, Sonnet) | no | 5, anonymous |
| Chairman (`dev:plan-chairman`, Opus) | 1 | 1 |
| Sub-agents | 7 | 12 |

**Never switch to full mode on your own.** If the feature looks risky or
ambiguous, you may *suggest* full mode in one line at the end, and stop there.

The model of each role is set in the frontmatter of its agent file in
`plugins/dev/agents/`; don't override it when spawning.

## Hard rules

- **Planning only.** Never implement, never modify project code, never run
  project code (tests, builds, scripts). The only file written is the plan,
  and it is written by the chairman.
- **Economy of tokens is a feature.** Only the scout explores the repo broadly.
  Advisors and the chairman work from the context pack and read at most the
  budget they are given. Don't read the code yourself before the scout has
  run, and don't re-read what the pack already contains.
- Spawn agents with the `dev:` prefix (`dev:plan-scout`, `dev:plan-advisor`,
  `dev:plan-reviewer`, `dev:plan-chairman`).
- **Parallel where independent**: the 5 advisors go in **one single message**
  (5 calls), and so do the 5 reviewers.
- Pass the framing, the pack and the outputs **verbatim** between agents. Don't
  summarise or "improve" them: you are a relay, not a participant.
- Never invent a file, a line or a symbol. Unknowns go to "Questions ouvertes".
- No mention of Claude inside the plan file.

## Steps

### 1. Gate: is a council worth it?

Don't convene for trivial work. Skip it and say so in one line (offer a short
direct plan instead) when the change is obviously small: a single file, a
clear approach, no design choice, a pure rename or typo, a question with one
right answer. Convene when there is a real design choice, several files or
layers, a data / API contract, a migration, or genuine uncertainty about the
approach.

### 2. Frame

Rewrite the request neutrally, **without adding your own opinion**:

```
Objectif : <what must exist when done>
Contexte : <why, who uses it, what triggers it>
Contraintes : <stack, deadlines, compatibility, things stated by the user>
Enjeux : <what a wrong call costs>
Critères de réussite connus : <if any>
```

If a ticket URL or file was given, read it to fill this in. If a **blocking**
ambiguity remains that the code cannot answer (the goal itself is unclear, two
very different readings), ask the user **at most 3 short questions** and wait.
Don't ask what the scout can find out.

Detect the mode now (see table) and compute, with a single command:
`git rev-parse --show-toplevel`, `git rev-parse --short HEAD`, `date +%F`.
If not in a git repository, use the current directory and omit the base sha.

### 3. Scout the code (once)

Spawn **one** `dev:plan-scout` with the framing (plus any path hints from the
user). It returns the **context pack** (about 1200 words max). Keep it
unchanged. If the pack says the repository is empty or unrelated to the
feature, say so and continue with a greenfield framing.

### 4. Convene the advisors

Read `references/advisors.md` once. Spawn the **5** `dev:plan-advisor` agents
**in parallel, in one message**. Each prompt contains, in this order:

1. its lens block, copied unchanged from `references/advisors.md`,
2. the framing,
3. the context pack,
4. the read budget: `0 à 2 fichiers` (light) or `0 à 3 fichiers` (full).

Collect the five opinions. If one agent fails, retry it once; if it fails
again, continue with four and say so in the final message.

### 5. Peer review (full mode only)

1. Label the five opinions **A–E** in a **random order** (not the order of the
   lens list), strip the lens names, and keep the letter ↔ lens mapping aside.
2. Spawn **5** `dev:plan-reviewer` agents **in parallel**, each receiving the
   framing and the five anonymised opinions.

Skip this step entirely in light mode.

### 6. Chairman

Choose the plan path:

- Folder: `plans/` at the repository root (created by the chairman if missing).
- File: `<YYYY-MM-DD>-<slug>.md`, slug = short title, lowercase, ASCII, words
  separated by `-`, 60 characters max.
- Check with `Glob` that the file does not exist; otherwise append `-2`, `-3`…
  Never overwrite.

Spawn **one** `dev:plan-chairman` with: the framing, the context pack, the five
opinions **with lens names**, in full mode the five reviews and the letter
mapping, plus the output path, the mode (`léger` / `complet`), the date and the
base sha. It writes the plan file and returns a short summary.

### 7. Report

Print to the user, in French:

```markdown
## Plan — <feature> (mode <léger|complet>)

<the chairman's summary: approach, number of steps, main risk>

📄 `plans/<file>.md`

### Questions ouvertes
<verbatim from the chairman>
```

Then, in one line each:
- the plan was not committed, and `plans/` may be worth ignoring in git if it
  isn't (check with `git check-ignore plans` first, stay silent if ignored);
- in light mode only, if the feature is risky or ambiguous: suggest relaunching
  with `--full`. Don't relaunch by yourself.
- if an advisor was missing, say it.

Don't paste the whole plan in the terminal: the file is the deliverable.

### 8. Follow-up (only if the user asks)

The skill ends at step 7. If the user answers the open questions, update the
plan file (small edits; no new council). If they ask to implement, that is a
separate task: start from the plan file, step by step.
