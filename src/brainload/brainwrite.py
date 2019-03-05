# -*- coding: utf-8 -*-
"""
Some functions for writing brain data to files.

These functions are helpful if you want to generate and write volume or surface data.
"""

import numpy as np


def get_volume_data_with_custom_marks(voxel_mark_list, background_voxel_value=0, shape=(256, 256, 256), dtype=np.uint8):
    """
    Generate a volume in which the target voxels are marked by the individual colors assigned to each voxel array in the list.

    Generate a volume in which the values of all target_voxel_indices are set to a target_voxel_value that can be defined separately for each subject/entry in the list. This is useful for visualizing the voxels in a 3D viewer.

    Parameters
    ----------

    voxel_mark_list: list of tuples
        Each tuple contains first the voxel indices (2D numpy int array with shape (n, 3)) and then a single integer, the voxel value to use for the voxel indices.

    background_voxel_value: np.uint8, optional
        The value to assign to all voxels which are not in the voxel_mark_list, i.e., the background voxels. Defaults to 0. The type must match the dtype parameter.

    shape: tupel of int, optional
        The shape of the 3D volume, i.e., the number of voxels along the 3 dimensions. Defaults to (256, 256, 256).

    dtype: datatype, optional
        The data type of the returned data 3D array. Defaults to ```np.uint8```.

    Returns
    -------
    voxel_data: numpy multi-dimensional array
        The shape depends on the shape parameter, and the data type on the dtype parameter of this function. The voxels within this 3D volume are marked with the requested target values (or the background value).

    Examples
    --------
    Create volume data with shape 256x256x256 in which 2 voxels are marked with intensity value 40, and 2 other voxels with intensity value 160:
    >>> import brainload.brainwrite as bw
    >>> voxel_mark_list = [(np.array([[15, 25, 30], [24, 24, 24]], dtype=int), 40), (np.array([[44, 44, 44], [55, 55, 55]], dtype=int), 160)]
    >>> vol_data = bw.get_volume_data_with_custom_marks(voxel_mark_list, background_voxel_value=0, shape=(256, 256, 256))

    You could now write vol_data to a nifti file using nibabel:

    >>> import nibabel as nib
    >>> ni_img = nib.Nifti1Image(vol_data, np.eye(4))
    >>> nib.save(ni_img, 'my_data.nii')
    """
    # set background
    voxel_data = np.ones(shape, dtype=dtype) * background_voxel_value
    # iterate through list and set proper color for each set of voxels
    for val_tuple in voxel_mark_list:
        target_voxel_indices = val_tuple[0]
        target_voxel_value = val_tuple[1]
        for coord in target_voxel_indices:
            voxel_data[coord[0],coord[1], coord[2]] = target_voxel_value
    return voxel_data


def get_surface_vertices_overlay_volume_data(num_verts, vertex_mark_list, background_rgb=[200, 200, 200], dtype=np.uint8):
    """
    Generates a surface overlay as a binary volume image file.

    Generates a surface overlay volume. The volume contains one color value per vertex of the surface and can be used to visualize different vertices on a brain surface. This functions supports coloring different sets of vertices with different colors. All vertices which are not explicitely listed with a color to assign to them are given the background color.

    Parameters
    ----------
    num_verts: int
        The number of vertices of the surface. E.g., 163842 if you want to color vertices on a hemisphere from the fsaverage Freesurfer subject.

    vertex_mark_list: list of tuples
        Each tuple contains first the voxel indices (1D numpy int array with shape (n, ) for n vertices) and then a 1D array of length 3 that represents the RGB values of the color to assign to all the previously given n vertices.

    background_rgb: numpy 1D array of length 3, optional
        The background color, defined as 3 RGB values. Defaults to [200, 200, 200], which is a bright gray. This is assigned to all vertices which do not occur in vertex_mark_list.

    dtype: data type, optional
        The data type of the returned data 3D array. Defaults to ```np.uint8```.

    Returns
    -------
    voxel_data: numpy 3D array
        A 3D array with shape (n, 3, 1) for the n vertices of the surface that contains the colors given by the 3 RGB values.

    Examples
    --------
    Create an overlay for an fsaverage hemisphere (which always has exactly 163842 vertices) and mark 3 of the vertices in red and 4 others in green. The rest will be gray.

    >>> num_verts = 163842
    >>> vertex_mark_list = [(np.array([0, 2, 4], dtype=int), [255, 0, 0]), (np.array([1, 3, 5, 7], dtype=int), [0, 255, 0])]
    >>> vol_data = bw.get_surface_vertices_overlay_volume_data(num_verts, vertex_mark_list, background_rgb=[200, 200, 200])

    You could now write this to a nifti or mgz file and load it as a surface overlay.

    See also
    --------
    ```get_surface_vertices_overlay_volume_data```: the same data, but for writing to a similar file in text format
    """
    background_rgb = np.array(background_rgb, dtype=dtype)
    shape = (num_verts, 3, 1)
    voxel_data = np.zeros(shape, dtype=dtype)
    # set background color for all voxels/verts
    voxel_data[:,0,0] = background_rgb[0]
    voxel_data[:,1,0] = background_rgb[1]
    voxel_data[:,2,0] = background_rgb[2]
    # overwrite the color for the marked ones with the requested colors.
    for val_tuple in vertex_mark_list:
        target_vertex_indices = val_tuple[0]
        target_vertex_rgb = val_tuple[1]
        for vert_idx in target_vertex_indices:
            voxel_data[vert_idx,0,0] = target_vertex_rgb[0]
            voxel_data[vert_idx,1,0] = target_vertex_rgb[1]
            voxel_data[vert_idx,2,0] = target_vertex_rgb[2]
    return voxel_data


def get_surface_vertices_overlay_text_file_lines(num_verts, vertex_mark_list, background_rgb=[200, 200, 200], dtype=np.uint8):
    """
    Generates a surface overlay as a text file.

    Performs the same task as get_surface_vertices_overlay_volume_data, but outputs the data as lines that can be written to a text file. This is an alternate format for a surface overlay file.

    Parameters
    ----------
    num_verts: int
        The number of vertices of the surface. E.g., 163842 if you want to color vertices on a hemisphere from the fsaverage Freesurfer subject.

    vertex_mark_list: list of tuples
        Each tuple contains first the voxel indices (1D numpy int array with shape (n, ) for n vertices) and then a 1D array of length 3 that represents the RGB values of the color to assign to all the previously given n vertices.

    background_rgb: numpy 1D array of length 3, optional
        The background color, defined as 3 RGB values. Defaults to [200, 200, 200], which is a bright gray. This is assigned to all vertices which do not occur in vertex_mark_list.

    dtype: data type, optional
        The data type of the returned data 3D array. Defaults to ```np.uint8```.

    Returns
    -------
    lines: list of str
        A list of lines that can be written to a text file as a surface overlay. Each line represents the color of a single vertex. Vertex order is the same as the order of vertices in the surface file that this overlay is for.
    """
    voxel_data = get_surface_vertices_overlay_volume_data(num_verts, vertex_mark_list, background_rgb=background_rgb, dtype=dtype)
    lines = []
    for row in voxel_data:
        lines.append("%d, %d, %d" % (row[0][0], row[1][0], row[2][0]))
    return lines
