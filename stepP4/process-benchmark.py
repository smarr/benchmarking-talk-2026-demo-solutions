# dependencies: python3.14 -m pip install matplotlib pandas git+https://github.com/JasonGross/tikzplotlib.git
# delete ~/.matplotlib/fontlist* if fonts are not found
import pandas as pd
from diagram import plot_change, plot_iteration_time
from download import download_to_cache
from latex import write_macro

# Step 3: basic details
PROJECT_NAME = "PlissDemo"
BASELINE_DATA_ID = "5843"
CHANGE_DATA_ID = "5844"

# Step 3: download data files
baseline_file_path = download_to_cache(BASELINE_DATA_ID, PROJECT_NAME)
change_file_path = download_to_cache(CHANGE_DATA_ID, PROJECT_NAME)

# Step 3: Read the CSV file
# columns: expid,runid,trialid,commitid,bench,exe,suite,cmdline,varvalue,cores,
#          inputsize,extraargs,invocation,warmup,criterion,unit,value,iteration,
#          envid
baseline_df = pd.read_csv(baseline_file_path)
change_df = pd.read_csv(change_file_path)

print(baseline_df.describe(include="all"))

# Step 4: per bench, calculate the median value of the baseline data set and normalize all values to the median
baseline_medians = baseline_df.groupby("bench")["value"].median()
baseline_df["normalized_value"] = baseline_df.apply(
    lambda row: row["value"] / baseline_medians[row["bench"]], axis=1
)
change_df["normalized_value"] = change_df.apply(
    lambda row: row["value"] / baseline_medians[row["bench"]], axis=1
)

# Step 4: create a plot that shows difference to baseline
plot_change(change_df, "change-boxplot.pdf")

# Step 7: calculate stats for use in paper



# Step 9: iteration time plots
