import xarray as xr
import netCDF4
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial

# Finds the nearest matrix coordinates corresponding to the
# Lat and long of the bounding box defined by the NW corner and SE corner

def findBoundBoxCoords(file_path, latNW, longNW, latSE, longSE):
	fh = netCDF4.Dataset(file_path, mode='r')
	collectionDate = fh.time_coverage_start[0:10]

	nav_dataset = xr.open_dataset(file_path, 'navigation_data')

	latitude = nav_dataset['latitude']
	longitude = nav_dataset['longitude']

	latarr = np.array(latitude).flatten()
	longarr = np.array(longitude).flatten()
	latarr = np.expand_dims(latarr, axis=1)
	longarr = np.expand_dims(longarr, axis=1)

	points = np.concatenate([latarr, longarr], axis=1)
	pointNW = [latNW, longNW]
	latlongKDTree = spatial.KDTree(points)
	distance,index = latlongKDTree.query(pointNW)
	orig_indexNW = np.unravel_index(index, latitude.shape)
	pointSE = [latSE, longSE]
	distance,index = latlongKDTree.query(pointSE)
	orig_indexSE = np.unravel_index(index, latitude.shape)

	return collectionDate, orig_indexSE, orig_indexNW