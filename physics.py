import numpy as np

def thermal_state(T, gap=1.0):
    if T <= 0:
        raise ValueError("Temperature must be positive")

    p0 = 1 / (1 + np.exp(-gap / T))
    p1 = 1 - p0

    rho = np.array([
        [p0, 0],
        [0, p1]
    ], dtype=float)

    return rho


def purity(rho):
    return np.trace(rho @ rho).real


def von_neumann_entropy(rho):
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-12]

    return -np.sum(eigenvalues * np.log2(eigenvalues))


def pure_state_density_matrix(alpha, beta):
    psi = np.array([alpha, beta], dtype=complex)

    norm = np.linalg.norm(psi)
    if norm == 0:
        raise ValueError("State vector cannot be zero")

    psi = psi / norm

    rho = np.outer(psi, psi.conj())

    return rho


def apply_dephasing(rho, p):
    if not 0 <= p <= 1:
        raise ValueError("Noise strength must be between 0 and 1")

    result = rho.copy()
    result[0, 1] *= (1 - p)
    result[1, 0] *= (1 - p)

    return result


def bloch_vector(rho):

    if rho.shape != (2, 2):
        raise ValueError("Density matrix must be 2x2")

    rx = 2 * np.real(rho[0, 1])
    ry = -2 * np.imag(rho[0, 1])
    rz = np.real(rho[0, 0] - rho[1, 1])

    return np.array([rx, ry, rz])

