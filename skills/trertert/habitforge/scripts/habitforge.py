#!/usr/bin/env python3
"""
HabitForge Core Script
Simple habit tracking system for Clawdbot.
"""

import json
import os
import sys
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Path to habit data
DATA_DIR = Path("memory/habitforge")
HABITS_FILE = DATA_DIR / "habits.json"

def ensure_data_dir():
    """Ensure data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not HABITS_FILE.exists():
        save_habits({"habits": {}, "last_updated": int(datetime.datetime.now().timestamp() * 1000)})

def load_habits() -> Dict[str, Any]:
    """Load habits from JSON file."""
    try:
        with open(HABITS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"habits": {}, "last_updated": int(datetime.datetime.now().timestamp() * 1000)}

def save_habits(data: Dict[str, Any]):
    """Save habits to JSON file."""
    with open(HABITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def today_str() -> str:
    """Get today's date as YYYY-MM-DD string."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

def create_habit(name: str, frequency: str = "daily") -> Dict[str, Any]:
    """Create a new habit."""
    return {
        "name": name,
        "frequency": frequency,
        "created_at": int(datetime.datetime.now().timestamp() * 1000),
        "current_streak": 0,
        "longest_streak": 0,
        "total_completions": 0,
        "completion_dates": [],
        "active": True
    }

def log_habit(habit_name: str) -> str:
    """Log a habit for today."""
    ensure_data_dir()
    data = load_habits()
    
    today = today_str()
    
    if habit_name not in data["habits"]:
        data["habits"][habit_name] = create_habit(habit_name)
    
    habit = data["habits"][habit_name]
    
    # Check if already logged today
    if today in habit["completion_dates"]:
        return f"Habit '{habit_name}' already logged for today!"
    
    # Add today's completion
    habit["completion_dates"].append(today)
    habit["total_completions"] += 1
    
    # Update streak
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if yesterday in habit["completion_dates"]:
        habit["current_streak"] += 1
    else:
        habit["current_streak"] = 1
    
    # Update longest streak
    if habit["current_streak"] > habit["longest_streak"]:
        habit["longest_streak"] = habit["current_streak"]
    
    data["last_updated"] = int(datetime.datetime.now().timestamp() * 1000)
    save_habits(data)
    
    streak_emoji = "馃敟" if habit["current_streak"] >= 7 else ""
    return f"鉁?{habit_name} logged for today! Current streak: {habit['current_streak']} days {streak_emoji}"

def unlog_habit(habit_name: str) -> str:
    """Remove today's log for a habit."""
    ensure_data_dir()
    data = load_habits()
    
    today = today_str()
    
    if habit_name not in data["habits"]:
        return f"Habit '{habit_name}' not found!"
    
    habit = data["habits"][habit_name]
    
    if today not in habit["completion_dates"]:
        return f"Habit '{habit_name}' wasn't logged today!"
    
    # Remove today's completion
    habit["completion_dates"].remove(today)
    habit["total_completions"] -= 1
    
    # Recalculate streak (simplified - just reset to 0 for now)
    habit["current_streak"] = 0
    
    data["last_updated"] = int(datetime.datetime.now().timestamp() * 1000)
    save_habits(data)
    
    return f"鉂?{habit_name} unlogged for today."

def get_status() -> str:
    """Get today's habit status."""
    ensure_data_dir()
    data = load_habits()
    
    today = today_str()
    output = [f"馃搮 **Today: {datetime.datetime.now().strftime('%b %d, %Y')}**\n"]
    
    active_habits = [h for h in data["habits"].values() if h.get("active", True)]
    
    if not active_habits:
        output.append("No active habits. Use 'track habit [name]' to start!")
        return "\n".join(output)
    
    for habit in active_habits:
        name = habit["name"]
        done = today in habit["completion_dates"]
        streak = habit["current_streak"]
        streak_emoji = "馃敟" if streak >= 7 else ""
        
        if done:
            output.append(f"鉁?{name}: Done {streak_emoji} Streak: {streak}")
        else:
            output.append(f"鉂?{name}: Not done yet")
    
    return "\n".join(output)

def generate_weekly_report() -> str:
    """Generate a weekly progress report."""
    ensure_data_dir()
    data = load_habits()
    
    today = datetime.datetime.now()
    week_start = today - datetime.timedelta(days=today.weekday())
    week_dates = [(week_start + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    
    output = ["馃搳 **HabitForge Weekly Report**", "鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?, ""]
    
    active_habits = [h for h in data["habits"].values() if h.get("active", True)]
    
    if not active_habits:
        output.append("No active habits to report on. Start tracking some habits!")
        return "\n".join(output)
    
    for habit in active_habits:
        name = habit["name"]
        completions = [d for d in habit["completion_dates"] if d in week_dates]
        completion_rate = len(completions)
        streak = habit["current_streak"]
        streak_emoji = "馃敟" if streak >= 7 else ""
        
        output.append(f"**{name}:** {completion_rate}/7 days {'鉁? if completion_rate >= 5 else ''} Current streak: {streak} {streak_emoji}")
    
    # Add some insights
    output.append("")
    output.append("馃挭 **Highlights**: " + ("Keep up the great work!" if any(h["current_streak"] >= 7 for h in active_habits) else "You're making progress!"))
    output.append("馃挕 **Insight**: Consistency is key - try to log habits at the same time each day.")
    output.append("馃幆 **Next week**: Aim for 5+ days on each habit!")
    
    return "\n".join(output)

def list_habits() -> str:
    """List all habits."""
    ensure_data_dir()
    data = load_habits()
    
    if not data["habits"]:
        return "No habits found. Use 'track habit [name]' to start!"
    
    output = ["馃搵 **Your Habits:**", ""]
    
    for name, habit in data["habits"].items():
        status = "Active" if habit.get("active", True) else "Archived"
        output.append(f"- {name}: {status} (Streak: {habit['current_streak']}, Total: {habit['total_completions']})")
    
    return "\n".join(output)

def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python habitforge.py [command] [args...]")
        print("\nCommands:")
        print("  log [habit]          - Log a habit for today")
        print("  unlog [habit]        - Unlog a habit for today")
        print("  status               - Show today's habit status")
        print("  weekly               - Generate weekly report")
        print("  list                 - List all habits")
        print("  help                 - Show this help")
        return
    
    command = sys.argv[1]
    
    if command == "log" and len(sys.argv) >= 3:
        print(log_habit(sys.argv[2]))
    elif command == "unlog" and len(sys.argv) >= 3:
        print(unlog_habit(sys.argv[2]))
    elif command == "status":
        print(get_status())
    elif command == "weekly":
        print(generate_weekly_report())
    elif command == "list":
        print(list_habits())
    elif command == "help":
        print("HabitForge - Intelligent Habit Tracking System")
        print("\nUsage: python habitforge.py [command] [args...]")
        print("\nCommands:")
        print("  log [habit]          - Log a habit for today")
        print("  unlog [habit]        - Unlog a habit for today")
        print("  status               - Show today's habit status")
        print("  weekly               - Generate weekly report")
        print("  list                 - List all habits")
    else:
        print(f"Unknown command: {command}")
        print("Use 'python habitforge.py help' for usage.")

if __name__ == "__main__":
    main()
