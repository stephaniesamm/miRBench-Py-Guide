# README

## miRBench
miRBench is a python package developed for facilitating benchmarking in the field of miRNA binding site prediction based on sequence, by providing access to state-of-the-art models and other simpler methods, as well as to various testing and training datasets available for download. 

The GitHub repository for this python package is available at https://github.com/katarinagresova/miRBench. 

## Getting started

### Setting up your environment
Create and activate a conda environment. 

### Installing miRBench
At the moment, the latest version of miRBench is on GitHub but not on Pypi. 

For now please use `pip install git+https://github.com/katarinagresova/miRBench.git` to install the package. 

## Resources

### Exploring miRBench
The Jupyter notebook `mirbench_guide.ipynb` will guide you to explore the functions in the miRBench package. 

### Getting predictions
The Python script `benchmark.py` by default gets you predictions from all tools on all test datasets (all ratios) and outputs in your current directory. 

From the command line, run:

`python benchmark_script.py [--out_dir OUT_DIR] [--predictors PREDICTOR [PREDICTOR ...]] [--datasets DATASET [DATASET ...]] [--ratios RATIO [RATIO ...]]`

#### Arguments
`--out_dir`: Output directory for predictions (default: current directory)
`--predictors`: List of predictors to benchmark (default: all available in miRBench)
`--datasets`: List of datasets to benchmark (default: all available in miRBench)
`--ratios`: List of ratios to benchmark (default: ["1", "10", "100"])

#### Output
The script generates TSV files with predictions for each dataset and ratio combination. The output files are named in the format: `{dataset}_{ratio}_predictions.tsv`. 

## Author
Stephanie Sammut (stephanie.sammut@um.edu.mt)

## Date
11-Sep-2024
