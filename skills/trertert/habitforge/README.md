# HabitForge - Quick Start Guide

## Installation

1. Copy the `habitforge` folder to your Clawdbot workspace skills directory
2. Add the following to your `HEARTBEAT.md`:

```markdown
## HabitForge Daily Check
- Ask user if they've logged today's habits if not already logged
- Generate weekly report every Sunday automatically
- Log results to memory/habitforge/
```

## Basic Usage

### Create a new habit
```
track habit meditation daily
```

### Log a habit
```
I did my meditation
```

### Check today's status
```
habit status
```

### Generate weekly report
```
weekly report
```

### List all habits
```
list habits
```

## Data Storage

All data is stored in `memory/habitforge/habits.json` in your Clawdbot workspace.

## Features

- 鉁?Natural language tracking
- 馃敟 Streak tracking
- 馃搳 Weekly progress reports
- 馃挕 Pattern insights
- 馃摑 Export to markdown

## License

MIT License - Use freely for personal or commercial purposes.
