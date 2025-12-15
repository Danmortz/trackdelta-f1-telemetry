import fastf1 as ff1
import fastf1.plotting as plotting
from fastf1.core import Laps
from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from matplotlib.collections import LineCollection
from cycler import cycler
import numpy as np
import pandas as pd
from timple.timedelta import strftimedelta


# -----------------------
# Theme: Red Bull Analyst (compatible with older Matplotlib)
# -----------------------
def apply_redbull_theme():
    """
    RedBull-style theme with stronger gridlines and axis lines for broadcast look.
    """
    RB_BG = "#071226"
    RB_CARD = "#0d1726"
    RB_TEXT = "#E6F0FF"
    RB_ACCENT_YELLOW = "#F7D117"
    RB_ACCENT_RED = "#FF4B2B"
    RB_ACCENT_BLUE = "#00A3FF"
    RB_GRID = "#122033"

    mpl.rcParams.update({
        "figure.facecolor": RB_BG,
        "axes.facecolor": RB_CARD,
        "savefig.facecolor": RB_BG,
        "axes.edgecolor": RB_GRID,
        "axes.labelcolor": RB_TEXT,
        "xtick.color": RB_TEXT,
        "ytick.color": RB_TEXT,
        "text.color": RB_TEXT,
        "figure.edgecolor": RB_BG,
        "font.size": 11,
        "font.family": "sans-serif",
        "axes.titleweight": "bold",
        "axes.titlepad": 10,
        "legend.frameon": False,
        "legend.loc": "best",

        # Bolder grid & axes for broadcast feel
        "grid.color": RB_GRID,
        "grid.linestyle": "--",
        "grid.linewidth": 0.75,
        "axes.linewidth": 1.2,        # axis spine thickness
        "lines.linewidth": 1.8,
        "lines.markersize": 4,

        # Ticks bolder
        "xtick.major.width": 1.0,
        "ytick.major.width": 1.0,
        "xtick.minor.width": 0.8,
        "ytick.minor.width": 0.8,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "axes.grid": True,
        "axes.spines.left": True,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.spines.bottom": True,
    })

    mpl.rcParams["axes.prop_cycle"] = cycler(color=[
        RB_ACCENT_BLUE,
        RB_ACCENT_YELLOW,
        RB_ACCENT_RED,
        "#7CE4FF",
        "#9AD94D",
        "#FF9F1C",
    ])

    mpl.rcParams['image.cmap'] = 'plasma'

# -----------------------
# Your original functions (logic unchanged)
# -----------------------
def prepare_session(year: int, event_name: str, session_code: str):
    """Load an F1 session with telemetry and return (session, laps)."""
    print(f"\nLoading session: {year} {event_name} ({session_code}) ...")
    session = ff1.get_session(year, event_name, session_code)
    session.load(telemetry=True)
    laps = session.laps
    print(f"Loaded {len(laps)} laps")
    return session, laps


def build_driver_data(laps: Laps, driver_code: str):
    """Return (laps_for_driver, fastest_lap, telemetry_with_distance)."""
    driver_laps = laps.pick_drivers(driver_code)
    fastest = driver_laps.pick_fastest()
    telemetry = fastest.get_car_data().add_distance()
    return driver_laps, fastest, telemetry

def add_dashboard_decor(fig, title=None):
    """
    Small helper: adds RedBull watermark, tight card padding & a top-left HUD area.
    """
    # watermark / brand
    fig.text(0.98, 0.02, "RB ANALYTICS", ha='right', va='bottom',
             fontsize=9, alpha=0.12, weight='bold')
    if title:
        fig.suptitle(title, fontsize=14, weight='bold', y=0.98)

    # try to use constrained layout if available for nicer spacing
    try:
        fig.set_constrained_layout_pads(hspace=0.05, wspace=0.05)
    except Exception:
        pass


