import sys
import argparse

def filter_results(result_file, p_cutoff, out_stream):
    with open(result_file) as infile:
        # handle the header first
        header = infile.readline().strip().split(',')
        targ_ind = header.index('target')
        pval_ind = header.index('p_value')
        # go through the result lines
        for l in infile:
            parts = l.strip().split(',')
            targ = parts[targ_ind]
            pval = float(parts[pval_ind])
            if pval <= p_cutoff:
                out_stream.write(targ)
                out_stream.write('\n')

def build_arg_parser():
    parser = argparse.ArgumentParser(
        description='Filter a KinderMiner list of targets by p-value.')
    parser.add_argument(
        'result_file',
        help='the KinderMiner result file to work on')
    parser.add_argument(
        '-p', '--p_cutoff',
        type=float, default=1e-5,
        help='p-value threshold for filtering (default: 1e-5)')
    parser.add_argument(
        '-o', '--out',
        help='out file to store results (default: stdout)')
    return parser

def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    # CL args
    RESULT_FILE = args.result_file
    THRESH = args.p_cutoff
    OUT_FILE = args.out
    # open an output file if one was given
    out_stream = sys.stdout
    if OUT_FILE is not None:
        out_stream = open(OUT_FILE, 'w')
    # do the filtering
    filter_results(RESULT_FILE, THRESH, out_stream)
    # and close the output file if we opened one
    if OUT_FILE is not None:
        out_stream.close()

if __name__ == '__main__':
    main()
