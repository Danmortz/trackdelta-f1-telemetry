# TrackDelta — Telemetry-Based Racing Analysis 🏁

TrackDelta is a Python project that analyzes racing telemetry data to understand how a vehicle behaves around a track.  
It focuses on visualizing speed, acceleration, braking, and gear usage to explain where time is gained or lost during a lap.

No prior knowledge of Formula 1 is required to understand the outputs.

---

## What This Project Shows

TrackDelta turns raw telemetry data into easy-to-read visual charts that help explain driving behavior on a racetrack.

It answers questions like:
- Where does the driver brake?
- Where does the car accelerate?
- How aggressively does the driver use gears?
- How consistent is the pace over multiple laps?

---

## Key Visualizations

### Track Map (Gear Usage)
- Displays the shape of the track using GPS data
- Colors the racing line based on gear usage
- Lower gears indicate tighter corners
- Higher gears indicate fast, straight sections

This helps visualize how the car is driven around the circuit.

---

### Telemetry Comparison (Two Drivers)
- Compares two drivers on the same lap
- Shows:
  - Engine speed (RPM)
  - Vehicle speed
  - Throttle input
  - Braking input
  - Gear selection
  - DRS (overtaking system)

This allows side-by-side analysis of driving style and performance.

---

### Lap Time Comparison
- Shows how lap times change across a race
- Helps identify:
  - Consistent pace
  - Pit stop laps
  - Performance drops or improvements

---

### Qualifying Performance Comparison
- Compares each driver’s fastest lap against the fastest overall lap
- Displays the time difference clearly
- Makes it easy to see relative performance

---

## How the Data Is Used

- Telemetry data is collected from FastF1, which provides official racing timing and telemetry
- GPS coordinates are used to reconstruct the track layout
- Telemetry signals are aligned using distance traveled along the lap
- Missing data is safely interpolated
- All charts are generated using Matplotlib with a clean, dark theme

This project focuses on data visualization and analysis, not prediction or simulation.

---

## Tools & Technologies

- Python
- FastF1
- Pandas
- NumPy
- Matplotlib

---

## Project Structure
