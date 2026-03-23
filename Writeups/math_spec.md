# Math Spec — Probabilistic Preference Inference & Alignment under Contextual Shifts

## 1. Problem Statement & Scope
**Goal:** Infer latent shopper preferences from session behavior in `online_shoppers_intention.csv`, then quantify **how consistently actions align** with those preferences, especially under **context shifts** (e.g., `Weekend`, `SpecialDay`, traffic sources). Produce interpretable **alignment/rationality scores** at the session and cohort level.

**Data (columns):**  
`Administrative`, `Administrative_Duration`, `Informational`, `Informational_Duration`, `ProductRelated`, `ProductRelated_Duration`, `BounceRates`, `ExitRates`, `PageValues`, `SpecialDay`, `Month`, `OperatingSystems`, `Browser`, `Region`, `TrafficType`, `VisitorType`, `Weekend`, `Revenue`.

**Key constraints:** Session-level aggregates (no user IDs or page sequences). This favors **structural discrete-choice / resource-allocation** models and **compositional modeling** of time shares, with contextual covariates.

---

## 2. Notation
- Sessions \(i=1,\dots,n\)
- Page categories \(j\in\{\text{Adm},\text{Info},\text{Prod}\}\)
- Counts: \(\mathbf{c}_i=(A_i, I_i, P_i)\)
- Durations: \(\mathbf{t}_i=(T^{\text{Adm}}_i, T^{\text{Info}}_i, T^{\text{Prod}}_i)\)
- Total: \(T_i=\sum_j T^j_i\)
- Shares: \(\mathbf{s}_i = \mathbf{t}_i/T_i \in \Delta^2\) (2-simplex)
- Context: \(\mathbf{z}_i\) (one-hot `Month`, `VisitorType`, `Weekend`, `SpecialDay`, etc.)
- Outcome: \(Y_i=\mathbf{1}\{\text{Revenue}=1\}\) — **auxiliary only**, not used for preference inference.

---

## 3. Modeling Assumptions
1. **Stable latent preferences** \(\boldsymbol{\theta}\) map context and page-type features to **utility** of allocating time/attention.
2. **Quantal (noisy) rationality**: actions maximize expected utility subject to stochasticity; inverse temperature \(\lambda\) captures rationality/consistency.
3. **Context shifts** perturb constraints/utilities but **do not** fundamentally change stable preferences; departures = misalignment/non-stationarity.

---

## 4. Primary Structural Model (Random Utility + Quantal Response)
Utility for allocating marginal attention to page type \(j\):

\[
U_{ij} = \alpha_j + \boldsymbol{\beta}_j^\top \mathbf{z}_i + \varepsilon_{ij}, \quad \varepsilon_{ij} \sim \text{i.i.d. Gumbel}
\]

Quantal response (multinomial logit) expected share:

\[
\mathbb{E}[s_{ij} \mid \mathbf{z}_i] =
\frac{\exp\left(\lambda (\alpha_j + \boldsymbol{\beta}_j^\top \mathbf{z}_i)\right)}
{\sum_{k} \exp\left(\lambda (\alpha_k + \boldsymbol{\beta}_k^\top \mathbf{z}_i)\right)}
\]

---

**Study Goals:**
- Derive MLE/MAP for multinomial logit on additive log-ratio (alr) transformed shares.
- Prove identifiability under scale confound (\(\lambda\) vs \(\Theta\)).
- Show convexity of negative log-likelihood in \(\Theta\) given \(\lambda\).
- Implement hierarchical Bayes: \(\boldsymbol{\beta}_j \sim \mathcal{N}(\mu_j, \Sigma)\), \(\lambda \sim \text{Lognormal}(\mu_\lambda, \sigma_\lambda^2)\).

---

## 5. Alternative View A — Logistic-Normal Compositional Regression
Transform \(\mathbf{s}_i\) via ALR:

\[
\boldsymbol{\eta}_i = \operatorname{alr}(\mathbf{s}_i) \in \mathbb{R}^2
\]

Model:

\[
\boldsymbol{\eta}_i \mid \mathbf{z}_i \sim \mathcal{N}(B \mathbf{z}_i, \Sigma)
\]

---

**Study Goals:**
- Derive ALR/ILR transforms, Jacobians, log-likelihood.
- Compare with quantal response; conditions for approximation.
- Bayesian inference via NUTS/VI and posterior predictive checks.

---

## 6. Alternative View B — MaxEnt IRL on Aggregated Features
Treat session as feature vector \(\mathbf{f}_i\) (counts/durations). Solve:

\[
\hat{\boldsymbol{\theta}} = \arg\max_{\boldsymbol{\theta}} \left[ \boldsymbol{\theta}^\top \bar{\mathbf{f}}_{\text{emp}} - \log Z(\boldsymbol{\theta}) \right]
\]

Partition function:

\[
Z(\theta) = \int_{\mathcal{A}} e^{\theta^\top \mathbf{f}(\mathbf{s})} \, d\mathbf{s}
\]

