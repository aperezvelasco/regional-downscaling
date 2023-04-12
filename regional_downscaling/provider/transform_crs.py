import pyproj
import xarray as xr
import xesmf as xe


def reproject_dataset(ds, input_crs, output_crs, output_file):
    """
    Reproject an xarray Dataset to a new coordinate reference system (CRS).

    Parameters
    ----------
    ds : xarray.Dataset
        The input dataset to reproject.
    input_crs : str
        The input CRS string in Proj format.
    output_crs : str
        The output CRS string in Proj format.
    output_file : str
        The output file path to save the reprojected dataset to.
    """

    # Define the projection objects for the input and output CRS
    in_proj = pyproj.Proj(input_crs)
    out_proj = pyproj.Proj(output_crs)

    # Reproject the input data to the output CRS
    lon, lat = pyproj.transform(
        in_proj, out_proj, ds.longitude.values, ds.latitude.values
    )
    data, _, _ = pyproj.transform(
        in_proj, out_proj, ds.values, lon, lat, always_xy=True
    )

    # Create a new xarray Dataset with the reprojected data
    ds_reprojected = xr.Dataset(
        {"data": (["lat", "lon"], data)}, coords={"lat": lat[:, 0], "lon": lon[0, :]}
    )

    # Set the coordinate reference system for the new Dataset
    ds_reprojected.attrs["crs"] = output_crs

    # Write the reprojected data to a netCDF file
    ds_reprojected.to_netcdf(output_file)


def interpolate_dataset(ds, grid, method, output_file):
    """
    Interpolate an xarray Dataset to a new grid using xesmf.

    Parameters
    ----------
    ds : xarray.Dataset
        The input dataset to interpolate.
    grid : xarray.Dataset or dict
        The target grid to interpolate to.
    method : str
        The interpolation method to use. Supported methods are 'bilinear', 'conservative', 'nearest_s2d',
        'nearest_d2s', 'patch', and 'regrid_doc'.
    output_file : str
        The output file path to save the interpolated dataset to.
    """

    # Create the xesmf regridder object
    regridder = xe.Regridder(ds, grid, method)

    # Interpolate the input data to the target grid
    ds_interpolated = regridder(ds)

    # Write the interpolated data to a netCDF file
    ds_interpolated.to_netcdf(output_file)
