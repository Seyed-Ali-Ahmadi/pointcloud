from laspy.file import File
import numpy as np
from scipy.spatial.kdtree import KDTree

######################################################


def read_laser(directory):
    # function to read '.las' files and print their size
    # input: file location and its name
    # output: .las file in numpy array
    laser_file = File(directory, mode='r')
    print('Number of points     >   ', len(laser_file.points))
    print('Scale of axis    >   ', laser_file.header.scale)
    print('Offset of points    >   ', laser_file.header.offset)
    print('Each column is    >  ', laser_file.points.dtype)
    print('Number of columns is     >   ', len(laser_file.points.dtype[0]))
    return laser_file
######################################################


def pt_format(laser_file):
    # function to print header information and point specs
    # input: .las file which is read before with read_laser function
    # output: point specifications and number of point columns (X, Y, Z, ...)
    m = 0
    for spec in laser_file.point_format:
        print(spec.name)
        m += 1
    print(m)
    return m
######################################################


def set_scale_offset(laser_file):
    # WARNING: THIS FUNCTION IS TIME CONSUMING AND REQUIRES MEMORY.
    # function to apply X, Y, Z scale and offset to raw points
    # input: .las file which is read before with read_laser function
    # output: scaled points as a numpy array
    # *** las_file.XYZ gives raw coordinates while las_file.xyz returns scaled dimensions,
    # *** but is not recommended due to rounding error.
    scaled_x = laser_file.X*laser_file.header.scale[0] + laser_file.header.offset[0]
    scaled_y = laser_file.Y*laser_file.header.scale[1] + laser_file.header.offset[1]
    scaled_z = laser_file.Z*laser_file.header.scale[2] + laser_file.header.offset[2]
    scaled_pts = np.column_stack((scaled_x, scaled_y, scaled_z))
    return scaled_pts
######################################################


def find_bad_pts(laser_file):
    # function to find invalid X, Y, Z values which are less or greater than min or max values.
    # input: .las file
    # output: indices of bad points
    # Get arrays which indicate invalid X, Y, or Z values.
    x_invalid = np.logical_or((laser_file.header.min[0] > laser_file.x),
                              (laser_file.header.max[0] < laser_file.x))
    y_invalid = np.logical_or((laser_file.header.min[1] > laser_file.y),
                              (laser_file.header.max[1] < laser_file.y))
    z_invalid = np.logical_or((laser_file.header.min[2] > laser_file.z),
                              (laser_file.header.max[2] < laser_file.z))
    bad_indices = np.where(np.logical_or(x_invalid, y_invalid, z_invalid))
    return bad_indices
######################################################


def build_tree(laser_file):
    # build a KD-tree over the point clouds to find nearest neighbors.
    # input: the point cloud file that is going to be searched.
    # output: the tree file that includes indices ready to be searched.
    data_ready = np.vstack([laser_file.X, laser_file.Y, laser_file.Z]).transpose()
    tree = KDTree(data_ready)
    return tree
######################################################


def find_nns(point, tree, k):
    # function to find k nearest neighbors to "point" from "laser_file" previously defined.
    # input: the point coordinate.
    # output: index and distance of k NNs
    # 1st array --> The distances to the nearest neighbors.
    # 2nd array --> The locations of the neighbors in self.data.
    found = tree.query(point, k=k)
    return found
######################################################


def write_laser():
    # TODO
    pass



