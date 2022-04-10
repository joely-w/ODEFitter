# ODEFitter

Framework created for approximating parameters in compartmental models for given dataset using curve fitting. Currently,
the only model that is implemented is the SIR model.

# Installation

Install required modules with `pip install -r requirements.txt`.

# Usage

## SIR Models

The SIR modelling is currently done in `main.py`, to use it you will need a CSV dataset of cases in the following
format:

```
<population at start>
<daily births at start>
<daily deaths at start>
<time index>, <cumulative cases>
....
```

Time index needs to start at 0, which would represent the first day of the recorded disease.
To use, change the filename at the bottom of the code to point towards your CSV file and run.
