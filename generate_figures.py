#!/usr/bin/env python3
"""
Generate figures for alignment.qmd
Run this script to regenerate figures before rendering the Quarto document.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pickle
import numpy as np

# Create output directory
outdir = Path("assets/figures")
outdir.mkdir(parents=True, exist_ok=True)

print("Loading data...")
# Load results
with open('data/processed/rationality_temperature.pkl', 'rb') as f:
    rationality_results = pickle.load(f)

lambda_hat = rationality_results['lambda_hat']
history = rationality_results['optimization_history']
logits_val = rationality_results['logits_validation']

# Load validation targets
y_val = np.load('data/processed/y_va.npy')

print("Generating figure 1: Optimization convergence...")
# Figure 1: Optimization convergence
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

axes[0, 0].plot(history['lambda'], marker='o', markersize=4)
axes[0, 0].axhline(y=lambda_hat, color='r', linestyle='--', label=f'Final λ̂ = {lambda_hat:.4f}')
axes[0, 0].set_xlabel('Iteration')
axes[0, 0].set_ylabel('Rationality Parameter λ')
axes[0, 0].set_title('Rationality Parameter Convergence')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(history['nll'], marker='o', markersize=4, color='green')
axes[0, 1].set_xlabel('Iteration')
axes[0, 1].set_ylabel('Negative Log-Likelihood')
axes[0, 1].set_title('Objective Function (NLL)')
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].plot(history['grad'], marker='o', markersize=4, color='orange')
axes[1, 0].axhline(y=0, color='r', linestyle='--')
axes[1, 0].set_xlabel('Iteration')
axes[1, 0].set_ylabel('Gradient')
axes[1, 0].set_title('Gradient Convergence')
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(history['hess'], marker='o', markersize=4, color='purple')
axes[1, 1].set_xlabel('Iteration')
axes[1, 1].set_ylabel('Hessian')
axes[1, 1].set_title('Hessian (should be ≥ 0)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()

# Save figure
outfile = outdir / "fig-optimization-convergence.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  ✓ Saved: {outfile}")

print("Generating figure 2: NLL landscape...")
# Define NLL function for grid evaluation
def negative_log_likelihood(lambda_rationality, logits, y_true):
    lambda_rationality = max(lambda_rationality, 1e-8)
    z = lambda_rationality * logits
    log1p_exp_z = np.logaddexp(0, z)
    nll = np.sum(log1p_exp_z - lambda_rationality * y_true * logits)
    return nll

# Evaluate NLL over a grid
lambda_grid = np.linspace(0.05, 5.0, 200)
nll_grid = np.array([negative_log_likelihood(lam, logits_val, y_val) for lam in lambda_grid])

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.plot(lambda_grid, nll_grid, 'b-', linewidth=2, label='NLL(λ)')
ax.axvline(x=lambda_hat, color='r', linestyle='--', linewidth=2, label=f'Newton λ̂ = {lambda_hat:.4f}')
ax.scatter([lambda_hat], [history['nll'][-1]], color='red', s=100, zorder=5, label='Optimal solution')
ax.set_xlabel('Rationality Parameter λ')
ax.set_ylabel('Negative Log-Likelihood')
ax.set_title('NLL vs Rationality Parameter')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()

# Save figure
outfile = outdir / "fig-nll-landscape.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  ✓ Saved: {outfile}")

print("\n✓ All figures generated successfully!")
print(f"  Location: {outdir.absolute()}")

