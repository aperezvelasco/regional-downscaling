from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from regional_downscaling.provider.download import download_cerra_data


def test_download_cerra_data(mocker: MockerFixture, tmp_path: Path):
    # Set up mock CDSAPI client and retrieve method
    mock_retrieve = mocker.patch("cdsapi.Client.retrieve")
    mock_cdsapi = mocker.patch("cdsapi.Client", return_value=mocker.Mock(retrieve=mock_retrieve))

    # Set up test variables
    variable = "2m_temperature"
    level_type = "surface_or_atmosphere"
    data_type = "reanalysis"
    product_type = "analysis"
    year = "2021"
    month = "01"
    day = "01"
    time = "00:00"
    fmt = "netcdf"
    output_directory = str(tmp_path)

    # Call function with test variables
    output_path = download_cerra_data(
        variable=variable,
        level_type=level_type,
        data_type=data_type,
        product_type=product_type,
        year=year,
        month=month,
        day=day,
        time=time,
        fmt=fmt,
        output_directory=output_directory,
    )

    # Assert that the output path is correct
    expected_output_path = tmp_path / f"reanalysis-cerra-single-levels/{variable}/" \
                                      f"{variable}_{day}{month}{year}_{time.split(':')[0]}.nc"
    assert output_path == expected_output_path

    # Assert that the CDSAPI client was called with the correct arguments
    mock_cdsapi.assert_called_once()
    mock_retrieve.assert_called_once_with(
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


