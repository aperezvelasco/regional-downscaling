import xarray
from regional_downscaling.provider.download import (download_cerra_data,
                                                    download_era5_data)
from regional_downscaling.provider.preprocess import preprocess


def main():
    era5_data_path = download_era5_data()
    era5_data = xarray.open_dataset(era5_data_path)
    era5_data = preprocess(era5_data, "ERA5", "tas", {"tas": "t2m"})
    cerra_data_path = download_cerra_data()
    cerra_data = xarray.open_dataset(cerra_data_path)
    cerra_data = preprocess(cerra_data, "CERRA", "tas", {"tas": "t2m"})
    return era5_data, cerra_data


if __name__ == "__main__":
    main()
