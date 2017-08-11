import unittest
import random

def sort_segments(input_numbers, params):
    dataset_size = params['dataset_size']
    segment_size = params['segment_size']
    segment_count = dataset_size // segment_size
    for i in xrange(segment_count):
        l = input_numbers[i * segment_size : (i + 1) * segment_size]
        l.sort()
        input_numbers[i * segment_size : (i + 1) * segment_size] = l

def merge(input_numbers, output_numbers, params):
    dataset_size = params['dataset_size']
    segment_size = params['segment_size']
    segment_count = dataset_size // segment_size
    chunk_size = params['chunk_size']

    # Init memory
    memory = []
    for i in xrange(segment_count):
        segment_start = i * segment_size
        memory += input_numbers[segment_start : segment_start + chunk_size]
    memory += [0 for i in xrange(segment_count * chunk_size)]
    chunk_offsets = [0 for i in xrange(segment_count)]
    chunk_indexes = [0 for i in xrange(segment_count)]

    # while all the segments are not emptied of their content
    while any(chunk_indexes[s] < chunk_size for s in xrange(segment_count)):
        # find a non-empty segment
        segment = next(s for s in xrange(segment_count) if chunk_indexes[s] < chunk_size)
        # find the non-empty segment with the smallest element
        for i in xrange(segment + 1, segment_count):
            if chunk_indexes[i] < chunk_size:
                if memory[chunk_size * segment + chunk_indexes[segment]] >= memory[chunk_size * i + chunk_indexes[i]]:
                    segment = i

        output_numbers.append(memory[chunk_size * segment + chunk_indexes[segment]])
        chunk_indexes[segment] += 1

def external_sort(input_numbers, output_numbers, params):
    sort_segments(input_numbers, params)
    merge(input_numbers, output_numbers, params)
    return output_numbers

class TestExternalSort(unittest.TestCase):

    def test_merge_1(self):
        output_numbers = []
        merge([2, 4, 1, 3], output_numbers, {'dataset_size': 4,
                                            'segment_size': 2,
                                            'chunk_size': 2})
        self.assertEqual([1, 2, 3, 4], output_numbers)

    def test_merge_2(self):
        output_numbers = []
        merge([2, 3, 1, 4], output_numbers, {'dataset_size': 4,
                                            'segment_size': 2,
                                            'chunk_size': 2})
        self.assertEqual([1, 2, 3, 4], output_numbers)

    def test_acceptance(self):
        dataset_size = 1000000
        segment_size = 100000
        input_numbers = [random.randrange(0, 65536) for i in xrange(dataset_size)]
        output_numbers = []

        external_sort(input_numbers, output_numbers, {
            'dataset_size': dataset_size,
            'segment_size': 100000,
            'chunk_size': 5000
        })

        for i in xrange(len(output_numbers) - 1):
            self.assertTrue(output_numbers[i] <= output_numbers[i + 1])
        self.assertEqual(len(output_numbers), len(input_numbers))

        sum_input  = reduce(lambda x, y: x ^ y, input_numbers, 0)
        sum_output = reduce(lambda x, y: x ^ y, output_numbers, 0)
        self.assertEqual(sum_output, sum_input)


if __name__ == '__main__':
    unittest.main()