---

**Study Goals:**
- Define feasible set \(\mathcal{A} = \{\mathbf{s} \in \Delta^2\}\).
- Derive connection to exponential family matching \(\mathbb{E}_\theta[\mathbf{f}] = \bar{\mathbf{f}}_{\text{emp}}\).
- Implement numerical approximation and compare with structural model.

---

## 7. Alignment & Rationality Scores

**(a) Quantal Rationality \(\hat{\lambda}_i\):**  
Estimate \(\lambda\) per session/cohort from \(\mathbf{s}_i\).

**(b) Regret-Based Alignment:**
\[
R_i = \max_{\mathbf{s} \in \Delta^2} U(\mathbf{s}; \hat{\Theta}, \mathbf{z}_i) - U(\mathbf{s}_i; \hat{\Theta}, \mathbf{z}_i), \quad
S^{\text{regret}}_i = \exp(-R_i)
\]

**(c) Preference Stability under Context Shift:**
\[
S^{\text{stab}}_i = 1 - \operatorname{TV}(\mathbf{s}_i, \mathbf{s}^*_i(c))
\]

---

**Study Goals:**
- Hierarchical prior on \(\lambda\), stability checks.
- Closed-form optimizer for regret; prove \(0 < S^{\text{regret}}_i \le 1\).
- TV/KL/JS bounds for stability score changes.

---

## 8. Evaluation & Robustness
- **Predictive fit:** Cross-entropy on held-out shares.
- **Correlation:** \(S^{\text{regret}}\), \(\hat{\lambda}\) vs Revenue/PageValues.
- **OOD robustness:** Weekday→Weekend; covariate shift correction via density ratio \(w(\mathbf{z})\).

---

**Study Goals:**
- Prove unbiasedness of importance-weighted risk under correct \(w\).
- Implement conformal prediction for calibrated uncertainty.

---

## 9. Regularization & Interpretability
- Monotonicity constraints (isotonic regression or monotone GBT).
- Group-lasso for sparse, stable interpretation.
- SHAP for linear utility models; ALR-space interpretation.

---

## 10. Data Quality & Derived Features
- Compute shares from durations; filter \(T_i=0\).
- Treat `BounceRates`/`ExitRates` as diagnostics, not preference drivers.
- Seasonal bucketing of `Month`.

---

**Study Goal:**  
Prove why including post-treatment outcomes biases preference estimates.

---

## 11. Deliverables
- Hierarchical Bayes (PyMC/Stan).
- CVXPY regret optimization.
- Conformal calibration of alignment scores.
- API: `fit_preferences()`, `alignment_scores()`, `counterfactual()`.

---

## 12. Core Equations
1. **Quantal Response:**
\[
p_{ij} = \frac{\exp\{\lambda(\alpha_j+\beta_j^\top z_i)\}}{\sum_k \exp\{\lambda(\alpha_k+\beta_k^\top z_i)\}}
\]
2. **ALR Transform:**
\[
\eta_1 = \log\frac{s_{\text{Adm}}}{s_{\text{Prod}}}, \quad
\eta_2 = \log\frac{s_{\text{Info}}}{s_{\text{Prod}}}
\]
3. **Logistic-Normal:**  
\(\eta \mid z \sim \mathcal{N}(Bz,\Sigma), \quad s = \text{softmax}([\eta;0])\)
4. **Regret:**  
\(S^{\text{regret}}_i = \exp(-R_i)\)
5. **Stability:**  
\(S^{\text{stab}}_i = 1 - \text{TV}(s_i, s_i^*(c))\)
6. **Density Ratio:**  
\(w(x) = \frac{\pi\,\sigma^{-1}(d=1|x)}{(1-\pi)\,[1-\sigma^{-1}(d=1|x)]}\)

---

## 13. Validation Plan
- Posterior predictive checks.
- Correlation analysis.
- OOD and covariate-shift testing.

---

## 14. Risks & Mitigations
- Identifiability: fix scale or impose priors.
- No sequences: use allocation models.
- Post-treatment bias: exclude certain features.

---

## 15. Week-by-Week Study Path (14 hrs/week pace)

### Week 1 — Foundations & Spec Check
- Discrete choice theory, compositional data basics.
- ALR/ILR transforms.
- **Milestone:** finalize notation & dataset prep.

### Week 2 — Estimation & Inference
- MLE derivations, logistic-normal likelihood.
- Implement MAP + VI.
- **Milestone:** posterior predictive checks.

### Week 3 — Alignment Metrics & Optimization
- Derive regret and stability metrics.
- Implement CVXPY routine.
- **Milestone:** pilot alignment scores.

### Week 4 — Causality & Robustness
- DAGs, post-treatment bias proofs.
- Double ML/CATEs for auxiliary analysis.
- Covariate shift correction.

### Week 5 — Synthesis & Reporting
- Interpretability: group-lasso, SHAP.
- Package code + write-up.
- **Milestone:** recruiter-ready project package.

---
