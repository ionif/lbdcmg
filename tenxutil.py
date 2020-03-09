import numpy

from os.path import exists

def load_10x_data(filename):
    # expecting the path to the files with basename, but
    # the data are split into .npy, .header, and .names files
    # and someone might give us a complete path to one of those
    if filename.endswith('.npy'):
        filename = filename[:-4]
    if filename.endswith('.header'):
        filename = filename[:-7]
    if filename.endswith('.names'):
        filename = filename[:-6]
    # get the actual filenames we want
    datafile = filename + '.npy'
    headfile = filename + '.header'
    namefile = filename + '.names'
    # double check that everything is present
    all_exist = exists(datafile) and exists(headfile) and exists(namefile)
    if not all_exist:
        return None,None,None,None,None
    # read the header
    genes = None
    with open(headfile) as infile:
        genes = [l.strip() for l in infile]
    # read the sample names
    sample_names = None
    with open(namefile) as infile:
        sample_names = [l.strip() for l in infile]
    # and turn those sample names into cell types and labels
    cell_types = list()
    ct_dict = dict()
    y = list()
    for sn in sample_names:
        # sample name is like [celltype]_[count]
        ctype = sn.split('_')[0]
        # store unique cell types observed in order
        if ctype not in ct_dict:
            ct_dict[ctype] = len(cell_types)
            cell_types.append(ctype)
        # and store the integral class of this cell type
        y.append(ct_dict[ctype])
    y = numpy.array(y)
    # finally, read the actual counts
    x = numpy.load(datafile)
    # and send them home
    return x,y,genes,sample_names,cell_types


def load_10x_folds(foldfile):
    # each line is train indices followed by test indices
    # like [comma sep train indices];[comma sep test indices]
    tt_tuples = list()
    with open(foldfile) as infile:
        for l in infile:
            parts = l.strip().split(';')
            train = numpy.array([int(v) for v in parts[0].split(',')])
            test = numpy.array([int(v) for v in parts[1].split(',')])
            tt_tuples.append((train,test))
    return tt_tuples

def log_normalize_10x_counts(x):
    # first scale each row to [0.0,1.0]
    # need row sums
    row_sums = numpy.sum(x, axis=1)
    # and then divide each row by the sum (div by column vector)
    new_x = x / row_sums[:, numpy.newaxis]
    # then rescale and log
    new_x *= 10e6
    new_x = numpy.log(new_x + 1)
    return new_x


def get_gene_set_submatrix(x, all_genes, keep_genes):
    # first compute the indices to keep
    keep_genes = set(keep_genes)
    keep_inds = [i for i,g in enumerate(all_genes) if g in keep_genes]
    # keep_genes may not have been in the same order as all_genes
    # give back a new gene list in all_genes order
    new_genes = [all_genes[i] for i in keep_inds]
    # and give those columns back
    new_x = x[:,keep_inds]
    return new_x,new_genes
