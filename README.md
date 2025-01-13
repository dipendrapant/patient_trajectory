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
from patient_trajectory.visualization import PatientTrajectoryVisualizer

data = {
"my_patient": [5, 5, 5],
"episode_start_date": ["2001-01-01", "2003-05-10", "2005-01-01"],
"episode_end_date": ["2001-06-01", "2003-12-31", None],
"age": [0, 2, 4],
"cluster": [1, 1, 2],
"diagnosis": ["Allergy", None, "Cold"]
}
df = pd.DataFrame(data)

# Create a visualizer, specifying columns to keep, rename, or drop

viz = PatientTrajectoryVisualizer(
selected_columns=["my_patient", "episode_start_date", "episode_end_date", "age", "cluster", "diagnosis"],
rename_dict={"my_patient": "pasient"},
drop_columns=[]
)

clean_df = viz.load_data(df)

# Plot with 'diagnosis' as an annotation on each episode

fig, ax = viz.plot_patient_timeline(
clean_df,
pasient_col="pasient",
age_col="age",
cluster_col="cluster",
annotation_cols=["diagnosis"], # Additional fields to display
xlim=(0, 10), # Age range for the x-axis
)
fig.show()
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
