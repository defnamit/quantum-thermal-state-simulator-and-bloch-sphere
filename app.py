
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from physics import (
    thermal_state,
    purity,
    von_neumann_entropy,
    pure_state_density_matrix,
    apply_dephasing,
)


# ---------------- PAGE SETUP ----------------

st.set_page_config(
    page_title="Quantum Thermal State Simulator",
    layout="wide"
)

st.title("Quantum Thermal State Simulator")
st.write(
    "Explore quantum states, temperature, coherence, "
    "dephasing noise, and the Bloch sphere."
)


# ---------------- BLOCH SPHERE FUNCTION ----------------

def plot_bloch_sphere(rho):

    # Calculate Bloch vector from the density matrix
    rx = 2 * np.real(rho[0, 1])
    ry = -2 * np.imag(rho[0, 1])
    rz = np.real(rho[0, 0] - rho[1, 1])

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    # Generate sphere coordinates
    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 30)

    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    # Draw the sphere
    ax.plot_surface(
        x, y, z,
        color="skyblue",
        alpha=0.12,
        edgecolor="gray",
        linewidth=0.3
    )

    # Draw the X, Y and Z axes
    ax.quiver(0, 0, 0, 1, 0, 0, color="red")
    ax.quiver(0, 0, 0, 0, 1, 0, color="green")
    ax.quiver(0, 0, 0, 0, 0, 1, color="blue")

    # Draw the Bloch vector for the final state
    ax.quiver(
        0, 0, 0,
        rx, ry, rz,
        color="black",
        linewidth=3,
        arrow_length_ratio=0.12
    )

    # Label the axes and basis states
    ax.text(1.1, 0, 0, "X")
    ax.text(0, 1.1, 0, "Y")
    ax.text(0, 0, 1.1, "|0>")
    ax.text(0, 0, -1.1, "|1>")

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)

    ax.set_box_aspect([1, 1, 1])
    ax.set_title("Bloch Sphere — Final State")

    return fig, (rx, ry, rz)


# ---------------- SELECT EXPERIMENT ----------------

mode = st.selectbox(
    "Choose an experiment",
    ["Pure quantum state + noise", "Thermal state"]
)


# ---------------- GENERATE QUANTUM STATE ----------------

if mode == "Pure quantum state + noise":

    state_name = st.selectbox(
        "Choose the initial state",
        ["Equal superposition", "|0>", "|1>"]
    )

    if state_name == "Equal superposition":
        alpha, beta = 1, 1
    elif state_name == "|0>":
        alpha, beta = 1, 0
    else:
        alpha, beta = 0, 1

    rho = pure_state_density_matrix(alpha, beta)

    p = st.slider(
        "Dephasing strength",
        0.0, 1.0, 0.0, 0.05
    )

    final_rho = apply_dephasing(rho, p)

else:

    T = st.slider(
        "Temperature",
        0.05, 10.0, 1.0
    )

    rho = thermal_state(T)
    final_rho = rho.copy()


# ---------------- DENSITY MATRIX COMPARISON ----------------

st.subheader("Density Matrix Comparison")

col1, col2 = st.columns(2)

with col1:
    st.write("Initial state")
    st.dataframe(np.round(rho, 4))

with col2:
    st.write("Final state")
    st.dataframe(np.round(final_rho, 4))


# ---------------- QUANTUM METRICS ----------------

st.subheader("Quantum Properties")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Initial purity",
        f"{purity(rho):.4f}"
    )

with col2:
    st.metric(
        "Final purity",
        f"{purity(final_rho):.4f}"
    )

with col3:
    st.metric(
        "Final entropy (bits)",
        f"{von_neumann_entropy(final_rho):.4f}"
    )


# ---------------- BLOCH SPHERE ----------------

st.subheader("Bloch Sphere Visualization")

fig_bloch, bloch_coords = plot_bloch_sphere(final_rho)

st.pyplot(fig_bloch)

rx, ry, rz = bloch_coords

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("X component", f"{rx:.4f}")

with col2:
    st.metric("Y component", f"{ry:.4f}")

with col3:
    st.metric("Z component", f"{rz:.4f}")


# ---------------- COHERENCE VS NOISE GRAPH ----------------

st.subheader("Coherence vs Noise Strength")

noise_values = np.linspace(0, 1, 101)
coherences = []

for noise in noise_values:

    noisy = apply_dephasing(rho, noise)

    # Magnitude of the off-diagonal element
    coherence = abs(noisy[0, 1])

    coherences.append(coherence)

fig, ax = plt.subplots()

ax.plot(noise_values, coherences)

ax.set_xlabel("Dephasing strength")
ax.set_ylabel("Magnitude of off-diagonal element")
ax.set_title("How Noise Affects Coherence")
ax.grid(True)

st.pyplot(fig)
