import sys
import argparse
import tenxutil

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix,accuracy_score
from scipy.spatial.distance import correlation # 1 - pearson correlation


def learn_and_print(data_file, cv, keep_genes, out_stream):
    x,y,all_genes,names,types = tenxutil.load_10x_data(data_file)
    out_stream.write('finished loading data...\n')
    # log normalize the data
    x = tenxutil.log_normalize_10x_counts(x)
    out_stream.write('finished normalizing...\n')
    # add an epsilon so Pearson correlation doesn't have 0 denominator
    x += 0.01
    # filter down to the keep genes
    # filter after normalize because we likely will end up with 0 vectors
    if keep_genes is not None:
        x,all_genes = tenxutil.get_gene_set_submatrix(x, all_genes, keep_genes)
    # do no preprocessing and do 5-fold CV
    clf = KNeighborsClassifier(n_neighbors=1, metric=correlation, n_jobs=10)
    cv_results = cross_val_predict(clf, x, y, cv=cv)
    out_stream.write('finished training/testing...\n')
    # now get the confusion matrix and accuracy
    cv_confmat = confusion_matrix(y, cv_results)
    cv_acc = accuracy_score(y, cv_results)
    # print them out
    out_stream.write('confusion matrix:\n')
    out_stream.write(','.join(types) + '\n')
    for r in cv_confmat:
        out_stream.write(','.join([str(v) for v in r]) + '\n')
    out_stream.write('accuracy:\n')
    out_stream.write(str(cv_acc) + '\n')

def build_arg_parser():
    parser = argparse.ArgumentParser(
        description='1-nearest-neighbor predictions for cell type.')
    parser.add_argument(
        'count_file',
        help='the data file to work on')
    parser.add_argument(
        '-g', '--genes',
        help='gene file (one per line) of genes to keep for analysis')
    parser.add_argument(
        '-f', '--folds',
        help='fold file to use for cross-validation (default: 5 random)')
    parser.add_argument(
        '-o', '--out',
        help='out file to store results (default: stdout)')
    return parser

def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    # CL args
    DATAFILE = args.count_file
    GENEFILE = args.genes
    FOLDFILE = args.folds
    OUTFILE = args.out
    # read the folds in (default to 5 random folds)
    cv = 5
    if FOLDFILE is not None:
        cv = tenxutil.load_10x_folds(FOLDFILE)
    # read in the genes to keep
    keep_genes = None
    if GENEFILE is not None:
        with open(GENEFILE) as infile:
            keep_genes = [l.strip() for l in infile]
    # point our output to a file or stdout
    outf = sys.stdout
    if OUTFILE is not None:
        outf = open(OUTFILE, 'w')
    # now do the actual learning
    learn_and_print(DATAFILE, cv, keep_genes, outf)
    # done, close the outfile if we opened one
    if OUTFILE is not None:
        outf.close()

if __name__ == '__main__':
    main()
