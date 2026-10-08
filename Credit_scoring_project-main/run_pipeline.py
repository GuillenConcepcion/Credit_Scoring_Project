"""
==============================================================================
Credit Scoring - End-to-End Pipeline Runner
==============================================================================
Author: Guillén Concepción (Senior Data Scientist & MLOps Engineer)
Architecture: Production-grade CRISP-DM Credit Risk Assessment Pipeline

This script orchestrates the end-to-end credit scoring pipeline:
  Phase 1: Raw Ingestion, Feature Derivation & Exploratory Data Analysis (EDA)
  Phase 2: Stratified Split, Outlier Clipping & Missing Value Imputation
  Phase 3: Correlation & Association Analysis (Kruskal-Wallis, Cramér's V, Spearman)
  Phase 4: Feature Discrimination Analysis & Cole Storytelling Visualization
  Phase 5: Monotony & Population Stability Index (PSI) Assessment
  Phase 6: 4-Fold Cross-Validation & Robust Multi-Rule Feature Selection
==============================================================================
"""

import sys
import os
import time

# Ensure UTF-8 output encoding on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless execution
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold

# Ensure project root is in sys.path
this_dir = Path(__file__).resolve().parent
if str(this_dir) not in sys.path:
    sys.path.insert(0, str(this_dir))

from config import data_path, src_path, data_output_path, folds_path
from src.data_analysis.data_analysis_utils import (
    create_quartile_bins,
    generate_categorical_report_excel
)
from src.data_analysis.data_cleaning import (
    build_distribution_summary,
    build_bounds_table,
    apply_iqr_bounds,
    impute_missing_values
)
from src.data_analysis.correlations import (
    correlation_quanti_def_KW,
    cramers_v_with_target,
    correlation_matrix_quanti,
    cramers_v_matrix
)
from src.data_analysis.feature_discrimination_plots import (
    plot_grouped_bar,
    contingency_analysis
)
from src.data_analysis.monotony_stability import (
    compute_psi_table,
    compute_psi_stability
)
from src.correlation.functions_for_var_selection import (
    build_and_save_folds,
    filter_uncorrelated_with_target,
    filter_categorical_variables,
    filter_correlated_variables_kfold,
    filter_correlated_categorical_variables
)


def log_step(step_num: int, title: str):
    separator = "=" * 78
    print(f"\n{separator}")
    print(f" [PHASE {step_num}] {title.upper()}")
    print(f"{separator}")


def run_phase_1_eda():
    log_step(1, "Raw Ingestion, Feature Derivation & Exploratory Data Analysis")
    raw_path = data_path / "credit_risk_dataset.csv"
    if not raw_path.exists():
        print("Raw dataset not found locally. Downloading via kagglehub...")
        import kagglehub
        dl_path = kagglehub.dataset_download("laotse/credit-risk-dataset")
        df_raw = pd.read_csv(os.path.join(dl_path, "credit_risk_dataset.csv"))
        df_raw.to_csv(raw_path, index=False)
        print(f"Downloaded and cached raw dataset to {raw_path}")
    else:
        print(f"Loading raw dataset from {raw_path}...")
        df_raw = pd.read_csv(raw_path)

    print(f"Raw dataset shape: {df_raw.shape}")

    # Feature engineering for credit history vintage and default label
    df = df_raw.copy()
    df["year"] = (2024 - df["cb_person_cred_hist_length"]).clip(lower=2013)
    df["def"] = df["loan_status"].astype(int)

    # Convert object columns to category
    obj_cols = df.select_dtypes(include="object").columns
    df[obj_cols] = df[obj_cols].astype("category")

    eda_dir = data_output_path / "eda_output"
    eda_dir.mkdir(parents=True, exist_ok=True)

    # Generate Excel EDA reports
    print("Generating EDA reports...")
    generate_categorical_report_excel(
        df=df,
        category_col="cb_person_cred_hist_length",
        default_col="def",
        output_path=str(eda_dir / "cb_person_cred_hist_length_report.xlsx"),
        sheet_name="Credit History Length",
        title="Distribution by Credit History Length",
        category_label="Credit History Length",
        sort_by="count",
        ascending=False
    )

    generate_categorical_report_excel(
        df=df,
        category_col="year",
        default_col="def",
        output_path=str(eda_dir / "year_report.xlsx"),
        sheet_name="Year",
        title="Distribution by Year of Credit History Start",
        category_label="Year of Credit History Start",
        sort_by="count",
        ascending=False
    )

    df_binned = create_quartile_bins(df, variable="person_age", new_var="age_quartile")
    generate_categorical_report_excel(
        df=df_binned,
        category_col="age_quartile",
        default_col="def",
        output_path=str(eda_dir / "age_quartile_report.xlsx"),
        sheet_name="Age Quartiles",
        title="Distribution by Age Quartiles",
        category_label="Age Quartiles",
        sort_by="default_rate",
        ascending=False
    )

    # Temporal split: Train/Test historical window (2013-2021) and Out-Of-Time (2022)
    train_test_df = df[df["year"] <= 2021].copy()
    oot_df = df[df["year"] == 2022].copy()

    train_test_path = data_path / "train_test_data.csv"
    oot_path = data_path / "oot_data.csv"
    train_test_df.to_csv(train_test_path, index=False)
    oot_df.to_csv(oot_path, index=False)

    print(f"Historical (Train/Test) rows: {len(train_test_df)} -> saved to {train_test_path.name}")
    print(f"OOT (Out-Of-Time) rows:       {len(oot_df)} -> saved to {oot_path.name}")
    return train_test_df, oot_df


