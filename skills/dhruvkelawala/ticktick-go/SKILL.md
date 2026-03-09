---
name: ticktick-go
version: 1.0.1
description: "Manage TickTick tasks and projects via the `ttg` CLI (github.com/dhruvkelawala/ticktick-go). Use when: adding tasks, listing tasks, marking complete, editing tasks, managing projects, or filtering by due date or priority. Requires ttg to be installed and authenticated."
metadata:
  openclaw:
    requires:
      bins:
        - ttg
    install:
      - id: ttg
        kind: shell
        label: "Build and install ttg CLI from source"
        script: "git clone https://github.com/dhruvkelawala/ticktick-go /tmp/ttg-install && cd /tmp/ttg-install && make install && rm -rf /tmp/ttg-install"
---

# TickTick CLI Skill (`ttg`)

A terminal interface for [TickTick](https://ticktick.com) via the [`ticktick-go` CLI](https://github.com/dhruvkelawala/ticktick-go).

## Prerequisites

Install `ttg`:
```bash
git clone https://github.com/dhruvkelawala/ticktick-go
cd ticktick-go && make install
```

Create `~/.config/ttg/config.json` with your TickTick API credentials (get them at [developer.ticktick.com](https://developer.ticktick.com/manage)):
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "timezone": "America/New_York"
}
```

Authenticate:
```bash
ttg auth login      # opens browser OAuth2 flow
ttg auth status     # confirm you're logged in
```

## Task Commands

```bash
# List
ttg task list                              # Inbox (default)
ttg task list --all                        # Every task
ttg task list --project "Work"             # By project name
ttg task list --due today                  # Due today
ttg task list --due tomorrow               # Due tomorrow
ttg task list --priority high              # By priority
ttg task list --json                       # JSON output for scripting

# Add
ttg task add "Buy milk"
ttg task add "Review PR" --project "Work" --priority high --due "tomorrow 9am"

# Manage
ttg task get <id>                          # Full details
ttg task done <id>                         # Mark complete
ttg task delete <id>                       # Delete
ttg task edit <id> --title "Updated title" --priority medium --due "next monday"
```

## Project Commands

```bash
ttg project list                           # All projects
ttg project get <id>                       # Project details
ttg project create "Side Projects"         # Create new project
```

## Due Date Formats

| Input | Result |
|-------|--------|
| `today`, `tomorrow` | Midnight of that day |
| `next monday` | Following Monday |
| `3pm`, `tomorrow 3pm` | Specific time |
| `in 2 days`, `in 3 hours` | Relative offset |
| `2026-03-20` | ISO date |
| `2026-03-20T15:00:00` | ISO datetime |

## Priority Values

`none` (default) · `low` · `medium` · `high`

## JSON / Scripting

Every command accepts `--json` / `-j`:

```bash
# Get all high-priority tasks as JSON
ttg task list --priority high --json

# Pipe into jq
ttg task list --all --json | jq '.[] | select(.dueDate != null) | .title'
```

## Common Patterns

```bash
# Morning review — what's due today?
ttg task list --due today

# Quick capture while in flow
ttg task add "Follow up with Alex" --due "tomorrow 10am" --priority medium

# End-of-day — mark things done
ttg task list --json | jq '.[].id'   # get IDs
ttg task done <id>

# Weekly planning — see everything
ttg task list --all
```
