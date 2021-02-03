import io
import unittest.mock
import transcript_length_plot


class TestTranscriptLengthPlot(unittest.TestCase):
    # notes:
    # main program takes in arguments with command line
    # get_transcript_length program requires proper bed file format and raises exception when that is not given

    no_args = []
    single_arg = ['bedfile1.bed']
    multiple_args = ['bedfile1.bed', 'bedfile2.bed', 'bedfile3.bed']
    bad_bedfile = ['bad_bedfile.bed']

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_single_read(self, std_output):
        transcript_length_plot.main(self.single_arg)
        result = std_output.getvalue()

        for line in result.split('\n')[1:]:
            if line:
                length, num_transcripts = line.split()
                if length == '10':
                    self.assertEqual(num_transcripts, '1')
                else:
                    self.assertEqual(num_transcripts, '0')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_multiple_reads(self, std_output):
        transcript_length_plot.main(self.multiple_args)
        result = std_output.getvalue()

        for line in result.split('\n')[1:]:
            if line:
                length, num_transcripts1, num_transcripts2, num_transcripts3 = line.split()
                if length == '10':
                    self.assertEqual(num_transcripts1, '1')
                    self.assertEqual(num_transcripts2, '0')
                    self.assertEqual(num_transcripts3, '0')

                elif length == '20':
                    self.assertEqual(num_transcripts1, '0')
                    self.assertEqual(num_transcripts2, '5')
                    self.assertEqual(num_transcripts3, '0')

                elif length == '30':
                    self.assertEqual(num_transcripts1, '0')
                    self.assertEqual(num_transcripts2, '0')
                    self.assertEqual(num_transcripts3, '10')

                else:
                    self.assertEqual(num_transcripts1, '0')
                    self.assertEqual(num_transcripts2, '0')
                    self.assertEqual(num_transcripts3, '0')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_improper_bedfile(self, std_output):
        with self.assertRaises(Exception):
            transcript_length_plot.main(self.bad_bedfile)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_no_args(self, std_output):
        with self.assertRaises(SystemExit):
            transcript_length_plot.main(self.no_args)


if __name__ == "__main__":
    unittest.main()
