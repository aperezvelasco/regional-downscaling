
****************************
Regional downscaling
****************************

|pypi_release| |pypi_status| |pypi_downloads| |docs|

A spatio-temporal downscaling package to perform regional downscaling over spatio-temporal datasets.

In this particular case, we define a model to perform downscaling from:

- the ERA5 dataset (https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels)

to:

- the CERRA dataset (https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-cerra-single-levels) .

ERA5 reanalysis cropped to CERRA coverage:

.. image:: https://github.com/aperezvelasco/regional-downscaling/blob/main/reports/viz/era5_in_cerra_coverage-viz-2m_temperature-01012021-00.png

CERRA reanalysis:

.. image:: https://github.com/aperezvelasco/regional-downscaling/blob/main/reports/viz/cerra-viz-2m_temperature-01012021-00.png


.. |pypi_release| image:: https://img.shields.io/pypi/v/thermofeel?color=green
    :target: https://pypi.org/project/thermofeel

.. |pypi_status| image:: https://img.shields.io/pypi/status/thermofeel
    :target: https://pypi.org/project/thermofeel

.. |pypi_downloads| image:: https://img.shields.io/pypi/dm/thermofeel
  :target: https://pypi.org/project/thermofeel
  
.. |docs| image:: https://readthedocs.org/projects/thermofeel/badge/?version=latest
  :target: https://thermofeel.readthedocs.io/en/latest/?badge=latest
