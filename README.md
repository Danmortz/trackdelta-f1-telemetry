# F1 Telemetry & Performance Analysis Dashboard

A **Python-based Formula 1 telemetry and performance analysis tool** built using the **FastF1 API** and **Matplotlib**, designed to replicate a **broadcast-style F1 team analytics screen** inspired by Red Bull Racing and F1TV visuals.

This project allows deep analysis of race and qualifying data including **gear usage maps, telemetry comparisons, lap time evolution, and qualifying deltas** — all presented in a clean, dark, professional dashboard theme.

---

## 🚀 Features

### 🗺 Track Gear Map
- Visualizes the **fastest lap racing line**
- Color-coded by **gear usage**
- Auto-centered, square track layout
- Broadcast-style HUD with fastest lap info

### 📊 Telemetry Comparison (Driver vs Driver)
- RPM
- Speed
- Throttle
- Brake
- Gear
- DRS
- Distance-aligned telemetry
- Left-margin legend like F1 broadcast screens

### ⏱ Lap Time Comparison
- Full race lap-by-lap comparison
- Useful for **stint consistency analysis**

### 🏁 Qualifying Delta Visualization
- Fastest lap per driver vs pole
- Team-colored bars (FastF1 team colors)
- Delta time annotations (+ms / +s)
- Ideal for **qualifying performance reviews**

### 🎨 Red Bull–Inspired Analyst Theme
- Dark telemetry dashboard aesthetic
- Bold gridlines and axis styling
- Cross-Matplotlib version compatibility
- Designed for long analysis sessions

---

## 🛠 Tech Stack

- **Python 3**
- **FastF1** – Official F1 timing & telemetry API
- **Matplotlib** – Visualization
- **NumPy / Pandas** – Data processing
- **Timple** – Time delta formatting

---

## 📂 Project Structure

```text
f1-telemetry-dashboard/
│
├── main.py               # Main application script
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── f1_cache/             # FastF1 local cache (auto-created)
