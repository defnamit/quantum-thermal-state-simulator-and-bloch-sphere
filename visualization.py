import numpy as np
import matplotlib.pyplot as plt


def plot_bloch_sphere(rho):
    from physics import bloch_vector

    rx, ry, rz = bloch_vector(rho)

    # Create the sphere surface
    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 30)

    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(
        x, y, z,
        alpha=0.12,
        color="skyblue",
        edgecolor="gray",
        linewidth=0.3
    )

    # Draw coordinate axes
    ax.quiver(0, 0, 0, 1, 0, 0, color="red")
    ax.quiver(0, 0, 0, 0, 1, 0, color="green")
    ax.quiver(0, 0, 0, 0, 0, 1, color="blue")

    # Draw the qubit's Bloch vector
    ax.quiver(
        0, 0, 0, rx, ry, rz,
        color="black",
        linewidth=3,
        arrow_length_ratio=0.12
    )

    ax.text(1.1, 0, 0, "X")
    ax.text(0, 1.1, 0, "Y")
    ax.text(0, 0, 1.1, "|0>")
    ax.text(0, 0, -1.1, "|1>")

    ax.set_xlim([-1.1, 1.1])
    ax.set_ylim([-1.1, 1.1])
    ax.set_zlim([-1.1, 1.1])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title("Qubit Bloch Sphere")

    return fig
