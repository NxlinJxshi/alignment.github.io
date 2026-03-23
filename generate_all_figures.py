#!/usr/bin/env python3
"""
Generate all figures for data.qmd, model.qmd, and alignment.qmd
This script ensures all figures are saved to assets/figures/ even when Quarto execution is disabled.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import arviz as az

# Create output directory
outdir = Path("assets/figures")
outdir.mkdir(parents=True, exist_ok=True)

print("Generating figures for data.qmd, model.qmd, and alignment.qmd...")
print(f"Output directory: {outdir}\n")

# ============================================================================
# DATA.QMD FIGURES
# ============================================================================

print("=" * 60)
print("Generating data.qmd figures...")
print("=" * 60)

# Load data once
df = pd.read_csv('data/online_shoppers_intention.csv')

# 1. Revenue Distribution
print("\n1. Generating fig-revenue-distribution.png...")
revenue_counts = df["Revenue"].value_counts()
revenue_props = df["Revenue"].value_counts(normalize=True)

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(revenue_props.index.astype(str), revenue_props.values, 
              color=['#3498db', '#e74c3c'], alpha=0.7, edgecolor='black')
ax.set_xlabel('Revenue', fontsize=12, fontweight='bold')
ax.set_ylabel('Proportion', fontsize=12, fontweight='bold')
ax.set_title('Revenue Distribution (Proportions)', fontsize=14, fontweight='bold')
ax.set_ylim([0, 1])
ax.grid(axis='y', alpha=0.3, linestyle='--')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.3f}\n({height*100:.1f}%)',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
outfile = outdir / "fig-revenue-distribution.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# 2. Revenue by Weekend
print("\n2. Generating fig-revenue-weekend.png...")
weekend_revenue = df.groupby("Weekend")["Revenue"].mean()

fig, ax = plt.subplots()
weekend_revenue.plot(kind="bar", ax=ax, color=["#1abc9c", "#f39c12"], edgecolor='black')
ax.set_ylabel("Revenue Rate")
ax.set_xlabel("Weekend")
ax.set_title("Revenue Rate by Weekend")
ax.set_xticklabels(['Not Weekend', 'Weekend'], rotation=0)
for i, v in enumerate(weekend_revenue):
    ax.text(i, v + 0.01, f"{v:.2%}", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()

outfile = outdir / "fig-revenue-weekend.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# 3. Revenue by Visitor Type
print("\n3. Generating fig-revenue-visitor.png...")
visitor_revenue = df.groupby("VisitorType")["Revenue"].mean()

fig, ax = plt.subplots()
visitor_revenue.plot(kind="bar", ax=ax, color="#8e44ad", edgecolor='black')
ax.set_ylabel("Revenue Rate")
ax.set_xlabel("Visitor Type")
ax.set_title("Revenue Rate by Visitor Type")
for i, v in enumerate(visitor_revenue):
    ax.text(i, v + 0.01, f"{v:.2%}", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()

outfile = outdir / "fig-revenue-visitor.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# 4. Revenue by Month
print("\n4. Generating fig-revenue-month.png...")
month_revenue = df.groupby("Month")["Revenue"].mean().sort_values()

fig, ax = plt.subplots(figsize=(10,5))
month_revenue.plot(kind="bar", ax=ax, color="#3498db", edgecolor='black')
ax.set_ylabel("Revenue Rate")
ax.set_xlabel("Month")
ax.set_title("Revenue Rate by Month")
for i, v in enumerate(month_revenue):
    ax.text(i, v + 0.004, f"{v:.2%}", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()

outfile = outdir / "fig-revenue-month.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# 5. Revenue by Browser
print("\n5. Generating fig-revenue-browser.png...")
browser_revenue = df.groupby("Browser")["Revenue"].mean()

fig, ax = plt.subplots()
browser_revenue.plot(kind="bar", ax=ax, color="#e67e22", edgecolor='black')
ax.set_ylabel("Revenue Rate")
ax.set_xlabel("Browser")
ax.set_title("Revenue Rate by Browser")
for i, v in enumerate(browser_revenue):
    ax.text(i, v + 0.01, f"{v:.2%}", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()

outfile = outdir / "fig-revenue-browser.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# 6. Revenue by Region
print("\n6. Generating fig-revenue-region.png...")
region_revenue = df.groupby("Region")["Revenue"].mean()

fig, ax = plt.subplots(figsize=(8,5))
region_revenue.plot(kind="bar", ax=ax, color="#16a085", edgecolor='black')
ax.set_ylabel("Revenue Rate")
ax.set_xlabel("Region")
ax.set_title("Revenue Rate by Region")
for i, v in enumerate(region_revenue):
    ax.text(i, v + 0.01, f"{v:.2%}", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()

outfile = outdir / "fig-revenue-region.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# 7. Bounce vs Exit Rates
print("\n7. Generating fig-bounce-exit.png...")
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df['BounceRates'], df['ExitRates'], alpha=0.5)
ax.set_xlabel('Bounce Rates')
ax.set_ylabel('Exit Rates')
ax.set_title('Bounce Rates vs Exit Rates')
plt.tight_layout()

outfile = outdir / "fig-bounce-exit.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# 8. Correlation Matrix
print("\n8. Generating fig-correlation-matrix.png...")
selected_features = [
    'Administrative_Duration',
    'Informational_Duration',
    'ProductRelated_Duration',
    'PageValues',
    'BounceRates',
    'ExitRates'
]

corr_matrix = df[selected_features].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True, 
            cbar_kws={"shrink": .8}, annot_kws={"size":11}, ax=ax)
ax.set_title('Correlation Heatmap of Selected Features', fontsize=14, fontweight='bold')
plt.tight_layout()

outfile = outdir / "fig-correlation-matrix.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# ============================================================================
# MODEL.QMD FIGURES
# ============================================================================

print("\n" + "=" * 60)
print("Generating model.qmd figures...")
print("=" * 60)

# Load trace and feature names
print("\nLoading PyMC trace and feature names...")
with open('data/processed/pymc_trace.pkl', 'rb') as f:
    trace = pickle.load(f)

with open('data/processed/feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

# Generate summary statistics
summary = az.summary(trace, var_names=["beta", "intercept"])
summary["feature"] = ["intercept"] + list(feature_names)

# Visualize top positive and negative predictors
summary_beta = summary.loc[summary["feature"] != "intercept"]
summary_sorted = summary_beta.sort_values("mean")

# 9. Top Positive Predictors
print("\n9. Generating fig-top-positive-predictors.png...")
top_pos = summary_sorted.tail(10)

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(top_pos["feature"], top_pos["mean"], color="green")
ax.set_title("Top Positive Predictors of Conversion (Posterior Mean)")
ax.set_xlabel("Posterior Mean")
plt.tight_layout()

outfile = outdir / "fig-top-positive-predictors.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# 10. Top Negative Predictors
print("\n10. Generating fig-top-negative-predictors.png...")
top_neg = summary_sorted.head(10)

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(top_neg["feature"], top_neg["mean"], color="red")
ax.set_title("Top Negative Predictors of Conversion (Posterior Mean)")
ax.set_xlabel("Posterior Mean")
plt.tight_layout()

outfile = outdir / "fig-top-negative-predictors.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# 11. Intercept Trace Plot
print("\n11. Generating fig-intercept-trace.png...")
axes = az.plot_trace(trace, var_names=["intercept"])
plt.tight_layout()

# ArviZ returns axes array, get the figure from the current figure
fig = plt.gcf()

outfile = outdir / "fig-intercept-trace.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# 12. Intercept Posterior
print("\n12. Generating fig-intercept-posterior.png...")
axes = az.plot_posterior(trace, var_names=["intercept"])
plt.tight_layout()

# ArviZ returns axes, get the figure from the current figure
fig = plt.gcf()

outfile = outdir / "fig-intercept-posterior.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {outfile}")

# ============================================================================
# ALIGNMENT.QMD FIGURES (if not already generated)
# ============================================================================

print("\n" + "=" * 60)
print("Checking alignment.qmd figures...")
print("=" * 60)

# Check if alignment figures exist, if not generate them
if not (outdir / "fig-optimization-convergence.png").exists():
    print("\n13. Generating fig-optimization-convergence.png...")
    with open('data/processed/rationality_temperature.pkl', 'rb') as f:
        rationality_results = pickle.load(f)

    lambda_hat = rationality_results['lambda_hat']
    history = rationality_results['optimization_history']

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

    outfile = outdir / "fig-optimization-convergence.png"
    fig.savefig(outfile, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {outfile}")
else:
    print("\n  fig-optimization-convergence.png already exists, skipping...")

if not (outdir / "fig-nll-landscape.png").exists():
    print("\n14. Generating fig-nll-landscape.png...")
    with open('data/processed/rationality_temperature.pkl', 'rb') as f:
        rationality_results = pickle.load(f)

    lambda_hat = rationality_results['lambda_hat']
    history = rationality_results['optimization_history']
    logits_val = rationality_results['logits_validation']
    y_val = np.load('data/processed/y_va.npy')

    def negative_log_likelihood(lambda_rationality, logits, y_true):
        lambda_rationality = max(lambda_rationality, 1e-8)
        z = lambda_rationality * logits
        log1p_exp_z = np.logaddexp(0, z)
        nll = np.sum(log1p_exp_z - lambda_rationality * y_true * logits)
        return nll

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

    outfile = outdir / "fig-nll-landscape.png"
    fig.savefig(outfile, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {outfile}")
else:
    print("\n  fig-nll-landscape.png already exists, skipping...")

print("\n" + "=" * 60)
print("All figures generated successfully!")
print("=" * 60)
print(f"\nTotal figures in {outdir}:")
for f in sorted(outdir.glob("*.png")):
    print(f"  - {f.name}")

