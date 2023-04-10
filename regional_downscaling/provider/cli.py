import click

import xarray
from regional_downscaling.provider.download import (download_cerra_data,
                                                    download_era5_data)
from regional_downscaling.provider.preprocess import preprocess


@click.group()
def launcher():
    """"""
    pass


@launcher.command("Provider")
@click.option(
    "-o",
    "--output_dir",
    help="Directory where to download the data to (example: /tmp)",
    default="/tmp",
    type=str,
)
@click.option(
    "-p",
    "--project",
    help="Project to download the data from (CERRA or ERA5)",
    default="ERA5",
    type=str,
)
@click.option(
    "-v",
    "--variable",
    help="Variable to download the data for (i.e. tas or pr)",
    default="tas",
    type=str,
)
@click.option(
    "-y",
    "--year",
    help="Year to download the data for (i.e. 1940-current)",
    default=2010,
    type=int,
)
@click.option(
    "-m",
    "--month",
    help="Month to download the data for (i.e. 1 for January)",
    default=1,
    type=int,
)
def provider_cli(
    output_dir: str, project: str, variable: str, year: int, month: int
) -> None:
    """
    Execute the main datacica workflow.

    This function runs the main datacica workflow using the configuration specified
    in the configuration_yaml file. The output configuration and data paths will be
    written to the results_yaml file. The force option can be set to True to force
    the workflow to run entirely, ignoring any previously completed steps.

    Parameters
    ----------
    output_dir: str
    project: str
    variable: str
    year: int
    month: int

    Returns
    -------
    None
    """
    day = None
    time = None
    if project == "CERRA":
        cds_variable = dict(tas="2m_temperature")
        data_path = download_cerra_data(
            variable=cds_variable[variable],
            year=str(year),
            month="{:02.0f}".format(month),
            day=day,
            time=time,
            output_directory=output_dir,
        )
    elif project == "ERA5":
        cds_variable = dict(tas="2m_temperature")
        data_path = download_era5_data(
            variable=cds_variable[variable],
            year=str(year),
            month="{:02.0f}".format(month),
            day=day,
            time=time,
            output_directory=output_dir,
        )
    else:
        raise NotImplementedError

    data_raw = xarray.open_dataset(data_path)
    data_processed = preprocess(
        data_raw, project=project, variable="tas", variable_map={"tas": "t2m"}
    )
    data_processed.to_netcdf("/tmp/trial_processed.nc")


if __name__ == "__main__":
    launcher()