def track(laps: Laps):
    """Track layout - Fastest Lap Gear Shift Visualization (fixed colors + centering)."""
    lap = laps.pick_fastest()
    tel = lap.get_telemetry()

    x = np.array(tel['X'].values)
    y = np.array(tel['Y'].values)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # use gear values that align with segments (len(segments) == len(gear_for_segments))
    gear = tel['nGear'].to_numpy().astype(float)
    if len(gear) >= 2:
        gear_for_segments = gear[:-1]
    else:
        gear_for_segments = gear

    # Use a perceptually-pleasing colormap and proper normalization
    cmap = mpl.cm.get_cmap('plasma')
    norm = plt.Normalize(vmin=np.nanmin(gear_for_segments), vmax=np.nanmax(gear_for_segments))

    lc_comp = LineCollection(
        segments,
        cmap=cmap,
        norm=norm,
        linewidths=4.5,
        alpha=0.95,
        zorder=2
    )
    # assign per-segment values (must match segments length)
    lc_comp.set_array(gear_for_segments)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.add_collection(lc_comp)

    # Compute symmetric limits so track is centered and fills the card nicely
    if x.size and y.size:
        xmin, xmax = x.min(), x.max()
        ymin, ymax = y.min(), y.max()
        xrange = xmax - xmin
        yrange = ymax - ymin
        # take the larger span to create a square view and center it
        span = max(xrange, yrange)
        # small padding
        pad = span * 0.04 if span > 0 else 1.0
        xmid = (xmax + xmin) / 2.0
        ymid = (ymax + ymin) / 2.0
        ax.set_xlim(xmid - span/2.0 - pad, xmid + span/2.0 + pad)
        ax.set_ylim(ymid - span/2.0 - pad, ymid + span/2.0 + pad)

    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor(mpl.rcParams['axes.facecolor'])
    ax.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    # hide spines for the card look
    for sp in ax.spines.values():
        sp.set_visible(False)

    # Colorbar styled safely cross-version
    cbar = fig.colorbar(mappable=lc_comp, ax=ax, fraction=0.046, pad=0.02, label="Gear")
    # make ticks readable on dark bg
    try:
        cbar.ax.yaxis.set_tick_params(color=mpl.rcParams["text.color"])
        for t in cbar.ax.get_yticklabels():
            t.set_color(mpl.rcParams["text.color"])
        cbar.set_label("Gear", color=mpl.rcParams["text.color"])
    except Exception:
        pass

    # HUD: lap info (small)
    try:
        best = lap['LapTime']
        lap_str = strftimedelta(best, '%m:%s.%ms')
        ax.text(0.02, 0.985, f"Fastest Lap: {lap_str}  |  Driver: {lap['Driver']}",
                transform=ax.transAxes, fontsize=10, va='top', color=mpl.rcParams['text.color'],
                bbox=dict(facecolor=mpl.rcParams['axes.facecolor'], edgecolor='none', alpha=0.65, pad=6))
    except Exception:
        pass

    add_dashboard_decor(fig, title="Fastest Lap — Gear Map")

