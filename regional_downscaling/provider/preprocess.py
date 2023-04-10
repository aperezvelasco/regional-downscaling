import xarray
import datetime
import pandas


def preprocess(ds: xarray.Dataset, project: str, variable: str, variable_map: dict):
    ds = fix_spatial_coord_names(ds)
    # ds = fix_non_standard_calendar(ds)
    ds = rename_and_delete_variables(ds, variable, variable_map)
    ds = fix_360_longitudes(ds, project=project)
    ds = convert_units(ds)
    return ds


def fix_non_standard_calendar(dataset: xarray.Dataset) -> xarray.Dataset:
    """
    Fix non-standard calendars.

    Function to change time with different calendar, if the frequency of the data is
    monthly just change the datatype,  if the frequency is daily calendars
    e.g UK models with leap year are solved

    Parameters
    ----------
    dataset (xarray.Dataset): data stored by dimensions

    Returns
    -------
    dataset (xarray.Dataset): dataset with the correct calendar
    """
    dataset_frequency, coerced = infer_dataset_frequency(dataset)
    dataset = dataset.assign_coords(time=coerced)
    if coerced[-1].month == 12 and coerced[-1].day == 30:
        real_time = pandas.date_range(
            start=coerced[0],
            end=coerced[-1] + datetime.timedelta(days=1),
            freq=dataset_frequency,
        )
    else:
        real_time = pandas.date_range(
            start=coerced[0].replace(day=1), end=coerced[-1], freq=dataset_frequency
        )
    # Removing 29 (no leap years) and 30 feb
    dataset = dataset.where(~dataset.time.isnull(), drop=True)
    # Filling missing dates (31 of every month)
    dataset = dataset.reindex({"time": real_time}, method="ffill")
    return dataset


def infer_dataset_frequency(dataset):
    """
    Infer dataset frequency (daily, monthly, ...).

    Function to infer the time frequency of the dataset and return the new time
    object in daily or hourly format

    Parameters
    ----------
    dataset (xarray.Dataset): data stored by dimensions

    Returns
    -------
    dataset_frequency (str): frequency of the dataset
    coerced (pandas.Datetime): dates stored in pandas object
    """
    try:
        dataset_frequency = xarray.infer_freq(dataset.time)
        if dataset_frequency == "D":
            string_dates = [str(d)[:10] for d in dataset.time.values]
        elif dataset_frequency == "H":
            string_dates = [str(d) for d in dataset.time.values]
        elif dataset_frequency == "MS":
            string_dates = [str(d)[:10] for d in dataset.time.values]
        elif dataset_frequency is None or dataset_frequency == "30D":
            string_dates = [str(d)[:10] for d in dataset.time.values]
            dataset_frequency = "MS"
        else:
            raise NotImplementedError
        coerced = pandas.to_datetime(string_dates, errors="coerce")
        return dataset_frequency, coerced
    except Exception as ex:
        raise Exception(ex)


def fix_spatial_coord_names(dataset: xarray.Dataset) -> xarray.Dataset:
    """
    Fix the coordinates names for spatial coordinates (x, y, lon, lat, ...).

    Function to renaming all spatial coords into lon and lat to chunk more easily later

    Parameters
    ----------
    dataset (xarray.Dataset): data stored by dimensions

    Returns
    -------
     dataset (xarray.Dataset): data with the remaining coordinates "lon" and "lat"
    """
    if ("rlon" in dataset.dims or "rlon" in dataset.coords) and (
        "longitude" in dataset.dims or "longitude" in dataset.coords
    ):
        return dataset.rename(
            {"rlon": "x", "rlat": "y", "longitude": "lon", "latitude": "lat"}
        )
    elif ("i" in dataset.dims or "i" in dataset.coords) and (
        "longitude" in dataset.dims or "longitude" in dataset.coords
    ):
        return dataset.rename(
            {"i": "x", "j": "y", "longitude": "lon", "latitude": "lat"}
        )
    elif "rlon" in dataset.dims or "rlon" in dataset.coords:
        return dataset.rename({"rlon": "x", "rlat": "y"})

    elif "lon" in dataset.dims or "lon" in dataset.coords:
        return dataset
    elif "x" in dataset.dims or "y" in dataset.coords:
        return dataset.rename({"x": "lon", "y": "lat"})
    elif "longitude" in dataset.dims or "longitude" in dataset.coords:
        return dataset.rename({"longitude": "lon", "latitude": "lat"})
    else:
        raise NotImplementedError


