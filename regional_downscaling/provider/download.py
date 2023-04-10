import os.path

import cdsapi

from typing import Union


def download_cerra_data(
        variable: str = "2m_temperature",
        level_type: str = "surface_or_atmosphere",
        data_type: str = "reanalysis",
        product_type: str = "analysis",
        year: str = "2021",
        month: Union[str, list] = "01",
        day: Union[str, list] = "01",
        time: Union[str, list] = "00:00",
        fmt: str = "netcdf",
        output_path: str = "/tmp/cerra-2m_temperature-surface_or_atmosphere"
                           "-reanalysis-analysis-01012021-00.nc"
):
    """
       Downloads CERRA data for a specified variable, level type, data type,
       product type, year, month, day, time, and file format, and saves it
       to the specified output path.

       Parameters
       ----------
       variable : str, optional
           The variable to provider data for, defaults to '2m_temperature'.
       level_type : str, optional
           The level type of the data, defaults to 'surface_or_atmosphere'.
       data_type : str, optional
           The type of data to provider, defaults to 'reanalysis'.
       product_type : str, optional
           The product type of the data, defaults to 'analysis'.
       year : str, optional
           The year of the data to provider, defaults to '2021'.
       month : str or list, optional
           The month of the data to provider, defaults to '01'.
       day : str or list, optional
           The day of the data to provider, defaults to '01'.
       time : str or list, optional
           The time of the data to provider in the format HH:MM, defaults to '00:00'.
       fmt : str, optional
           The format to provider the data in, defaults to 'netcdf'.
       output_path : str, optional
           The output path to save the downloaded data, defaults to
           '/tmp/cerra-2m_temperature-surface_or_atmosphere-reanalysis-analysis-01012021-00.nc'.

       Returns
       -------
       str
           The output path of the downloaded data.

       Raises
       ------
       cdsapi.api.CDSAPIError
           If the CDS API request fails.

       Examples
       --------
       download_cerra_data(variable='2m_temperature', year='2020', month='12', day='31')
       '/tmp/cerra-2m_temperature-surface_or_atmosphere-reanalysis-analysis-12312020-00.nc'

       """
    if os.path.exists(output_path):
        return output_path

    c = cdsapi.Client()

    c.retrieve(
        'reanalysis-cerra-single-levels',
        {
            'variable': variable,
            'level_type': level_type,
            'data_type': data_type,
            'product_type': product_type,
            'year': year,
            'month': month,
            'day': day,
            'time': time,
            'format': fmt,
        },
        output_path
    )
    return output_path


def download_era5_data(
        variable: str = "2m_temperature",
        product_type: str = "reanalysis",
        year: str = "2021",
        month: Union[str, list] = "01",
        day: Union[str, list] = "01",
        time: Union[str, list] = "00:00",
        fmt: str = "netcdf",
        output_path: str = "/tmp/era5-2m_temperature-reanalysis-01012021-00.nc"
) -> str:
    """
    Downloads ERA5 data for a specified variable, year, month, day,
    time, and file format, and saves it to the specified output path.

    Parameters
    ----------
    variable : str, optional
        The variable to provider data for, defaults to '2m_temperature'.
    product_type : str, optional
        The product type of the data, defaults to 'reanalysis'.
    year : str, optional
        The year of the data to provider, defaults to '2021'.
    month : str or list, optional
        The month of the data to provider, defaults to '01'.
    day : str or list, optional
        The day of the data to provider, defaults to '01'.
    time : str or list, optional
        The time of the data to provider in the format HH:MM, defaults to '00:00'.
    fmt : str, optional
        The format to provider the data in, defaults to 'netcdf'.
    output_path : str, optional
        The output path to save the downloaded data, defaults to 'provider.nc'.

    Returns
    -------
    str
        The output path of the downloaded data.

    Raises
    ------
    cdsapi.api.CDSAPIError
        If the CDS API request fails.

    Examples
    --------
    download_era5_data(variable='2m_temperature', year='2021', month='01', day='01')
    "/tmp/era5-2m_temperature-reanalysis-01012021-00.nc"

    """
    if os.path.exists(output_path):
        return output_path

    c = cdsapi.Client()

    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': product_type,
            'variable': variable,
            'year': year,
            'month': month,
            'day': day,
            'time': time,
            'format': fmt,
        },
        output_path
    )
    return output_path


