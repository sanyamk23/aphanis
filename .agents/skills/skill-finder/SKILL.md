---
name: skill-finder
description: "Search, install, use, and auto-remove a skill on demand. Includes Skill Match (Tinder-style matching), Skill Map (knowledge graph), and Stats Dashboard (gamification). Call this when the user asks to find a skill for a task, or says 'find a skill for X', 'skill match me', 'show skill map', 'skill stats', or similar."
---

# Skill Finder — Just-in-Time Skill Workflow

> 🎭 Match. 🗺 Map. 📊 Stats.

Skill Finder adds **three powerful modes** to your AI agent:

| Mode | What it does | Trigger |
|---|---|---|
| **🔍 Find** (default) | Search → Install → Use → Remove | "Find a skill for X" |
| **🎭 Match** | Tinder-style skill matching | "Skill match me" |
| **🗺 Map** | Visual knowledge graph | "Show skill map for X" |
| **📊 Stats** | Points, levels, achievements | "Skill stats" |

---

## Mode 1: Find (Default)

The classic just-in-time workflow.

### When to use

- "Find a skill for X" / "Is there a skill for X" / "Search skills for X"
- "I need help with X" where X is a specialized task

### Workflow

1. **Search:** `npx skills find <query>`
2. **Pick:** Best match by installs, reputation, alignment
3. **Confirm:** Tell user what was found
4. **Install:** `npx skills add <skill> -y`
5. **Use:** Read SKILL.md, execute task
6. **Remove:** `npx skills remove <skill> -y`

---

## Mode 2: Skill Match (Tinder-Style) 🎭

Gamified skill discovery with compatibility scores.

### When to use

- "Skill match me"
- "Match me a skill"
- "What skill should I use?"
- "Find me something fun"

### Workflow

1. **Search:** Run `npx skills find <query>` to get top 5 matches
2. **Calculate Compatibility** for each skill:

```
compatibility = (install_factor × 40) + (relevance × 35) + (recency × 25)

where:
- install_factor = min(installs / 30000, 1.0)
- relevance = keyword match strength (0.0 to 1.0)
- recency = how recently updated (0.0 to 1.0)
```

3. **Present as cards** (see format below)
4. **User picks** their match
5. **Install → Use → Remove** (standard workflow)

### Output Format

```
🎭 SKILL MATCH ═══════════════════════════════════

  ┌─────────────────────────────────────────────┐
  │  🎯 CARD 1                                  │
  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
  │                                             │
  │  presentation-creator                       │
  │  📊 29K installs • googleworkspace/cli      │
  │  📝 Create Google Slides presentations      │
  │                                             │
  │  🔥 Compatibility: 94%                      │
  │  ████████████████████░░░                    │
  │                                             │
  └─────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────┐
  │  🎯 CARD 2                                  │
  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
  │                                             │
  │  slide-design                               │
  │  📊 8.5K installs • design-co              │
  │  📝 Beautiful slide designs                 │
  │                                             │
  │  🔥 Compatibility: 78%                      │
  │  ██████████████████░░░░░                    │
  │                                             │
  └─────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────┐
  │  🎯 CARD 3                                  │
  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
  │                                             │
  │  pitch-deck                                 │
  │  📊 4.2K installs • startup-tools          │
  │  📝 Startup pitch deck generator            │
  │                                             │
  │  🔥 Compatibility: 71%                      │
  │  ███████████████░░░░░░░░                    │
  │                                             │
  └─────────────────────────────────────────────┘

═══════════════════════════════════════════════════
Reply with 1, 2, or 3 to install that skill!
```

### Match Outcomes

| User picks | Result |
|---|---|
| Card number | Install that skill |
| "None" / "Skip" | Search again with different query |
| "All" | Install top match |
| "Surprise me" | Pick random from top 3 |

---

## Mode 3: Skill Map (Knowledge Graph) 🗺️

Visualize skills as a constellation showing relationships.

### When to use

- "Show skill map for X"
- "Skill map: react"
- "What skills relate to X?"
- "Explore the skill universe"

### Workflow

1. **Find the main skill:** `npx skills find <query>` (top result = center)
2. **Find related skills:** Search for variations (query + "testing", "deploy", "docs", etc.)
3. **Generate constellation diagram** (see format below)
4. **User picks a node** to install
5. **Install → Use → Remove** (standard workflow)

### Output Format

