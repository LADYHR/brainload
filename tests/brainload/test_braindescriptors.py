import os
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_allclose
import brainload as bl
import brainload.freesurferdata as fsd
import brainload.braindescriptors as bd


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, os.pardir, 'test_data')

# Respect the environment variable BRAINLOAD_TEST_DATA_DIR if it is set. If not, fall back to default.
TEST_DATA_DIR = os.getenv('BRAINLOAD_TEST_DATA_DIR', TEST_DATA_DIR)

def test_braindescriptors_init_nonempty():
    subjects_list = ['subject1', 'subject2']
    bdi = bd.BrainDescriptors(TEST_DATA_DIR, subjects_list)
    assert len(bdi.subjects_list) == 2
    assert len(bdi.descriptor_names) == 0
    assert bdi.descriptor_values.shape == (2, 0)


def test_braindescriptors_parcellation_stats():
    subjects_list = ['subject1', 'subject2']
    bdi = bd.BrainDescriptors(TEST_DATA_DIR, subjects_list)
    bdi.add_parcellation_stats(['aparc', 'aparc.a2009s'])
    bdi.add_segmentation_stats(['aseg'])
    bdi.add_custom_measure_stats(['aparc'], ['area'])
    bdi.add_curv_stats()
    assert len(bdi.descriptor_names) == 2873
    assert bdi.descriptor_values.shape == (2, 2873)


def test_braindescriptors_add_standard_stats():
    subjects_list = ['subject1', 'subject2']
    bdi = bd.BrainDescriptors(TEST_DATA_DIR, subjects_list)
    bdi.add_standard_stats()
    assert len(bdi.descriptor_names) == 3210
    assert bdi.descriptor_values.shape == (2, 3210)


def test_braindescriptors_standard_stats_have_unique_names():
    subjects_list = ['subject1', 'subject2']
    bdi = bd.BrainDescriptors(TEST_DATA_DIR, subjects_list)
    bdi.add_standard_stats()
    assert len(bdi.descriptor_names) == 3210
    assert bdi.descriptor_values.shape == (2, 3210)
    assert len(bdi.descriptor_names) == len(list(set(bdi.descriptor_names)))


def test_braindescriptors_file_checks():
    subjects_list = ['subject1', 'subject2']
    bdi = bd.BrainDescriptors(TEST_DATA_DIR, subjects_list)
    bdi.check_for_parcellation_stats_files(['aparc', 'aparc.a2009s'])
    bdi.check_for_segmentation_stats_files(['aseg', 'wmparc'])
    bdi.check_for_custom_measure_stats_files(['aparc'], ['area'])
    bdi.check_for_curv_stats_files()
    assert len(bdi.subjects_list) == 2
    assert len(bdi.descriptor_names) == 0
    assert bdi.descriptor_values.shape == (2, 0)
