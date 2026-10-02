# Script Bench: Official Sample Scripts

This directory contains the five official benchmark outputs produced by Script Bench.

All sample files in this directory are **raw, unedited program output** generated directly by the CLI pipeline. No outputs have been manually written, polished, or modified.

---

## Official Benchmarks & Generation Commands

Commands can be executed directly from the project root directory with your `GEMINI_API_KEY` configured in `.env`.

### 01. Personal Finance (30s)
- **File**: `samples/01_personal_finance_30s.json`
- **Niche**: `personal finance`
- **Target Runtime**: `30` seconds (Allowed word budget: 65–77 words)
- **Actual Word Count**: 67 words
- **Topic**: *"Why automating savings is easier than relying on willpower"*
- **Command**:
  ```bash
  python -m src.script_bench.main --niche "personal finance" --topic "Why automating savings is easier than relying on willpower" --target-seconds 30
  ```

---

### 02. Productivity (60s)
- **File**: `samples/02_productivity_60s.json`
- **Niche**: `productivity`
- **Target Runtime**: `60` seconds (Allowed word budget: 130–152 words)
- **Actual Word Count**: 138 words
- **Topic**: *"Why constantly switching between tasks makes a workday feel busy without producing much"*
- **Command**:
  ```bash
  python -m src.script_bench.main --niche "productivity" --topic "Why constantly switching between tasks makes a workday feel busy without producing much" --target-seconds 60
  ```

---

### 03. Technology (45s)
- **File**: `samples/03_technology_45s.json`
- **Niche**: `technology`
- **Target Runtime**: `45` seconds (Allowed word budget: 98–114 words)
- **Actual Word Count**: 106 words
- **Topic**: *"Why developers should understand APIs even when AI coding tools can generate API code"*
- **Command**:
  ```bash
  python -m src.script_bench.main --niche "technology" --topic "Why developers should understand APIs even when AI coding tools can generate API code" --target-seconds 45
  ```

---

### 04. Career (30s)
- **File**: `samples/04_career_30s.json`
- **Niche**: `career`
- **Target Runtime**: `30` seconds (Allowed word budget: 65–77 words)
- **Actual Word Count**: 68 words
- **Topic**: *"Why tailoring a resume to each internship can improve how clearly your experience matches the role"*
- **Command**:
  ```bash
  python -m src.script_bench.main --niche "career" --topic "Why tailoring a resume to each internship can improve how clearly your experience matches the role" --target-seconds 30
  ```

---

### 05. Food (45s)
- **File**: `samples/05_food_45s.json`
- **Niche**: `food`
- **Target Runtime**: `45` seconds (Allowed word budget: 98–114 words)
- **Actual Word Count**: 107 words
- **Topic**: *"Why preheating the pan matters when you want vegetables to brown instead of becoming watery"*
- **Command**:
  ```bash
  python -m src.script_bench.main --niche "food" --topic "Why preheating the pan matters when you want vegetables to brown instead of becoming watery" --target-seconds 45
  ```
