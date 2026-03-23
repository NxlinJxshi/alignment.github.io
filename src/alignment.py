"""
Rationality estimation and alignment score computation.

This module provides functions for estimating rationality parameters
and computing alignment scores between observed behavior and inferred preferences.
"""

import numpy as np


def negative_log_likelihood(lambda_rationality, logits, y_true):
    """
    Compute negative log-likelihood for rationality-scaled predictions.
    
    Args:
        lambda_rationality: Rationality parameter λ
        logits: Raw logits η_i
        y_true: True binary labels
        
    Returns:
        float: Negative log-likelihood
    """
    pass


def estimate_rationality(logits, y_true, lambda_init=1.0, method='newton'):
    """
    Estimate optimal rationality parameter using Newton's method.
    
    Args:
        logits: Raw logits from model
        y_true: True binary labels
        lambda_init: Initial guess for λ
        method: Optimization method ('newton' or 'grid')
        
    Returns:
        float: Optimal rationality parameter λ̂
    """
    pass


def compute_regret_alignment(utilities, observed_shares, inferred_preferences):
    """
    Compute regret-based alignment scores.
    
    Args:
        utilities: Utility values
        observed_shares: Observed time/attention shares
        inferred_preferences: Inferred preference parameters
        
    Returns:
        numpy.ndarray: Alignment scores
    """
    pass


def compute_stability_score(shares_before, shares_after):
    """
    Compute preference stability score under context shift.
    
    Args:
        shares_before: Shares before context shift
        shares_after: Shares after context shift
        
    Returns:
        float: Stability score
    """
    pass

