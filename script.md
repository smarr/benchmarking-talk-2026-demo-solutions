# Benchmarking: Walk Through

----

## Part 1: Experiments

### StepE1: Create The Research Repo

```
mkdir GreatOpt
cd GreatOpt
git init .
git remote add gitlab git@gitlab.com:smarr/pliss-demo.git
```

Add the basic experimental setup:

```
cp ~/Talk/d/stepE1/.gitlab-ci.yml .
cp ~/Talk/d/stepE1/rebench.conf .
code .
```

**commit and push**

```
t
git push --force gitlab main
```


---

### StepE2: Add Benchmarks and Add Config

```
git subtree add --prefix awfy https://github.com/smarr/are-we-fast-yet master --squash -m "Add the AWFY benchmarks in the latest version of today"
```

in `rebench.conf` add executor:

```
executors:
  java:
    executable: java
```

add experiments:

```
experiments:
  java:
    suites: [awfy-java]
    executions: [java]
```

---

### StepE3: Setup First Benchmark Runs

Run the benchmarks locally:

`rebench rebench.conf`

**commit and push**

Look at CI running at https://gitlab.com/smarr/pliss-demo

---

### StepE4: Create Baseline Branch


```
t   # and do it visually
git switch -c baseline
```

---

### StepE5: Optimize 

```
t   # and do it visually
git switch -c opt
code awfy/benchmarks/Java
```

open `Sieve.java`

<span style="color:#66356E;font-weight:bold;">✋ What's could we possibly optimize in a classic Sieve of Eratosthenes, i.e., to find prime numbers? ✋</span>


 - change loop boundary, starting at 3
 - change loop increment: `i += 2`
 - **commit and push**
 - inspect the GitLab CI to see whether it's running and succeeding https://gitlab.com/smarr/pliss-demo/-/jobs
 - it should break...

### StepE6: Fix Optimization

 - fix the primeCount, start at 1
 - **commit and push**
 - inspect GitLab https://gitlab.com/smarr/pliss-demo/-/jobs
 - should be fixed, and we should get results
 - run locally for good measures `rebench -c rebench.conf`

also open https://rebench.dev

## Part 2: Write Our Paper

### Step P1: Create Paper

```
cd workspace
mkdir paper
cd paper
~/Talks/d/stepP1/acmart-init.sh
git init .
code .
```
---

### Step P2: Automate

```
cp ~/Talks/d/stepP2/.gitlab-ci.yml .
~/Talks/d/stepP2/rebench-plot-code.sh
code .
```

- commit and publish

---

### Step P3: Process the Data

 - Need data from ReBenchDB
   - PROJECT_NAME="PlissDemo"
   - look up the baseline and change data ids `BASELINE_DATA_ID`, `CHANGE_DATA_ID`
   - baseline_file_path = download_to_cache(BASELINE_DATA_ID, PROJECT_NAME)
   - change_file_path = download_to_cache(CHANGE_DATA_ID, PROJECT_NAME)
   - baseline_df = pd.read_csv(baseline_file_path)
   - change_df = pd.read_csv(change_file_path)
   - print(baseline_df.describe(include="all"))

---

### Step P4: Normalize data

```
baseline_medians = baseline_df.groupby("bench")["value"].median()
baseline_df["normalized_value"] = baseline_df.apply(
    lambda row: row["value"] / baseline_medians[row["bench"]], axis=1
)
change_df["normalized_value"] = change_df.apply(
    lambda row: row["value"] / baseline_medians[row["bench"]], axis=1
)
```

And finally:
 - `plot_change(change_df, "change-boxplot.pdf")`

---
### Step P5: Setup "Paper Run"

<span style="color:red;">⚠ switch to baseline branch</span>


add experiment: `exp/rebench.conf`

```
  java-paper:
    iterations: 250!
    invocations: 5
    suites: [awfy-java]
    executions: [java]
```

`exp/.gitlab-ci.yml`

 - add experiment name: `rebench` ... `java-paper`

Commit and push.

<span style="color:red;">⚠ switch to opt branch</span>

add experiment: `exp/rebench.conf`

```
  java-paper:
    iterations: 250!
    invocations: 5
    suites: [awfy-java]
    executions: [java]
```

`exp/.gitlab-ci.yml`

 - add experiment name: `rebench` ... `java-paper`

commit and push.


---

### Step P6: Write first part of paper 

```
\section{Evaluation}

\begin{figure}[h]
  \centering
  \includegraphics{experiments/change-boxplot.pdf}
  \Description{}
  \caption{A box plot showing the run time of Sieve}
  \label{fig:change}
\end{figure}
```

<span style="color:#66356E;font-weight:bold;">✋ What's wrong with this caption? ✋</span>


Now, the caption:

```
\caption{A box plot of run time of Sieve
  with our novel algorithm.
  After our improvements,
  it takes in the median only \sieveMedian
  (min.\ \sieveMin, max.\ \sieveMax) of the run time.}
```


---

### Step P7: Get Summary Stats

```
normalized_vals = change_df.loc[change_df["bench"] == "Sieve", "normalized_value"]
sieve_median_norm = normalized_vals.median()
sieve_min_norm = normalized_vals.min()
sieve_max_norm = normalized_vals.max()

with open("results.tex", "w") as f:
    write_macro("sieveMedian", sieve_median_norm, f)
    write_macro("sieveMin", sieve_min_norm, f)
    write_macro("sieveMax", sieve_max_norm, f)
print("Saved results to results.tex")
```

- run `python3 process-benchmark.py`

- commit `experiments/results.tex`

- add `\input{experiments/results.tex}` to Eval Sec. in tex

- build pdf

---

### Step P8: Let's Analyze The Data We Have

Go to https://rebench.dev/PlissDemo

select last base and opt

We see about 40% time reduction.
Great.

But what else do we see?

- number of measurements
- command line
- machine it was on
- history (probably nothing really to see here)
- iteration behavior

---

### Step P9: Let's add this to the paper

Start: `process-benchmark.py`

```
plot_iteration_time(baseline_df, "baseline-iteration-time.pdf", "Sieve")
plot_iteration_time(change_df, "change-iteration-time.pdf", "Sieve")
```

Latex: `paper.tex`

```
\begin{figure}[h]
  \centering
  \includegraphics{experiments/change-iteration-time.pdf}
  \Description{}
  \caption{A dot plot of the iteration time of Sieve with our novel algorithm.
  Dots are grouped by the iteration the belong to.}
  \label{fig:change-iteration-time}
\end{figure}

\begin{figure}[h]
  \centering
  \includegraphics{experiments/baseline-iteration-time.pdf}
  \Description{}
  \caption{A dot plot of the iteration time of Sieve with the classic algorithm.
  Dots are grouped by the iteration the belong to.}
  \label{fig:baseline-iteration-time}
\end{figure}
```

---

### Step P10: Let's see whether our experiments are finished...

Go to: https://gitlab.com/smarr/pliss-demo/-/jobs

Looks like they are done: https://rebench.dev/PlissDemo/data/

Update:

```
BASELINE_DATA_ID = ""
CHANGE_DATA_ID = ""
```

