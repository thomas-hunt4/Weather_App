# Week 11 Reflection

## Student Information
- **Name:**  Thomas Hunt
- **GitHub Username:** thomas-hunt4
- **Preferred Feature Track:** Data / Visual / Smart
- **Team Interest:** Yes Project Owner or Contributor

## Section 1: Week 11 Reflection
Answer each prompt with 3–5 bullet points:

### Key Takeaways
What did you learn about capstone goals and expectations?
- Weekly milestones to help keep up wity Capstone
- Core app expections
- Feature optioins to choose from  

### Concept Connections
Which Week 1–10 skills feel strongest? Which need more practice?
- general understanding **strongest**
- working with data structures **weakest**
- basic algorithms **weakest**


### Early Challenges
Any blockers (e.g., API keys, folder setup)?
- Slowing down and planning correctly


### Support Strategies
Which office hours or resources can help you move forward?
- Office Hours
- Peers for questions/debug


## Section 2: Feature Selection Rationale
List three features + one enhancement you plan to build.

| # | Feature Name | Difficulty (1–3) | Why You Chose It / Learning Goal |
|---|--------------|------------------|----------------------------------|
| 1 | Temp graphs             |        2          |             practice viz and working with data                     |
| 2 |  Theme Switcher            |       2           |  I like dark mode on everything                                |
| 3 |  Weather Alerts            |        2          |           work with API's                       |
| Enhancement | undecided  |        n/a          |             n/a                     |

**Tip:** Pick at least one "level 3" feature to stretch your skills!

## Section 3: High-Level Architecture Sketch
Add a diagram or a brief outline that shows:
- Core modules and folders
- Feature modules
- Data flow between components

```
WEATHER-PROJECT/
├── data/                        # Handles data storage and access
│   ├── data.py                 # Data loading and processing functions
│   ├── open_weather_*.txt      # API or forecast data
│   └── weather_history.txt     # Historical weather records
│
├── docs/                       # Project documentation
│   ├── LICENSE
│   └── Week11_Reflection.md
│
├── features/                   # Feature engineering modules
│   ├── __init__.py
│
├── gui/                        # GUI interfaces
│   ├── __init__.py
│   ├── gui_main.py             # Main GUI implementation
│   └── v2gui_main.py           # Alternative/new GUI version
│
├── screenshots/                # UI screenshots (for docs)
│
├── tests/                      # Unit tests for modules
│   ├── __init__.py
│   └── features_test.py        # Tests for feature logic
│
├── .env                        # Environment variables (e.g., API keys)
├── .gitignore
├── 10637-2024.csv              # External CSV data (likely weather)
├── config.py                   # Global configuration/settings
├── main.py                     # Entry point, ties data + features + GUI
├── README.md
└── requirements.txt            # Python dependencies


graph TD
    A[data.py] -->|loads| B[main.py]
    A -->|reads| C[weather_history.txt]
    A -->|reads| D[open_weather_*.txt]

    B --> E[features/]
    B --> F[gui/gui_main.py]
    B --> G[config.py]

    E -->|feature data| F
    F -->|displays| H[User GUI]

    subgraph Tests
        I[features_test.py] --> E
    end
[Add your architecture diagram or outline here]
```

## Section 4: Data Model Plan
Fill in your planned data files or tables:  
I have not made decisions on this yet beyond the core requirements. 
Depending on where I get on the project this week I will decide if to introduce some larger relational db for some more advanced modeling. I want to make sure I have my core complete and half my features before commiting to something advanced. I will be using json for weather imports and API data dumps and then need to do some more research on putting those to csv or PostGres as an alternative. 

| File/Table Name | Format (txt, json, csv, other) | Example Row |
|-----------------|--------------------------------|-------------|
| `weather_history.txt` | txt | 2025-06-09,New Brunswick,78,Sunny |
|                 |                                |             |
|                 |                                |             |
|                 |                                |             |

## Section 5: Personal Project Timeline (Weeks 12–17)
Customize based on your availability:

| Week | Monday | Tuesday | Wednesday | Thursday | Key Milestone |
|------|--------|---------|-----------|----------|---------------|
| 12 | API setup | Error handling | Tkinter shell | Buffer day | Basic working app |
| 13 | Feature 1 | Integrate | Feature 1 complete | | |
| 14 | Feature 2 start | Review & test | Finish | | Feature 2 complete |
| 15 | Feature 3 | Polish UI | Error passing | Refactor | All features complete |
| 16 | Enhancement | Docs | Tests | Packaging | Ready-to-ship app |
| 17 | Rehearse | Buffer | Showcase | | Demo Day |

## Section 6: Risk Assessment
Identify at least 3 potential risks and how you'll handle them.

| Risk | Likelihood (High/Med/Low) | Impact (High/Med/Low) | Mitigation Plan |
|------|---------------------------|----------------------|-----------------|
| API Rate Limit | Medium | Medium | Add delays or cache recent results |
|  Data Structure Setup    |          Medium                 |    High                  |       Leave a buffer          |
|  Feature creep    |          low                 |        low              |        focus on core and required features first         |
|      |                           |                      |                 |

## Section 7: Support Requests
What specific help will you ask for in office hours or on Slack/Discord?  

- Postgres set up perhaps
- use Postgres or json or dictionaries for some data storage and look up

## Section 8: Before Monday (Start of Week 12)
Complete these setup steps before Monday:

- [x ] Push `main.py`, `config.py`, and a `/data/` folder to your repo
- [ x] Add OpenWeatherMap key to `.env` (⚠️ Do *not* commit the key)
- [x ] Copy chosen feature templates into `/features/`
- [ x] Commit and push a first-draft `README.md`
- [ x] Book office hours if you're still stuck on API setup

## Final Submission Checklist (Due Friday 23:59)
- [x ] `Week11_Reflection.md` completed
- [ x] File uploaded to GitHub repo `/docs/`
- [x ] Repo link submitted on Canvas
