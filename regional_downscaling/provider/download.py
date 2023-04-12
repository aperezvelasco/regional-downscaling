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

    """

    output_path = get_output_path(
        catalogue_entry="reanalysis-cerra-single-levels",
        output_directory=output_directory,
        variable=variable,
        day=day,
        month=month,
        year=year,
        hour=time,
    )

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
        The year of the data to provide, defaults to '2021'.
    month : str or list, optional
        The month of the data to provide, defaults to '01'.
    day : str or list, optional
        The day of the data to provide, defaults to '01'.
    time : str or list, optional
        The time of the data to provide in the format HH:MM, defaults to '00:00'.
    fmt : str, optional
        The format to provide the data in, defaults to 'netcdf'.
    output_directory : str, optional
        The output directory to save the downloaded data, defaults to '/tmp'.

    Returns
    -------
    str
        The output path of the downloaded data.

    """
    output_path = get_output_path(
        catalogue_entry="reanalysis-era5-single-levels",
        output_directory=output_directory,
        variable=variable,
        day=day,
        month=month,
        year=year,
        hour=time,
    )

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


def get_output_path(
    catalogue_entry, output_directory, variable, day, month, year, hour
):
    """
    Generate a file path for a given parameter combination.

    Given the output directory, catalogue entry, variable, date, and time.

    Parameters
    ----------
    output_directory : str
        The directory in which the output file will be saved.
    catalogue_entry : str
        The catalogue entry for the output file.
    variable : str
        The variable name for the output file.
    day : str or None
        The day of the month for the output file (e.g. '01' for the 1st).
        If `None`, the day will be excluded from the file name.
    month : str
        The month of the year for the output file (e.g. '01' for January).
    year : str
        The year for the output file (e.g. '2023').
    hour : str or None
        The hour of the day for the output file (e.g. '12:00' for noon).
        If `None`, the hour will be excluded from the file name.

    Returns
    -------
    output_path : pathlib.Path
        The full file path for the output file.
    """
    if day and hour:
        date_str = "{0}{1}{2}_{3}".format(day, month, year, hour.split(":")[0])
    elif day and not hour:
        date_str = "{0}{1}{2}".format(day, month, year)
    else:
        date_str = "{0}{1}".format(month, year)
    output_path = (
        f"{output_directory}/"
        f"{catalogue_entry}/"
        f"{variable}/"
        f"{variable}_{date_str}.nc"
    )
    output_path = Path(output_path)
    return output_path
