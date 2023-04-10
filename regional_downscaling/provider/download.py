import calendar
from pathlib import Path
from typing import Union

import cdsapi


def download_cerra_data(
    variable: str = "2m_temperature",
    level_type: str = "surface_or_atmosphere",
    data_type: str = "reanalysis",
    product_type: str = "analysis",
    year: str = "2021",
    month: Union[str, list] = "01",
    day: Union[str, list, None] = "01",
    time: Union[str, list, None] = "00:00",
    fmt: str = "netcdf",
    output_directory: str = "/tmp",
) -> Path:
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
    output_directory : str, optional
        The output directory to save the downloaded data, defaults to '/tmp'.

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

    if day and time:
        date_str = "{0}{1}{2}_{3}".format(day, month, year, time.split(":")[0])
    elif day and not time:
        date_str = "{0}{1}{2}".format(day, month, year, time.split(":")[0])
    else:
        date_str = "{0}{1}".format(month, year)

    output_path = (
        f"{output_directory}/"
        f"reanalysis-cerra-single-levels/"
        f"{variable}/"
        f"{variable}_{date_str}.nc"
    )
    output_path = Path(output_path)

    if output_path.exists():
        return output_path
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True, mode=0o777)

    c = cdsapi.Client()

    if not day:
        _, days_in_month = calendar.monthrange(int(year), int(month))
        day = [day for day in range(1, days_in_month + 1)]

    if not time:
        hours = ["{:02.0f}".format(hour) for hour in range(0, 24, 3)]
        time = [f"{hour}:00" for hour in hours]

    c.retrieve(
        "reanalysis-cerra-single-levels",
        {
            "variable": variable,
            "level_type": level_type,
            "data_type": data_type,
            "product_type": product_type,
            "year": year,
            "month": month,
            "day": day,
            "time": time,
            "format": fmt,
        },
        output_path,
    )
    return output_path


def download_era5_data(
    variable: str = "2m_temperature",
    product_type: str = "reanalysis",
    year: str = "2021",
    month: Union[str, list, None] = "01",
    day: Union[str, list, None] = "01",
    time: Union[str, list, None] = "00:00",
    fmt: str = "netcdf",
    output_directory: str = "/tmp",
) -> Path:
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
    output_directory : str, optional
        The output directory to save the downloaded data, defaults to '/tmp'.

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
    if day and time:
        date_str = "{0}{1}{2}_{3}".format(day, month, year, time.split(":")[0])
    elif day and not time:
        date_str = "{0}{1}{2}".format(day, month, year, time.split(":")[0])
    else:
        date_str = "{0}{1}".format(month, year)

    output_path = (
        f"{output_directory}/"
        f"reanalysis-cerra-single-levels/"
        f"{variable}/"
        f"{variable}_{date_str}.nc"
    )
    output_path = Path(output_path)

    if output_path.exists():
        return output_path
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True, mode=0o777)

    if not day:
        _, days_in_month = calendar.monthrange(int(year), int(month))
        day = [day for day in range(1, days_in_month + 1)]

    if not time:
        hours = ["{:02.0f}".format(hour) for hour in range(0, 24, 1)]
        time = [f"{hour}:00" for hour in hours]

    c = cdsapi.Client()

    c.retrieve(
        "reanalysis-era5-single-levels",
        {
            "product_type": product_type,
            "variable": variable,
            "year": year,
            "month": month,
            "day": day,
            "time": time,
            "format": fmt,
        },
        output_path,
    )
    return output_path
