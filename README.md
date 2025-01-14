A Python package to load, transform, and visualize patient trajectories for one or many patients.  
It handles missing values gracefully, allows you to rename or drop columns,  
and lets you annotate the plotted trajectories with any additional fields.

## Installation

```bash
pip install patient_trajectory
```

## Usage Example

```

import pandas as pd
import numpy as np
from patient_trajectory import plot_patient_gantt
import matplotlib.pyplot as plt

# Example data
data = {
    "pasient": [
        1, 1, 1, 2, 2, 3, 4, 4, 5, 6,
        7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
        17, 18, 19, 20, 21
    ],
    "episode_start_date": [
        "2001-01-01", "2002-03-20", "2003-10-05", "2005-05-01", "2005-06-15",
        "2010-01-01", "2018-08-20", "2019-02-02", "2020-01-01", "2020-05-15",
        "2021-07-10", "2021-12-01", "2022-03-14", "2023-01-01", "2023-04-10",
        "2023-06-15", "2023-08-01", "2023-09-12", "2024-01-01", "2024-03-15",
        "2025-01-01", "2025-02-15", "2025-03-20", "2025-05-10", "2025-07-01"
    ],
    "episode_end_date": [
        "2001-02-15", "2002-06-01", "2004-01-10", "2005-05-10", None,
        "2010-01-05", "2019-01-01", None, "2020-02-01", "2020-06-01",
        None, "2022-01-10", "2022-04-01", "2023-02-15", "2023-05-05",
        None, "2023-08-20", None, "2024-02-01", None,
        "2025-01-10", None, "2025-04-01", None, None
    ],
    "age": [
        10, 11, 12, 35, 36,
        75, 5, 6, 45, 30,
        25, 28, 33, 20, 22,
        18, 40, 50, 60, 65,
        27, 55, 78, 42, 24
    ],
    "cluster": [
        1, np.nan, 2, 2, 3,
        3, 1, np.nan, 5, 5,
        np.nan, 5, 2, 6, np.nan,
        6, 4, 3, 4, np.nan,
        3, 1, 5, 2, 4
    ],
    "diagnosis": [
        None, "Flu", "Migraine", "COVID", None,
        "Cold", "Broken Bone", "Follow-up", "Diabetes", "Asthma",
        "Hypertension", "Obesity", "Depression", "Anxiety", None,
        "Migraine", "Arthritis", "Pneumonia", "Stroke", None,
        "Allergy", "Hypertension", "Cold", "COVID", "Broken Bone"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Visualizing patient trajectories
fig, ax = plot_patient_gantt(
    df=df,
    pasient_col="pasient",
    cluster_col="cluster",
    start_date_col="episode_start_date",
    end_date_col="episode_end_date",
    annotation_cols=["diagnosis"],  # Add diagnosis as annotations
    figsize=(12, 6),
    dpi=120,
    row_height=0.7,
    row_gap=0.3,
    annotation_fontsize=8,
    axis_fontsize=10,
    title_fontsize=14,
    add_cluster_legend=True,
    curve_color="blue",
    curve_linestyle="--",
    curve_linewidth=1.5,
    save_path=None  # Change to a path if saving the plot
)

plt.show()

```

## Citation

If you use this work, please cite:

```bibtex
@inproceedings{Pant2024,
  author    = {Pant, D. and Koochakpour, K. and Westbye, O. S. and Clausen, C. and Leventhal, B. L. and Koposov, R. and Rost, T. B. and Skokauskas, N. and Nytro, O.},
  title     = {Visualizing Patient Trajectories and Disorder Co-occurrences in Child and Adolescent Mental Health},
  booktitle = {2024 IEEE International Conference on Bioinformatics and Biomedicine (BIBM)},
  publisher = {IEEE Computer Society},
  pages     = {5531--5538},
  year      = {2024},
  month     = {Dec 1}
}
```
