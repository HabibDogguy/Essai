import unittest
import random
from functools import reduce

def external_sort(input_numbers, output_numbers, params):
    sort_segments(input_numbers, params)
    merge(input_numbers, output_numbers, params)
    return output_numbers


def sort_segments(input_numbers, params):
    dataset_size = params['dataset_size']
    segment_size = params['segment_size']
    segment_count = dataset_size // segment_size
    for i in range(segment_count):
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
    for i in range(segment_count):
        memory += Segment(i, segment_size).from_input(input_numbers, chunk_size)
    chunk_offsets = [0 for i in range(segment_count)]
    chunk_indexes = [0 for i in range(segment_count)]

    # while all the segments are not emptied of their content
    while any(chunk_indexes[s] < chunk_size for s in range(segment_count)):
        # find a non-empty segment
        segment = next(s for s in range(segment_count) if chunk_indexes[s] < chunk_size)
        # find the non-empty segment with the smallest element
        for i in range(segment + 1, segment_count):
            if chunk_indexes[i] < chunk_size:
                if memory[chunk_size * segment + chunk_indexes[segment]] >= memory[chunk_size * i + chunk_indexes[i]]:
                    segment = i

        output_numbers.append(memory[chunk_size * segment + chunk_indexes[segment]])
        chunk_indexes[segment] += 1

        if chunk_indexes[segment] == chunk_size:
            chunk_offsets[segment] += chunk_size
            if chunk_offsets[segment] < segment_size:
                memory_chunk_start = segment * chunk_size
                input_chunk_start = segment_size * segment + chunk_offsets[segment]
                memory[memory_chunk_start : memory_chunk_start + chunk_size] = input_numbers[input_chunk_start : input_chunk_start + chunk_size]
                chunk_indexes[segment]=0

class Segment:
    def __init__(self, ident, segment_size):
        self.ident = ident
        self.segment_size = segment_size

    def start(self):
        return self.ident * self.segment_size

    def from_input(self, input_numbers, chunk_size):
        return input_numbers[self.start() : self.start() + chunk_size]

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


    def test_merge_add_data_when_chunk_exhausted(self):
        output_numbers = []
        merge([1, 2, 4, 9, 1, 2, 3, 8], output_numbers, {'dataset_size': 8,
                                            'segment_size': 4,
                                            'chunk_size': 1})
        self.assertEqual([1, 1, 2, 2, 3, 4, 8, 9], output_numbers)

    def est_acceptance(self):
        dataset_size = 1000000
        segment_size = 100000
        input_numbers = [random.randrange(0, 65536) for i in range(dataset_size)]
        output_numbers = []

        external_sort(input_numbers, output_numbers, {
            'dataset_size': dataset_size,
            'segment_size': 100000,
            'chunk_size': 5000
        })

        for i in range(len(output_numbers) - 1):
            self.assertTrue(output_numbers[i] <= output_numbers[i + 1])
        self.assertEqual(len(output_numbers), len(input_numbers))

        sum_input  = reduce(lambda x, y: x ^ y, input_numbers, 0)
        sum_output = reduce(lambda x, y: x ^ y, output_numbers, 0)
        self.assertEqual(sum_output, sum_input)


if __name__ == '__main__':
    unittest.main()
