
import numpy as np
import pandas as pd
import pytest

from patient_trajectory.visualization import PatientTrajectoryVisualizer


def test_load_data_and_rename():
    data = {
        "patient_id": [5, 5, 6],
        "episode_start_date": ["2001-01-01", "2005-01-01", None],
        "episode_end_date": ["2001-06-01", None, "2010-12-31"],
        "age": [0, 4, 50],
        "cluster": [1, 2, np.nan],
        "diagnosis": [np.nan, "B", "C"]
    }
    df = pd.DataFrame(data)

    viz = PatientTrajectoryVisualizer(
        selected_columns=["patient_id", "episode_start_date", "episode_end_date", "age", "cluster", "diagnosis"],
        rename_dict={"patient_id": "pasient"},
    )
    result = viz.load_data(df)

    assert "pasient" in result.columns
    assert "patient_id" not in result.columns

def test_plot_patient_timeline():
    data = {
        "pasient": [5, 5, 6],
        "episode_start_date": pd.to_datetime(["2001-01-01", "2005-01-01", "2010-01-01"]),
        "episode_end_date": pd.to_datetime(["2001-06-01", None, "2010-12-31"]),
        "age": [0, 4, 50],
        "cluster": [1, 2, np.nan],
        "diagnosis": [np.nan, "B", "C"]
    }
    df = pd.DataFrame(data)

    viz = PatientTrajectoryVisualizer()
    clean_df = viz.load_data(df)
    
    # We add 'diagnosis' to annotation_cols to test extra field display
    fig, ax = viz.plot_patient_timeline(
        clean_df,
        pasient_col="pasient",
        age_col="age",
        cluster_col="cluster",
        annotation_cols=["diagnosis"],
        xlim=(0,60)
    )
    assert fig is not None
    assert ax is not None

