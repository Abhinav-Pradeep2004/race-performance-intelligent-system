# Project Charter – Race Performance Intelligence System (RPIS)

## 1. Project overview
**Objective:**  
Design and implement a race performance and strategy analysis tool using public Formula 1 data to support decision-making similar to a race engineering and strategy team.

**Motivation:**  
Modern F1 teams rely on telemetry and strategy tools to understand pace, tyre behaviour, and race scenarios. This project recreates a simplified version of such a tool to demonstrate project engineering, data analysis, and systems thinking.

## 2. Scope

**In scope:**
- Use publicly available F1 data (via FastF1).
- Analyze race sessions (RACE) from at least one F1 season or selected races.
- Process lap and stint data (by driver, tyre compound, and pit stops).
- Implement simple tyre degradation modelling.
- Implement basic strategy comparison (e.g., one-stop vs two-stop).
- Build an interactive dashboard for exploring results.

**Out of scope:**
- Real-time live race integration.
- Detailed vehicle dynamics (CFD, suspension modelling, etc.).
- Full optimization-based strategy solvers used in real teams.

## 3. Stakeholders and roles
- **Primary user – Race Engineer:** uses the tool to understand driver pace and stint behaviour.
- **Primary user – Strategy Engineer:** uses the tool to compare simple strategies.
- **Project engineer – You (Abhinav):** responsible for planning, implementation, documentation, deployment, and maintenance.

## 4. Constraints
- Public data only, no access to internal McLaren data.
- Computation limited to personal laptop resources.
- Timeframe: Approximately 6–8 weeks total.
- Technology stack restricted to Python-based solutions and a simple web UI framework (Streamlit).

## 5. Success criteria
- A working dashboard deployed online and accessible via URL.
- At least 2–3 full races analyzed and demonstrable within the tool.
- All major project documents completed (charter, WBS, Gantt, risk register, testing summary, deployment guide).
- Clear, interview-ready explanation of design decisions and limitations.