import miRBench
import pandas as pd
import argparse
import os

def yield_blocks(file_path, block_size):
    """
    Yield df-blocks of data from a file, with each block containing block_size rows (or less).
    """
    with open(file_path, 'r') as file:
        # Read the first line as the header
        header = file.readline().strip().split('\t')
        block = []
        # Read from the second line onwards
        for line in file: 
            row = line.strip().split('\t')
            block.append(row)
            if len(block) == block_size:
                yield pd.DataFrame(block, columns=header)
                block = []
        if block:
            yield pd.DataFrame(block, columns=header)


def benchmark(predictors, block, dset, ratio):
    """
    Benchmark predictors on a block of data.
    """
    for pred_name in predictors:
        print(f"Running {pred_name} on {dset} dataset, ratio {ratio}")           
        encoder = miRBench.encoder.get_encoder(pred_name)
        predictor = miRBench.predictor.get_predictor(pred_name)
        input = encoder(block)
        output = predictor(input)
        block[pred_name] = output
    return block


def main():
    parser = argparse.ArgumentParser(description="Benchmark predictors on datasets.")

    parser.add_argument("--out_dir", type=str, default=".", help="Output directory for predictions.")
    parser.add_argument("--predictors", type=str, nargs='+', default=None, help="List of predictors to benchmark.")
    parser.add_argument("--datasets", type=str, nargs='+', default=None, help="List of datasets to benchmark.")
    parser.add_argument("--ratios", type=str, nargs='+', default=None, help="List of ratios to benchmark.")

    args = parser.parse_args()

    if args.predictors is None:
        predictors = miRBench.predictor.list_predictors()
    else:
        predictors = args.predictors

    if args.datasets is None:
        datasets = miRBench.dataset.list_datasets()
    else:
        datasets = args.datasets

    if args.ratios is None:
        ratios = ["1", "10", "100"]
    else:
        ratios = args.ratios

    split = "test"

    block_size = 339066
    # Note: 339066 is the number of examples in AGO2_eCLIP_Manakov2022_1_test_dataset.tsv, to be processed in one batch.
    #       AGO2_eCLIP_Manakov2022_10_test_dataset.tsv and AGO2_eCLIP_Manakov2022_100_test_dataset.tsv need to be processed in multiple batches. 

    for dset in datasets:
        for ratio in ratios:
            print(f"Downloading {dset} dataset, ratio {ratio}")

            input_file = miRBench.dataset.get_dataset_path(dset, split=split, ratio=ratio)
            output_file = os.path.join(args.out_dir, f"{dset}_{ratio}_predictions.tsv")

            header_written = False

            for block in yield_blocks(input_file, block_size): 
                block_preds = benchmark(predictors, block, dset, ratio)

                if not header_written:
                    block_preds.to_csv(output_file, sep='\t', index=False, mode='w')
                    header_written = True
                else:
                    block_preds.to_csv(output_file, sep='\t', index=False, mode='a', header=False)

            print(f"Predictions for {dset} dataset, ratio {ratio}, written to {output_file}")

    print(f"Predictions for all datasets written to output directory.")

if __name__ == "__main__":
    main()