def run_phase_2_cleaning(train_test_df, oot_df):
    log_step(2, "Stratified Splitting, Outlier Treatment & Missing Value Imputation")
    clean_dir = data_output_path / "data_cleaning_output"
    clean_dir.mkdir(parents=True, exist_ok=True)

    # Create composite stratification target
    train_test_df = train_test_df.copy()
    train_test_df["def_year"] = (
        train_test_df["def"].astype(str) + "_" + train_test_df["year"].astype(str)
    )

    # 80/20 Stratified Split
    train_df, test_df = train_test_split(
        train_test_df,
        test_size=0.20,
        random_state=42,
        stratify=train_test_df["def_year"]
    )
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)
    oot_df = oot_df.reset_index(drop=True)

    train_df.to_csv(data_path / "train_data.csv", index=False)
    test_df.to_csv(data_path / "test_data.csv", index=False)

    # Train per year distribution
    train_per_year = train_df.groupby("year")["def"].agg(
        n_defaults="sum",
        n_obs="count"
    )
    train_per_year.to_excel(data_path / "train_per_year.xlsx")

    # Overall dataset distribution summary
    dist_summary = build_distribution_summary({
        "Train": train_df,
        "Test": test_df,
        "OOT": oot_df
    })
    dist_summary.to_excel(clean_dir / "dataset_default_distribution.xlsx", index=False)
    print("Dataset Default Distribution:")
    print(dist_summary.to_string(index=False))

    # Outlier detection & IQR clipping computed on Train only
    continuous_vars = [
        "person_age",
        "person_income",
        "person_emp_length",
        "loan_amnt",
        "loan_int_rate",
        "loan_percent_income",
    ]
    bounds_table, train_clean, test_clean, oot_clean = apply_iqr_bounds(
        train=train_df,
        test=test_df,
        oot=oot_df,
        variables=continuous_vars
    )
    bounds_table.to_excel(clean_dir / "bounds_table.xlsx", index=False)

    # Missing values audit
    missing_table = (
        train_clean.isnull()
        .agg(["sum", "mean"])
        .T
        .rename(columns={"sum": "missing_count", "mean": "missing_percentage"})
    )
    missing_table.to_excel(clean_dir / "missing_values_table.xlsx", index=True)

    # Missing value imputation (conservative: emp_length=0, loan_int_rate=median)
    train_imp, test_imp, oot_imp = impute_missing_values(
        train=train_clean,
        test=test_clean,
        oot=oot_clean,
        emp_var="person_emp_length",
        rate_var="loan_int_rate",
        emp_value=0
    )

    train_imp.to_csv(data_path / "train_imputed.csv", index=False)
    test_imp.to_csv(data_path / "test_imputed.csv", index=False)
    oot_imp.to_csv(data_path / "oot_imputed.csv", index=False)

    print(f"Cleaned datasets exported successfully: Train={train_imp.shape}, Test={test_imp.shape}, OOT={oot_imp.shape}")
    return train_imp, test_imp, oot_imp


