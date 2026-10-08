"""
Source package for Credit Scoring Project.
"""
# Expose data_analysis_utils at src level for backward compatibility
try:
    from src.data_analysis import data_analysis_utils
except ImportError:
    pass