def fix_360_longitudes(
    dataset: xarray.Dataset, project: str, lonname: str = "lon"
) -> xarray.Dataset:
    """
    Fix longitude values.

    Function to transform datasets where longitudes are in (0, 360) to (-180, 180).

    Parameters
    ----------
    dataset (xarray.Dataset): data stored by dimensions
    project (str): project of the process e.g CMIP6, CORDEX...
    lonname (str): name of the longitude dimension

    Returns
    -------
    dataset (xarray.Dataset): data with the new longitudes
    """
    lonname = lonname if "CERRA" not in project else "longitude"
    lon = dataset[lonname]
    if lon.max().values > 180 and lon.min().values >= 0:
        dataset[lonname] = dataset[lonname].where(lon <= 180, other=lon - 360)
    if "CERRA" not in project and len(dataset.lat.shape) != 2:
        dataset = dataset.reindex(**{lonname: sorted(dataset[lonname])})
    return dataset


def rename_and_delete_variables(
    ds: xarray.Dataset, variable: str, var_mapping: dict
) -> xarray.Dataset:
    """
    Remove unused data.

    Function to remove variables and dimensions not used.

    Parameters
    ----------
    ds (xarray.Dataset): data stored by dimensions
    var_mapping (dict): dictionary for mapping the variables of the different datasets

    Returns
    -------
    xarray.Dataset: dataset with unnecessary coordinates removed
    """
    # select the main variable
    try:
        var_name = var_mapping[variable]
    except KeyError:
        var_name = variable
    # rename variable
    ds = ds.rename_vars({var_name: variable})
    # adding height coordinate
    ds = ds.assign_coords({"height": 2.0})
    # avoiding useless variables
    ds = ds[[variable]]
    # delete useless dimensions
    main_coords = ["time", "lon", "lat", "height", "x", "y", "latitude", "longitude"]
    if sorted(list(ds.coords)) != sorted(main_coords):
        dim_to_remove = [dim for dim in list(ds.coords) if dim not in main_coords]
        ds = ds.drop_vars(dim_to_remove)
    if "time" not in list(ds.dims):
        ds = ds.expand_dims("time")
    return ds

def convert_units(ds: xarray.Dataset) -> xarray.Dataset:
    """
    Transform the data units.

    Performs data transformation by reading the 'units' attribute inside the metadata.
    For instance: if data is in Kelvin, the function transform it in ºC

    Parameters
    ----------
    ds (xarray.Dataset): data stored by dimensions

    Returns
    -------
    ds (xarray.Dataset): data with the new units
    """

    UNIT_CONVERTER = {
        "Kelvin": (1, -273.15, "Celsius"),
        "K": (1, -273.15, "Celsius"),
        "Fahrenheit": (5 / 9, -32 * 5 / 9, "Celsius"),
        "Celsius": (1, 0, "Celsius"),
        "degC": (1, 0, "Celsius"),
        "m hour**-1": (1000 * 24, 0, "mm"),
        "mm day**-1": (1, 0, "mm"),
        "mm": (1, 0, "mm"),
        "m": (1000, 0, "mm"),
        "mm s**-1": (3600 * 24, 0, "mm"),
        "kg m**-2 day**-1": (1, 0, "mm"),
        "kg m-2 s-1": (3600 * 24, 0, "mm"),
        "kg m**-2": (1, 0, "mm"),
        "kg m-2": (1, 0, "mm"),
        "m of water equivalent": (1000, 0, "mm"),
        "m s**-1": (1, 0, "m s-1"),
        "m s-1": (1, 0, "m s-1"),
        "km h**-1": (10 / 36, 0, "m s-1"),
        "knots": (0.51, 0, "m s-1"),
        "kts": (0.51, 0, "m s-1"),
        "mph (nautical miles per hour)": (0.51, 0, "m s-1"),
        "%": (1, 0, "%"),
        "W m**-2": (1, 0, "W m-2"),
    }

    VALID_UNITS = {
        "tas": "Celsius",
        "mx2t": "Celsius",
        "tasmax": "Celsius",
        "tasmin": "Celsius",
        "hurs": "%",
        "clt": "%",
        "evspsbl": "kg m-2 s-1",
        "pr": "mm",
        "psl": "Pa",
        "prsn": "mm",
        "sisonc": "%",
        "sfcwind": "m s-1",
        "uwind": "m s**-1",
        "vwind": "m s**-1",
        "mrso": "kg m-2",
        "huss": "1",
        "sst": "Celsius",
        "rlds": "W m-2",
        "rsds": "W m-2",
        "mslp": "Pa",
        "z": "m**2 s**-2",
    }

    for ds_var in list(ds.data_vars):
        if ds[ds_var].attrs["units"] == VALID_UNITS[ds_var]:
            continue
        else:
            conversion = UNIT_CONVERTER[ds[ds_var].attrs["units"]]
            ds[ds_var] = ds[ds_var] * conversion[0] + conversion[1]
            ds[ds_var].attrs["units"] = conversion[2]
    return ds

