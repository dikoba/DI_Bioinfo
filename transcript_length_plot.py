import sys
import argparse
from collections import defaultdict
from GC_bioinfo.utils.verify_bed_file import verify_bed_files


def main(args):
    filenames, maximum_transcript_length = parse_args(args)

    # create a dict that will contain each dataset filename as the key and a dictionary containing the dataset's
    # transcript length and number of transcripts as the value
    all_datasets_dict = dict()

    # get the name of each regions file for a dataset
    for file in filenames:
        # add the transcript length dictionary from the function to the all datasets dictionary
        all_datasets_dict[file] = get_transcript_length(file)

    output_data(all_datasets_dict, maximum_transcript_length)


def output_data(all_datasets_dict, max_tl):
    print('\t'.join(['Transcript Length'] + list(all_datasets_dict.keys())))
    # print out a line of data with the transcript length, and the number of transcripts for each dataset
    for position in range(max_tl+1):
        print('\t'.join([str(position)] + [str(all_datasets_dict[dataset][position]) for dataset in all_datasets_dict]))


# function gets the transcript length of each region in a regions file and returns a dictionary containing a specific
# transcript length as the key and the number of transcripts at that length as the value
def get_transcript_length(filename):
    # create dictionary for current dataset to hold transcript length as key and number of transcripts as value
    tl_dict = defaultdict(int)

    # open regions file and loop through each line and get transcript length of each region
    verify_bed_files(filename)
    with open(filename, 'r') as file:
        for line in file:
            chrom, left, right, name, score, strand = line.split()
            right = int(right)
            left = int(left)

            if right > left:
                transcript_length = right - left
            else:
                raise Exception('Improper .bed file format in: ' + filename)

            # add one to the number of transcripts
            tl_dict[transcript_length] += 1

    return tl_dict


def parse_args(args):
    parser = argparse.ArgumentParser(description= 'Takes one or more .bed files and an optional maximum transcript ' +
                                                  'length value and returns the number of transcripts at each '
                                                  'transcript length from 17 bp to the max length (600 bp by default).')

    parser.add_argument('bedfiles', metavar='bedfiles', type=str, nargs='+', help='must be a .bed file')
    parser.add_argument('-m', '--maxlength', dest='max_transcript_length', metavar='max_transcript_length', type=int, nargs='?',
                        default=600)
    args = parser.parse_args(args)

    filenames = args.bedfiles
    verify_bed_files(filenames)

    if args.max_transcript_length:
        max_tl = args.max_transcript_length

    return filenames, max_tl

if __name__ == '__main__':
    main(sys.argv[1:])