def run_phase_3_correlations(train_imputed):
    log_step(3, "Statistical Association & Multicollinearity Analysis")
    corr_dir = data_output_path / "correlation"
    corr_dir.mkdir(parents=True, exist_ok=True)

    continuous_vars = [
        "person_income",
        "person_age",
        "person_emp_length",
        "loan_amnt",
        "loan_int_rate",
        "loan_percent_income",
        "cb_person_cred_hist_length",
    ]
    qualitative_vars = [
        "person_home_ownership",
        "cb_person_default_on_file",
        "loan_intent",
        "loan_grade",
    ]
    target = "def"

    # Kruskal-Wallis test
    kw_results = correlation_quanti_def_KW(
        database=train_imputed,
        continuous_vars=continuous_vars,
        target=target
    )
    kw_results.to_excel(corr_dir / "correlations_kw.xlsx", index=False)
    print("Kruskal-Wallis p-values with Default Target:")
    print(kw_results.to_string(index=False))

    # Cramér's V with target
    cv_results = cramers_v_with_target(
        database=train_imputed,
        categorical_vars=qualitative_vars,
        target=target
    )
    cv_results.to_excel(corr_dir / "cramers_v.xlsx", index=False)
    print("\nCramér's V with Default Target:")
    print(cv_results.to_string(index=False))

    # Spearman correlation matrix
    spearman_corr = correlation_matrix_quanti(
        database=train_imputed,
        continuous_vars=continuous_vars,
        method="spearman"
    )
    spearman_corr.to_excel(corr_dir / "correlation_matrix_spearman.xlsx")

    # Cramér's V inter-categorical matrix
    cv_matrix = cramers_v_matrix(
        database=train_imputed,
        categorical_vars=qualitative_vars
    )
    cv_matrix.to_excel(corr_dir / "cramers_v_matrix.xlsx")
    print("\nCorrelation matrices saved to data_analysis_output/correlation/")


def run_phase_4_visualizations(train_imputed):
    log_step(4, "Feature Discrimination & Storytelling Visualizations")
    # Contingency analysis on Home Ownership
    ctg = contingency_analysis(
        df=train_imputed,
        var1="def",
        var2="person_home_ownership",
        plot=False
    )
    print(f"Chi2: {ctg['chi2']:.2f} (p-value: {ctg['p_value']:.4e}), Cramér's V: {ctg['cramers_v']:.4f}")

    # Cole storytelling chart
    plot_grouped_bar(
        df=train_imputed,
        cat_var="def",
        subcat_var="person_home_ownership",
        normalize="index",
        title="Default Rate by Home Ownership"
    )
    plt.close("all")
    print(f"Generated storytelling graphic: {this_dir / 'default_by_ownership.png'}")


def run_phase_5_monotony_stability(train_imputed, test_imputed, oot_imputed):
    log_step(5, "Monotony & Population Stability Index (PSI) Assessment")
    # Re-group home ownership categories for maximum risk stability
    mapping = {
        "OWN": "OWN",
        "MORTGAGE": "MORTGAGE",
        "RENT": "OTHER_RENT",
        "OTHER": "OTHER_RENT"
    }
    for df in [train_imputed, test_imputed, oot_imputed]:
        df["home_ownership_3"] = df["person_home_ownership"].map(mapping)

    continuous_vars = [
        "person_income",
        "person_emp_length",
        "loan_int_rate",
        "loan_percent_income"
    ]
    qualitative_vars = ["home_ownership_3", "cb_person_default_on_file"]

    # Year to year PSI on Train
    y2y_psi = compute_psi_table(
        df=train_imputed,
        continuous_vars=continuous_vars,
        qualitative_vars=qualitative_vars,
        year_var="year",
        bins=3
    )
    y2y_psi.to_excel(data_path / "year_to_year.xlsx")
    print("Year-to-Year PSI Table (Train):")
    print(y2y_psi.to_string())

    # Train vs Test vs OOT Stability
    stab_psi = compute_psi_stability(
        train=train_imputed,
        test=test_imputed,
        oot=oot_imputed,
        continuous_vars=continuous_vars,
        qualitative_vars=qualitative_vars,
        bins=3
    )
    stab_psi.to_excel(data_path / "psi_stability.xlsx")
    print("\nTrain vs Test vs OOT PSI Stability:")
    print(stab_psi.to_string())


