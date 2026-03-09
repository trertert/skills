---
name: habitforge
version: 1.0.0
description: "Intelligent habit tracking system for Clawdbot. Track daily habits with natural language, get weekly progress reports, streaks, and visual summaries. Build better habits with AI assistance."
tags: [habit-tracking, productivity, self-improvement, statistics, wellness, daily-routine]
author: trertert
homepage: ""
metadata:
  author: trertert
  version: "1.0.0"
  clawdbot:
    emoji: 馃敟
    requires:
      bins: []
      env: []
    tags: ["habit-tracking", "productivity", "self-improvement", "statistics", "wellness"]
compatibility: "Works with all Clawdbot installations. No external dependencies required."
---

# 馃敟 HabitForge 鈥?Intelligent Habit Tracking System

> *"We are what we repeatedly do. Excellence, then, is not an act, but a habit."*
> 鈥?Will Durant

Turn your Clawdbot into a personal habit coach. Track daily habits with natural language, maintain streaks, get weekly progress reports, and build lasting positive habits.

## Why HabitForge?

Most habit trackers are just apps 鈥?this is an **AI-powered habit coach** that lives with you in your assistant. It:

- Understands natural language ("I went for a run today" 鈫?auto-tracks exercise)
- Maintains streak history and celebrates progress
- Generates weekly progress summaries with actionable insights
- Reminds you to log habits if you forget
- Helps you identify patterns and improve consistency
- Exports data to markdown for your notes

---

## Key Features

### 1. Natural Language Tracking

No buttons to press 鈥?just tell Clawdbot what you did:
```
User: "I did my meditation this morning"
HabitForge: 鉁?Meditation logged for today! Current streak: 12 days 馃敟
```

Works with any habit you want to track: exercise, reading, meditation, water intake, coding, journaling...

### 2. Streak System

Track consecutive days:
- Auto-increments streaks when you log
- Resets on missed days (but gives encouragement!)
- Highlights your longest streaks for motivation

### 3. Weekly Progress Reports

Every Sunday (or on demand), get a beautiful summary:

```
馃搳 **HabitForge Weekly Report**
鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?
馃弮 Exercise:     5/7 days 鉁? Current streak: 3
馃 Meditation:   7/7 days 鉁? Current streak: 21 馃敟
馃摉 Reading:      4/7 days    Current streak: 4

馃挭 **Highlights**: You hit a new personal best on meditation!
馃挕 **Insight**: You're more consistent with exercise on weekdays.
馃幆 **Next week**: Focus on improving reading consistency.
```

### 4. Habit Management

- Add new habits with custom goals
- Archive habits you've mastered
- Delete habits you don't track anymore
- Rename or reconfigure anytime

### 5. Statistics & Patterns

See your progress over time:
- Monthly completion rates
- Most consistent days of the week
- Habit interaction patterns
- Progress towards long-term goals

---

## Usage

### Getting Started

Add this to your `HEARTBEAT.md` for daily checks:
```markdown
## HabitForge Daily Check
- Ask user if they've logged today's habits if not already logged
- Generate weekly report every Sunday automatically
- Log results to memory/habitforge/
```

### Common Commands

| What you say | What it does |
|---|---|
| `track habit meditation daily` | Creates a new daily habit called "meditation" |
| `I did my meditation` | Logs meditation for today |
| `undo meditation today` | Unlogs meditation for today |
| `habit status` | Shows current streaks and today's completion |
| `weekly report` | Generates weekly progress report |
| `monthly stats` | Shows monthly statistics |
| `list habits` | Lists all active habits |
| `archive meditation` | Archives the meditation habit |
| `delete meditation` | Deletes the meditation habit completely |

### Example Workflow

```
> track habit 30min-walk daily
鉁?New habit created: 30min-walk (daily)

> I did my 30min walk
鉁?30min-walk logged for today! Current streak: 1

> habit status
馃搮 Today: Mar 9, 2026

馃弮 30min-walk: 鉁?Done 馃敟 Streak: 1
馃 meditation: 鉂?Not done yet

> weekly report
[generates beautiful weekly report...]
```

---

## Data Storage

All habit data is stored locally in your Clawdbot workspace at:
```
memory/habitforge/habits.json
```

This keeps your data private and under your control. No cloud sync required unless you want it.

Example data structure:
```json
{
  "habits": {
    "meditation": {
      "name": "meditation",
      "frequency": "daily",
      "created_at": 1709000000000,
      "current_streak": 21,
      "longest_streak": 21,
      "total_completions": 145,
      "completion_dates": ["2026-03-01", "2026-03-02", ...],
      "active": true
    }
  },
  "last_updated": 1710000000000
}
```

---

## Integration with Clawdbot Features

### Heartbeat Integration

Perfect for daily check-ins. Example `HEARTBEAT.md` entry:
```markdown
## HabitForge Check (every 2nd heartbeat)
- Check if any daily habits are still unlogged for today
- Gently remind user to log them
- If Sunday and no report generated today, generate weekly report
```

### Cron Integration

Schedule automatic weekly reports:
```json
{
  "name": "HabitForge Weekly Report",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 0",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Generate your weekly HabitForge progress report."
  },
  "sessionTarget": "main",
  "enabled": true
}
```

### Memory Integration

HabitForge automatically adds key insights to your daily memory files when generating reports.

---

## Best Practices

1. **Start small** 鈥?2-3 habits max when beginning
2. **Be consistent** 鈥?log at the same time every day (e.g., after breakfast)
3. **Be honest** 鈥?it's okay to miss a day, just get back on track tomorrow
4. **Review weekly** 鈥?the weekly report helps you stay accountable
5. **Celebrate wins** 鈥?HabitForge will celebrate streaks with you!

---

## Tips for Success

- **Habit stacking**: "I meditate after I brush my teeth in the morning"
- **Implementation intention**: "When situation X occurs, I will do habit Y"
- **Accountability**: Share your weekly reports with a friend if you need extra motivation
- **Flexibility**: Life happens 鈥?if you miss a day, just get back on track the next day

---

## Roadmap (Future Features)

- [ ] Visual charts and graphs (requires Python matplotlib)
- [ ] Goal setting (e.g., "run 20km this month")
- [ ] Habit correlation analysis (does meditation help you sleep better?)
- [ ] Reminder notifications
- [ ] Export to CSV/JSON for backup

---

## Contributing

Found a bug or have an idea for improvement? Feel free to submit an issue or PR on GitHub.

---

## License

MIT License 鈥?feel free to use this skill for personal or commercial purposes.

---

*"The chains of habit are generally too light to be felt until they are too strong to be broken."*
鈥?Samuel Johnson

馃敟 Happy habit building!