def gas(telemetry_driver1, telemetry_driver2, driver1: str, driver2: str):
    """
    Telemetry comparison with legend placed in the left margin.
    Fixed to work across Matplotlib versions (safe legend handle access).
    """
    data_fields = ['RPM', 'Speed', 'Throttle', 'Brake', 'nGear', 'DRS']

    fig, ax = plt.subplots(len(data_fields), 1, figsize=(13, 10), sharex=True, constrained_layout=False)
    add_dashboard_decor(fig, title="Fastest Race Lap Telemetry Comparison")

    prop_colors = [d['color'] for d in mpl.rcParams['axes.prop_cycle']]
    color1 = prop_colors[0] if len(prop_colors) > 0 else '#00A3FF'
    color2 = prop_colors[1] if len(prop_colors) > 1 else '#F7D117'

    # Copy & interpolate (avoid deprecated fillna method syntax)
    d1 = telemetry_driver1.copy()
    d2 = telemetry_driver2.copy()

    for col in data_fields:
        if col in d1:
            d1[col] = d1[col].interpolate().bfill().ffill()
        if col in d2:
            d2[col] = d2[col].interpolate().bfill().ffill()

    for i, field in enumerate(data_fields):
        ax_i = ax[i]

        if field in d1:
            ax_i.plot(d1['Distance'], d1[field], label=driver1,
                      linewidth=2.4, color=color1, zorder=3)

        if field in d2:
            ax_i.plot(d2['Distance'], d2[field], label=driver2,
                      linewidth=2.0, color=color2, alpha=0.95, zorder=2)

        # Y-label
        ax_i.set_ylabel(field, fontsize=9, labelpad=8)
        ax_i.yaxis.set_label_coords(-0.065, 0.5)

        # Bolder broadcast-style grid
        ax_i.grid(True, linestyle='--', linewidth=0.75, zorder=0)

        # Subtle side trim
        try:
            trim_color = color1 if i % 2 == 0 else color2
            ax_i.add_patch(plt.Rectangle((-0.03, 0), 0.02, 1, transform=ax_i.transAxes,
                                        facecolor=trim_color, alpha=0.04, zorder=1))
        except Exception:
            pass

        ax_i.tick_params(axis='y', labelsize=8)

        try:
            yt = ax_i.get_yticks()
            if len(yt) > 4:
                ax_i.set_yticks(np.linspace(yt.min(), yt.max(), 4))
        except:
            pass

        for sp in ax_i.spines.values():
            sp.set_linewidth(1.0)

    # === Legend in left margin (fixed) ===
    fig.subplots_adjust(left=0.20, right=0.97, top=0.92, bottom=0.08, hspace=0.36)

    legend = ax[0].legend(
        [driver1, driver2],
        loc='upper left',
        bbox_to_anchor=(-0.12, 1.02),
        bbox_transform=ax[0].transAxes,
        frameon=True,
        ncol=1,
        borderaxespad=0,
        handlelength=1.8,
        handletextpad=0.6,
        fontsize=10
    )

    # Style legend safely across Matplotlib versions:
    try:
        # prefer the modern attribute if available
        handles = getattr(legend, "legend_handles", None)
        if handles is None:
            handles = getattr(legend, "legendHandles", None)
        if handles is None:
            # final fallback: ask legend for its lines (works for Line2D handles)
            handles = legend.get_lines()
    except Exception:
        handles = []

    try:
        legend.get_frame().set_facecolor(mpl.rcParams['axes.facecolor'])
        legend.get_frame().set_edgecolor('none')
    except Exception:
        pass

    # shrink markers / handles where possible
    for h in handles:
        try:
            # Line2D and Patch-like handles may implement set_markersize or set_linewidth
            if hasattr(h, "set_markersize"):
                h.set_markersize(6)
            if hasattr(h, "set_linewidth"):
                h.set_linewidth(2.0)
        except Exception:
            pass

    # X-axis
    ax[-1].set_xlabel("Distance (m)", fontsize=10)
    plt.setp(ax[-1].get_xticklabels(), rotation=0, ha='center', fontsize=9)

def compare(laps_driver1: Laps, laps_driver2: Laps, driver1: str, driver2: str):
    """Lap time comparison over all laps."""
    fig, ax = plt.subplots(figsize=(9, 4))

    ax.plot(
        laps_driver1['LapNumber'],
        laps_driver1['LapTime'],
        label=driver1
    )
    ax.plot(
        laps_driver2['LapNumber'],
        laps_driver2['LapTime'],
        label=driver2
    )

    ax.set_title(f"{driver1} vs {driver2} — Lap Time Comparison")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")

    ax.legend(frameon=False)
    fig.subplots_adjust(right=0.98, top=0.9)


