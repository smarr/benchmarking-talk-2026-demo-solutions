# dependencies: python3.14 -m pip install matplotlib pandas git+https://github.com/JasonGross/tikzplotlib.git
# delete ~/.matplotlib/fontlist* if fonts are not found
import pandas as pd
from diagram import plot_change, plot_iteration_time
from download import download_to_cache
from latex import write_macro

# Step 3: basic details
PROJECT_NAME = ""
BASELINE_DATA_ID = ""
CHANGE_DATA_ID = ""

# Step 3: download data files



# Step 3: Read the CSV file
# columns: expid,runid,trialid,commitid,bench,exe,suite,cmdline,varvalue,cores,
#          inputsize,extraargs,invocation,warmup,criterion,unit,value,iteration,
#          envid



# Step 4: per bench, calculate the median value of the baseline data set and normalize all values to the median




# Step 4: create a plot that shows difference to baseline




# Step 7: calculate stats for use in paper



# Step 9: iteration time plots
