# rtk-compress

**Save 60-90% of LLM tokens on shell commands, file reads, and test output.**

This skill wraps [rtk (Rust Token Killer)](https://github.com/rtk-ai/rtk) — a CLI proxy that filters and compresses command outputs before they reach your LLM context.

## Install

```bash
# 1. Install rtk
brew install rtk          # macOS
# or: curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh

# 2. Verify
rtk gain  # Should show token savings stats
```

Then copy this `SKILL.md` to your agent's skills directory.

## Rules for the Agent

Use `rtk <command>` instead of bare commands whenever possible:

### Always use rtk for:
- `rtk git status` / `rtk git log` / `rtk git diff`
- `rtk ls -la` / `rtk cat <file>`
- `rtk npm test` / `rtk pytest` / `rtk cargo test`
- `rtk npm run build` / `rtk ruff check`

### Don't use rtk for:
- Commands whose output is piped to other tools (e.g., `git log | grep ...`)
- Scripts that parse raw output
- Commands where you need the exact full output

### If rtk fails:
Fall back to the bare command. Never block a task because of compression.

### Check savings:
```bash
rtk gain           # current session
rtk gain --global  # all-time stats
```

## Token Savings Reference

| Operation | Without rtk | With rtk | Savings |
|-----------|------------|----------|---------|
| `git status` | ~300 | ~60 | -80% |
| `git log -20` | ~2,000 | ~400 | -80% |
| `cat file.ts` | ~2,000 | ~600 | -70% |
| `npm test` | ~5,000 | ~500 | -90% |
| `pytest` | ~2,000 | ~200 | -90% |
| **Typical session** | **~150k** | **~45k** | **-70%** |

## Links

- rtk: https://github.com/rtk-ai/rtk
- OpenClaw feature request: https://github.com/openclaw/openclaw/issues/35053
