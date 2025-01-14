
import pytest
import pandas as pd

from patient_trajectory.visualization import PatientTrajectoryVisualizer


def test_patient_trajectory_visualizer():
    # A small DataFrame for testing
    df = pd.DataFrame({
        "pasient": [1, 1, 2],
        "episode_start_date": ["2020-01-01", "2020-03-01", "2021-01-15"],
        "episode_end_date":   ["2020-02-01", "2020-04-01", "2021-02-15"],
        "age": [10, 11, 50],
        "cluster": [1, 2, 1],
        "diagnosis": ["Flu", "Cold", "Check-up"]
    })

    # Instantiate the visualizer
    viz = PatientTrajectoryVisualizer(df=df)

    # Plot
    fig, ax = viz.plot_gantt(
        annotation_cols=["diagnosis"],
        figsize=(6, 3),
        dpi=80,
        row_height=0.5,
        row_gap=0.1,
        annotation_fontsize=6,
        axis_fontsize=8,
        title_fontsize=10,
        add_cluster_legend=True,
        curve_color="blue",
        curve_linestyle="--",
        curve_linewidth=1.0,
        title="Test Patient Trajectory Plot"
    )

    # Basic check: fig and ax should be created
    assert fig is not None, "Figure is None!"
    assert ax is not None, "Axes object is None!"

    # Optionally, test specific aspects of the plot...
    # e.g., check the axis labels or title
    assert ax.get_xlabel() == "Age (Years)"
    assert ax.get_ylabel() == "Patient Episodes"

    # If you want to temporarily save the figure to ensure it visually looks correct
    # fig.savefig("test_output.png")

    # Cleanup
    # (Matplotlib auto-closes but you could do plt.close(fig) if needed)