def qualifying(session, laps: Laps):
    """Qualifying-style plot: fastest lap per driver vs pole, with delta labels after bars."""
    plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)

    drivers = pd.unique(laps['Driver'])
    list_fastest_laps = []

    for drv in drivers:
        drv_laps = laps.pick_drivers(drv)
        if drv_laps.empty:
            continue
        try:
            drvs_fastest_lap = drv_laps.pick_fastest()
        except Exception:
            continue
        if drvs_fastest_lap is None or drvs_fastest_lap.empty:
            continue
        list_fastest_laps.append(drvs_fastest_lap)

    if not list_fastest_laps:
        print("[qualifying] No valid fastest laps found for any driver. Not plotting.")
        return

    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

    # collect team colors (fastf1 helper)
    team_colors = []
    for index, lap_row in fastest_laps.iterlaps():
        color = plotting.get_team_color(lap_row['Team'], session)
        team_colors.append(color)

    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(
        fastest_laps.index,
        fastest_laps['LapTimeDelta'].apply(lambda td: td.total_seconds() if hasattr(td, "total_seconds") else float(td)),
        color=team_colors,
        edgecolor='black',
        linewidth=0.9
    )

    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])
    ax.invert_yaxis()
    ax.set_axisbelow(True)

    # stronger gridlines (vertical & horizontal)
    ax.xaxis.grid(True, linestyle='--', color=mpl.rcParams['grid.color'], linewidth=0.9, zorder=-1000)
    ax.yaxis.grid(False)

    # annotate delta AFTER each bar as a formatted time string (+0.123s)
    # convert pole diff seconds to show +mm:ss.mmm or +s.ms depending on magnitude
    max_val = max([b.get_width() for b in bars]) if bars else 0
    padding = max_val * 0.02 if max_val > 0 else 0.01

    for i, (bar, row) in enumerate(zip(bars, fastest_laps.itertuples())):
        val_seconds = bar.get_width()
        # format sensible time delta: if >=1s, show s.ms, else show ms
        if val_seconds >= 1.0:
            s = f"+{val_seconds:.3f}s"
        else:
            s = f"+{val_seconds*1000:.0f}ms"
        ax.text(bar.get_width() + padding, bar.get_y() + bar.get_height()/2.0,
                s, va='center', ha='left', fontsize=9, color=mpl.rcParams['text.color'])

    # Lap time label header
    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')
    event_name = session.event['EventName']
    event_year = session.event['EventDate'].year
    fig.suptitle(f"{event_name} {event_year} Qualifying\nFastest Lap: {lap_time_string} ({pole_lap['Driver']})")

    # make spines thicker
    for sp in ax.spines.values():
        sp.set_linewidth(1.1)


# -----------------------
# Main (apply theme)
# -----------------------
def main():
    # ---- CACHE ----
    ff1.Cache.enable_cache('/Users/danmortz/Documents/f1_cache')  # make sure this folder exists

    # ---- Apply FastF1 time support but override style with our theme ----
    plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)
    apply_redbull_theme()

    print("=== F1 Session Analyzer ===")
    print("Example events: Monza, Zandvoort, Abu Dhabi, Bahrain, Imola, Silverstone ...")
    print("Sessions: R (Race), Q (Quali), FP1, FP2, FP3\n")

    # ---- USER INPUT ----
    year_str = input("Enter year [default 2021]: ").strip()
    year = int(year_str) if year_str else 2021

    event_name = input("Enter event name (e.g. Monza, Zandvoort) [default Monza]: ").strip()
    if not event_name:
        event_name = "Monza"

    session_code = input("Enter session code (R, Q, FP1, FP2, FP3) [default R]: ").strip().upper()
    if not session_code:
        session_code = "R"

    # ---- LOAD SESSION ----
    session, laps = prepare_session(year, event_name, session_code)

    # ---- SHOW AVAILABLE DRIVERS ----
    driver_codes = sorted(pd.unique(laps['Driver']))
    print("\nAvailable driver codes in this session:")
    print(", ".join(driver_codes))

    default_d1 = driver_codes[0] if len(driver_codes) > 0 else ""
    default_d2 = driver_codes[1] if len(driver_codes) > 1 else default_d1

    d1_input = input(f"\nEnter Driver 1 code [default {default_d1}]: ").strip().upper()
    d2_input = input(f"Enter Driver 2 code [default {default_d2}]: ").strip().upper()

    driver1 = d1_input if d1_input in driver_codes else default_d1
    driver2 = d2_input if d2_input in driver_codes else default_d2

    print(f"\nUsing drivers: {driver1} vs {driver2}")

    # ---- BUILD DRIVER DATA ----
    laps_driver1, fastest_driver1, telemetry_driver1 = build_driver_data(laps, driver1)
    laps_driver2, fastest_driver2, telemetry_driver2 = build_driver_data(laps, driver2)

    # ---- PLOTS ----
    track(laps)
    gas(telemetry_driver1, telemetry_driver2, driver1, driver2)
    compare(laps_driver1, laps_driver2, driver1, driver2)
    qualifying(session, laps)

    plt.show()


if __name__ == '__main__':
    main()