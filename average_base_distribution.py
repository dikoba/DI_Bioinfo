def main():
    import sys
    import pybedtools

    # open regions file and get number of regions
    try:
        regions_file = open(sys.argv[1], 'r')
        regions_count = 0
        for region in regions_file.read().splitlines():
            if region.strip():
                regions_count += 1
        regions_file.close()

    # raise error if proper regions file argument is not given
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <region_filename.bed> <fasta_filename.fa>")

    # read regions file and pass into pybedtools 'getfasta' wrapper along with fasta filename
    # kept getting errors when I tried to read the regions_file a second time, so I had to close and open file again
    regions = open(sys.argv[1], 'r')
    fasta = sys.argv[2]
    regions_bedtool = pybedtools.BedTool(regions.read(), from_string=True)
    get_fasta = regions_bedtool.sequence(fi=fasta)
    fasta_sequence = open(get_fasta.seqfn).read().splitlines()
    regions.close()

    dna_list = []
    sequence_length = []

    for i in range(0, len(fasta_sequence), 2):
        # get current fasta sequence and add to list
        curr_sequence = fasta_sequence[i+1].upper()
        sequence_length.append(len(curr_sequence))
        dna_list.append(curr_sequence)

    # get base frequencies
    base_frequencies = create_frequency_matrix(dna_list, regions_count, sequence_length[0])

    # print header then base distribution
    print('\t'.join(['Position', 'A', 'T', 'G', 'C']))
    base_distribution(base_frequencies, sequence_length[0])

    return None


# function prints out position of base followed by 'ATGC' frequencies
def base_distribution(base_frequency_matrix, seq_length):
    # go through matrix and print out the distribution at each dna sequence position
    for pos in range(seq_length):
        # specify current bp position (start position at around -0.5*seq_length)
        # this may change with different sequences so ask Geoff later about it
        if pos < int(.5*seq_length):
            position = pos - int(.5*seq_length)
        else:
            position = pos - int(.5*seq_length) + 1

        # add position to data table
        distribution_data = [position]

        # cycle through 'ATGC', get frequency, and put into a list
        for nuc in range(4):
            distribution_data += [base_frequency_matrix[nuc][pos]]

        # print base distribution at current position
        print('\t'.join([str(x) for x in distribution_data]))

    return None


# function from: https://hplgit.github.io/bioinf-py/doc/pub/html/main_bioinf.html
def create_frequency_matrix(dna_sequences, num_regions, seq_length):
    # Create empty frequency_matrix[i][j] = 0
    # i=0,1,2,3 corresponds to A,T,G,C
    # j=0,..., sequence length

    frequency_matrix = [[0 for s in range(seq_length)] for t in 'ATGC']
    base2index = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
    for dna in dna_sequences:
        for index, base in enumerate(dna):
            frequency_matrix[base2index[base]][index] += 1/num_regions
    return frequency_matrix


if __name__ == '__main__':
    main()
