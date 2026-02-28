import streamlit as st
import numpy as np
import time
import base64

st.set_page_config(page_title="Penguin Evolution Simulation", layout="wide")

st.title("🐧 Penguin Evolution Simulation")

# --- Controls ---
x0 = st.slider("Initial proportion of Jumpers (x₀)", 0.0, 1.0, 0.3, 0.05)
T = st.slider("Waiting cost T", 0.0, 12.0, 3.0, 0.1)
rounds = st.slider("Number of rounds", 5, 60, 30, 1)
speed = st.slider("Animation speed (seconds per round)", 0.0, 0.3, 0.05, 0.01)

# --- Continuous rest point ---
def x_star(T):
    return (3 + T) / (8 + 0.35 * T)

# --- Evolutionary update (hump‑proof, adaptive speed) ---
STEP = 0.6

def update_x(x, T):
    target = x_star(T)
    target = max(0.0, min(1.0, target))  # clamp to feasible range
    gap = target - x
    return x + STEP * gap * (1 - abs(gap))

# --- Penguin SVGs ---
BLUE_PENGUIN = """
<svg width="24" height="24" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
<path fill="#1E90FF" d="M36 8c-9 0-16 7-16 20 0 15 8 24 16 24s16-9 16-24C52 15 45 8 36 8z"/>
<path fill="#FFFFFF" d="M36 20c-7 0-12 6-12 14 0 10 6 16 12 16s12-6 12-16C48 26 43 20 36 20z"/>
</svg>
"""

GREY_PENGUIN = """
<svg width="24" height="24" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
<path fill="#808080" d="M36 8c-9 0-16 7-16 20 0 15 8 24 16 24s16-9 16-24C52 15 45 8 36 8z"/>
<path fill="#FFFFFF" d="M36 20c-7 0-12 6-12 14 0 10 6 16 12 16s12-6 12-16C48 26 43 20 36 20z"/>
</svg>
"""

def svg_url(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

BLUE_URL = svg_url(BLUE_PENGUIN)
GREY_URL = svg_url(GREY_PENGUIN)

NUM_PENGUINS = 40
penguin_area = st.empty()
graph_area = st.empty()

def draw_penguins(x):
    n_jump = int(round(x * NUM_PENGUINS))
    icons = [f"<img src='{BLUE_URL}'/>"] * n_jump + \
            [f"<img src='{GREY_URL}'/>"] * (NUM_PENGUINS - n_jump)
    np.random.shuffle(icons)
    rows = ["".join(icons[i:i+10]) for i in range(0, NUM_PENGUINS, 10)]
    penguin_area.markdown("<br>".join(rows), unsafe_allow_html=True)

# --- Run simulation ---
if st.button("Run evolution"):
    x = x0
    xs = [x]

    for _ in range(rounds):
        draw_penguins(x)
        graph_area.line_chart(xs)
        time.sleep(speed)

        x = update_x(x, T)
        x = max(0.0, min(1.0, x))
        xs.append(x)

    draw_penguins(x)
    graph_area.line_chart(xs)

    st.write(f"Final proportion of Jumpers:  x ≈ {x:.4f}")
    st.write(f"Continuous rest point:  x*(T) ≈ {x_star(T):.4f}")