```
🗺 SKILL CONSTELLATION
═══════════════════════════════════════════════════
  Center: presentation (29K installs)

                    ★ presentation
                   / | \
                  /  |  \
        slide-  ←    →   ←  pitch-
       design animations    deck
              |        |
              ↓        ↓
       ui-    ←  transitions  →
      effects

═══════════════════════════════════════════════════
★ = Center skill    ● = Related skill
| = Connection      ← → = Related to each other

Pick a skill to install:
1. presentation (center)
2. slide-design
3. animations
4. pitch-deck
5. transitions
6. ui-effects
```

### Advanced Map (for complex queries)

```
🗺 SKILL UNIVERSE: "react"
═══════════════════════════════════════════════════

                        ★ react
                     /    |    \
           testing ←      →      → styling
              |    \    |    /    |
              ↓     ↓   ↓   ↓     ↓
           jest  vite  css  sass  tailwind
              |     |    |    |
              ↓     ↓    ↓    ↓
           types  hotswap modules  design

═══════════════════════════════════════════════════
Total skills: 12    Categories: 4    Connections: 18
```

---

## Mode 4: Stats Dashboard 📊

Track your skill-finding prowess with points, levels, and achievements.

### When to use

- "Skill stats"
- "My stats"
- "Show dashboard"
- "What level am I?"
- "Achievements"

### Points System

| Action | Points |
|---|---|
| Find a skill | +10 |
| Install a skill | +25 |
| Use a skill successfully | +50 |
| Remove after use (clean) | +15 |
| Discover new category | +100 |
| Perfect Match (90%+ compat) | +30 |
| Share/recommend a skill | +20 |

### Levels

| Level | Points | Title | Icon |
|---|---|---|---|
| 1 | 0–99 | Skill Seedling | 🌱 |
| 2 | 100–299 | Skill Seeker | 🔍 |
| 3 | 300–599 | Skill Hunter | ⚡ |
| 4 | 600–999 | Skill Master | 🎯 |
| 5 | 1000–1999 | Skill Ninja | 🏆 |
| 6 | 2000+ | Skill Legend | 👑 |

### Achievements

| Achievement | Icon | How to unlock |
|---|---|---|
| First Find | 🔍 | Found your first skill |
| Clean Freak | 🧹 | Removed 5 skills in one session |
| Perfect Match | 🎯 | 90%+ compatibility on first try |
| Collector | 📚 | Used 10+ different skills |
| Speed Demon | ⏱️ | Found + used in under 60 seconds |
| Night Owl | 🌙 | Used skills past midnight |
| Streak Master | 🔥 | 3+ days of skill usage |
| Explorer | 🧭 | Discovered 5+ categories |
| Social Butterfly | 🦋 | Shared 3+ skills |
| Legendary | 👑 | Reached Level 6 |

### Output Format

```
📊 SKILL DASHBOARD
═══════════════════════════════════════════════════

  👤 User: sanyamk23
  ⚡ Level: 3 — Skill Hunter
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ███████████████░░░░░░░░░░░░░░░░░░░░░  340/600

  🏅 Achievements: 3/10
  ┌─────────────────────────────────────────────┐
  │ ✅ First Find    │ ✅ Clean Freak │ 🔒 ... │
  └─────────────────────────────────────────────┘

  📈 Session Stats:
  • Skills found: 12
  • Skills used: 8
  • Skills removed: 8
  • Clean score: 100% 🌟

  🔥 Current streak: 3 days
═══════════════════════════════════════════════════
```

---

## Command Reference

### Trigger Phrases

| Mode | Phrases |
|---|---|
| Find | "Find a skill for X", "Is there a skill for X", "Search skills for X" |
| Match | "Skill match me", "Match me a skill", "What skill should I use?" |
| Map | "Show skill map for X", "Skill map: react", "Explore skills for X" |
| Stats | "Skill stats", "My stats", "Dashboard", "What level am I?" |

### Quick Commands

```
"Find a skill for presentations"     → Mode: Find
"Skill match me for testing"         → Mode: Match
"Show skill map for react"           → Mode: Map
"Skill stats"                        → Mode: Stats
```

---

## Edge cases

- **No skills found:** Tell the user and offer to do it with base capabilities
- **Install fails:** Report the error; don't retry blindly
- **Skill already installed:** Skip install, use directly, still remove after
- **User says "keep it":** Skip the remove step
- **Multiple modes match:** Ask user which mode they want
- **Empty query:** Ask what they're looking for

---

## Important notes

- Skills run with **full agent permissions** — review before use
- Always clean up unless the user asks to keep it
- If the task spans multiple turns, keep installed until done
- Stats are approximate and session-based (for fun, not precision)
- Compatibility scores are estimates — your mileage may vary
