# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

C:\Srihan\projects\ai110-module2show-pawpal-starter>python main.py
Today's Schedule:
- Mittens:
    - Feed Cat
- Fido:
    - Feed Dog
    - Morning Walk


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```
These tests verify whether or not high-priority tasks are scheduled first, the total time doesn't go over to what the owner can handle, cache invalidation after task changes and any unclear tasks get clear explanations.
Confidence Level is 5 stars because all my tests have passed.


Sample test output:

```
# Paste your pytest output here

C:\Srihan\projects\ai110-module2show-pawpal-starter>python -m pytest
==================================================== test session starts =====================================================
platform win32 -- Python 3.12.6, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Srihan\projects\ai110-module2show-pawpal-starter
plugins: anyio-4.12.1
collected 7 items                                                                                                             

tests\test_pawpal.py .......                                                                                            [100%]

===================================================== 7 passed in 0.08s ======================================================

## 📐 Smarter Scheduling

The PawPals+ app now has high priority scheduling where high prior tasks gets scheduled first, gap-filling algorithms where large tasks are done before small tasks and describes the day by day routine like morning exercises for the pet. There is also pet clustering which groups different kind of pets in one area for more efficient care.

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
Connect your logic to the Streamlit UI in app.py.
Refine UML so it matches what you actually built.


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

http://localhost:8501/