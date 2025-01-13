
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class PatientTrajectoryVisualizer:
    """
    A class to load, transform, and visualize patient trajectories for any number of patients.
    
    Key Features:
    -------------
    1. Load and prepare data with flexible options:
       - Select columns to keep.
       - Rename columns.
       - Drop unwanted columns.
       - Automatically sort by 'episode_start_date' if present.
       - Convert 'episode_start_date' and 'episode_end_date' to datetime.
       - Handle missing (NaN) values gracefully.
       
    2. Plot patient timelines:
       - Plot by 'age' or any numeric column that indicates a starting point.
       - Auto-calculate end position based on start date + date difference, if available.
       - Allows specifying a list of columns to annotate each episode segment.
       - Handle any number of patients.
       - Optionally color-code by cluster (or any integer column).
       - Save the figure to file if desired.

    Usage Example:
    --------------
    from patient_trajectory.visualization import PatientTrajectoryVisualizer
    import pandas as pd
    
    data = {
        "patient_id": [5, 5, 6],
        "episode_start_date": ["2001-01-01", "2005-01-01", "2010-01-01"],
        "episode_end_date": ["2001-06-01", "2005-06-01", "2010-12-31"],
        "age": [0, 4, 50],
        "cluster": [1, 2, np.nan],  # Missing cluster for patient 6
        "diagnosis": ["A", "B", None]
    }
    df = pd.DataFrame(data)
    
    # Instantiate visualizer with custom options
    viz = PatientTrajectoryVisualizer(
        selected_columns=["patient_id", "episode_start_date", "episode_end_date", "age", "cluster", "diagnosis"],
        rename_dict={"patient_id": "pasient"},
        drop_columns=[],
    )
    
    clean_df = viz.load_data(df)
    fig, ax = viz.plot_patient_timeline(
        clean_df,
        cluster_col="cluster",
        annotation_cols=["diagnosis"],
        xlim=(0, 60),
        save_path="example_plot.png"
    )
    plt.show()
    """

    def __init__(
        self,
        selected_columns=None,
        rename_dict=None,
        drop_columns=None,
    ):
        """
        Parameters
        ----------
        selected_columns : list of str, optional
            Columns to keep from the original DataFrame. If None, keep all columns.
        rename_dict : dict, optional
            A dictionary mapping {old_name: new_name} for renaming columns.
        drop_columns : list of str, optional
            Columns to drop from the DataFrame (after selecting and renaming).
        """
        self.selected_columns = selected_columns
        self.rename_dict = rename_dict
        self.drop_columns = drop_columns

    def load_data(self, df):
        """
        Load and transform patient data.
        
        Steps:
        1. Optionally select specific columns (if selected_columns is provided).
        2. Optionally rename columns based on rename_dict.
        3. Optionally drop columns in drop_columns.
        4. Convert 'episode_start_date' and 'episode_end_date' columns to datetime if they exist.
        5. Sort by 'episode_start_date' if it exists.
        
        Parameters
        ----------
        df : pandas.DataFrame
            Original DataFrame containing patient data.
        
        Returns
        -------
        pandas.DataFrame
            A cleaned/processed DataFrame ready for plotting.
        """
        # Make a copy so we don't alter the original DataFrame
        df = df.copy()

        # 1. Select columns
        if self.selected_columns is not None:
            df = df[self.selected_columns]

        # 2. Rename columns
        if self.rename_dict is not None:
            df = df.rename(columns=self.rename_dict)

        # 3. Drop unwanted columns
        if self.drop_columns is not None:
            df = df.drop(columns=self.drop_columns, errors="ignore")

        # 4. Convert date columns to datetime if they exist
        for date_col in ["episode_start_date", "episode_end_date"]:
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

        # 5. Sort by episode_start_date if available
        if "episode_start_date" in df.columns:
            df = df.sort_values(by="episode_start_date")

        return df

    def plot_patient_timeline(
        self,
        df,
        pasient_col="pasient",
        age_col="age",
        cluster_col="cluster",
        annotation_cols=None,
        cluster_colors=None,
        xlim=(0, 100),
        figsize=(12, 5),
        dpi=100,
        save_path=None,
    ):
        """
        Plot a timeline of patient trajectories by age (or a user-selected numeric column).
        
        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame returned by load_data().
        pasient_col : str, optional
            The column name identifying patients. Default is "pasient".
        age_col : str, optional
            The column name containing the numeric value for the start of the episode. Default is "age".
        cluster_col : str, optional
            The column name used to color-code the episodes (integer-based). Default is "cluster".
        annotation_cols : list of str, optional
            A list of column names to annotate on each timeline segment.
            Each segment will show these columns' values (if not NaN).
        cluster_colors : list of str, optional
            A list of colors for cluster indices (1-based). If None, a default palette is used.
        xlim : tuple, optional
            (min, max) for the X-axis. Default is (0, 100).
        figsize : tuple, optional
            The size of the figure in inches. Default is (12, 5).
        dpi : int, optional
            Resolution of the figure in dots per inch. Default is 100.
        save_path : str, optional
            File path to save the figure. If None, the figure is not saved.
        
        Returns
        -------
        (matplotlib.figure.Figure, matplotlib.axes._axes.Axes)
            The created figure and axes objects.
        
        Notes
        -----
        - If `episode_end_date` and `episode_start_date` columns exist, the end
          age is computed as: start_age + (end_date - start_date in days)/365.2425.
          If either date is missing, we default to the start_age for both ends.
        - Missing cluster or annotation values are handled gracefully; e.g., if
          cluster is NaN, a default color of 'gray' is used.
        """
        # Check if the DataFrame has the required columns
        if pasient_col not in df.columns:
            raise KeyError(f"DataFrame must contain a '{pasient_col}' column.")
        if age_col not in df.columns:
            raise KeyError(f"DataFrame must contain a '{age_col}' column.")

        if cluster_colors is None:
            # Some default colors for clusters 1..n
            cluster_colors = ["red", "green", "blue", "orange", "purple", "brown", "cyan"]

        if annotation_cols is None:
            annotation_cols = []

        unique_patients = df[pasient_col].unique()
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)

        for i, patient_id in enumerate(unique_patients):
            # Subset for one patient
            patient_data = df[df[pasient_col] == patient_id]

            for _, row in patient_data.iterrows():
                start_val = row[age_col]

                # If the row has date columns, attempt to compute an end_val
                if "episode_end_date" in row and "episode_start_date" in row:
                    if pd.notnull(row["episode_end_date"]) and pd.notnull(row["episode_start_date"]):
                        duration_days = (row["episode_end_date"] - row["episode_start_date"]).days
                        end_val = start_val + duration_days / 365.2425
                    else:
                        end_val = start_val
                else:
                    end_val = start_val

                # Determine color based on cluster
                if cluster_col in row and pd.notnull(row[cluster_col]):
                    # Convert cluster to an int, then index into cluster_colors
                    cluster_idx = int(row[cluster_col]) - 1
                    if 0 <= cluster_idx < len(cluster_colors):
                        color = cluster_colors[cluster_idx]
                    else:
                        color = "gray"
                else:
                    color = "gray"

                # Plot the line segment
                ax.plot([start_val, end_val], [i, i], linewidth=5, color=color)

                # Build annotation text from annotation_cols
                annotation_parts = []
                for col in annotation_cols:
                    if col in row and pd.notnull(row[col]):
                        annotation_parts.append(f"{col}: {row[col]}")
                annotation_text = "; ".join(annotation_parts)

                # If there's something to annotate, place text near the start
                if annotation_text:
                    ax.annotate(
                        annotation_text,
                        (start_val, i),
                        xytext=(5, 5),
                        textcoords="offset points",
                        ha="left",
                        va="bottom",
                        fontsize=8,
                        bbox=dict(
                            boxstyle="round,pad=0.3",
                            edgecolor="grey",
                            linewidth=0.5,
                            facecolor="white",
                            alpha=0.7
                        ),
                    )

        ax.set_yticks(range(len(unique_patients)))
        ax.set_yticklabels(unique_patients)
        ax.set_xlim(xlim)
        ax.set_xlabel(age_col.capitalize())
        ax.set_ylabel(pasient_col.capitalize())
        ax.grid(True, linewidth=0.5, alpha=0.3)

        fig.tight_layout()

        # Optionally save the figure
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")

        return fig, ax