def run_phase_6_variable_selection(train_imputed):
    log_step(6, "4-Fold Cross-Validation & Multi-Rule Feature Selection")
    skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    train_imputed = train_imputed.copy().reset_index(drop=True)
    train_imputed["fold"] = -1

    for fold, (_, test_idx) in enumerate(skf.split(train_imputed, train_imputed["def_year"])):
        train_imputed.loc[test_idx, "fold"] = fold

    # Persist folds
    folds = build_and_save_folds(
        train_imputed,
        fold_col="fold",
        save_dir=str(folds_path) + "/"
    )
    print(f"Generated {len(folds)} folds persisted to {folds_path}")

    continuous_vars = [
        "person_income",
        "person_age",
        "person_emp_length",
        "loan_amnt",
        "loan_int_rate",
        "loan_percent_income",
        "cb_person_cred_hist_length"
    ]
    qualitative_vars = [
        "person_home_ownership",
        "cb_person_default_on_file",
        "loan_intent",
        "loan_grade",
    ]

    # Rule 1: Drop continuous variables uncorrelated with target on any fold (p >= 0.05)
    rule1_vars = filter_uncorrelated_with_target(
        folds=folds,
        variables=continuous_vars,
        target="def_year",
        pvalue_threshold=0.05
    )
    print(f"\nRule 1 (Continuous vs Target) Retained ({len(rule1_vars)}): {rule1_vars}")

    # Rule 2: Drop categorical variables weakly linked to target (V < 0.10)
    rule2_vars = filter_categorical_variables(
        folds=folds,
        cat_variables=qualitative_vars,
        target="def_year",
        low_threshold=0.10,
        high_threshold=0.50
    )
    print(f"\nRule 2 (Categorical vs Target) Retained ({len(rule2_vars)}): {rule2_vars}")

    # Rule 3: Drop highly collinear continuous variables (Spearman >= 0.50)
    selected_continuous = filter_correlated_variables_kfold(
        folds=folds,
        variables=rule1_vars,
        target="def",
        threshold=0.50
    )
    print(f"\nRule 3 (Continuous Multicollinearity Filter) Retained ({len(selected_continuous)}): {selected_continuous}")

    # Rule 4: Drop redundant categorical variables (Cramér's V >= 0.50)
    selected_categorical = filter_correlated_categorical_variables(
        folds=folds,
        cat_variables=rule2_vars,
        target="def_year",
        high_threshold=0.50
    )
    print(f"\nRule 4 (Categorical Multicollinearity Filter) Retained ({len(selected_categorical)}): {selected_categorical}")

    final_features = selected_continuous + selected_categorical
    print(f"\n" + "#" * 78)
    print(f" FINAL SELECTED FEATURE SET ({len(final_features)} variables):")
    for idx, feat in enumerate(final_features, 1):
        print(f"   {idx}. {feat}")
    print("#" * 78)

    # Save selection summary to Excel
    selection_summary = pd.DataFrame({
        "Feature": final_features,
        "Type": ["Continuous" if f in selected_continuous else "Categorical" for f in final_features],
        "Selection_Status": "Selected"
    })
    selection_summary.to_excel(data_output_path / "final_selected_features.xlsx", index=False)
    print(f"Summary table saved to {data_output_path / 'final_selected_features.xlsx'}")
    return final_features


def main():
    start_time = time.time()
    print("=" * 78)
    print(" CREDIT SCORING PIPELINE EXECUTION STARTED")
    print(f" Working Directory: {this_dir}")
    print("=" * 78)

    train_test_df, oot_df = run_phase_1_eda()
    train_imp, test_imp, oot_imp = run_phase_2_cleaning(train_test_df, oot_df)
    run_phase_3_correlations(train_imp)
    run_phase_4_visualizations(train_imp)
    run_phase_5_monotony_stability(train_imp, test_imp, oot_imp)
    final_features = run_phase_6_variable_selection(train_imp)

    duration = time.time() - start_time
    print(f"\nALL 6 PHASES COMPLETED SUCCESSFULLY IN {duration:.2f} SECONDS!")


if __name__ == "__main__":
    main()
