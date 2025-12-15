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

trackdelta-f1-telemetry/
│
├── trackdelta.py        # Main application script
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── LICENSE


## ⚙️ Installation

This project uses Python and the FastF1 API. Follow the steps below to set it up locally.

### 1️⃣ Clone the repository

    git clone https://github.com/Danmortz/trackdelta-f1-telemetry.git
    cd trackdelta-f1-telemetry

### 2️⃣ Create a virtual environment (recommended)

    python3 -m venv venv
    source venv/bin/activate   # macOS / Linux

### 3️⃣ Install dependencies

    pip install -r requirements.txt


## ▶️ Usage

Run the main script:

    python trackdelta.py

You will be prompted to enter:

- Season year (default: 2021)
- Event name (e.g. Monza, Abu Dhabi, Silverstone)
- Session type:
  - `R`  → Race
  - `Q`  → Qualifying
  - `FP1`, `FP2`, `FP3` → Practice
- Two driver codes (e.g. `VER`, `HAM`, `NOR`)

### Example Input

    Enter year [default 2021]: 2025
    Enter event name [default Monza]: Abu Dhabi
    Enter session code [default R]: R
    Enter Driver 1 code [default VER]: VER
    Enter Driver 2 code [default HAM]: PIA

The script automatically generates:

- Track gear map (fastest lap racing line)
- Telemetry comparison (RPM, speed, throttle, brake, gear, DRS)
- Lap time comparison across the race
- Qualifying delta visualization vs pole


