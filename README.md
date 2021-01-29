# EGD-downloader

Tool to download the data from the Erasmus Glioma Database

## Background

This tool can be used to download the data from the Erasmus Glioma Database that is hosted on the [BMIA XNAT](https://xnat.bmia.nl/data/archive/projects/egd). This data is described in the accompanying publication (publication to be published later). Please cite this publication when using this data.

The data is hosted on `XNAT`, and can be interacted with using the `XNAT` API or one of the python packages that can interact with `XNAT` such as [xnatpy](https://xnat.readthedocs.io/en/latest/) or [pyxnat](https://pyxnat.github.io/pyxnat/).

This tool was designed to obviate the need for interacting with XNAT, instead directly downloading the data to a local directory.

## Downloading the data

This tool requires the installation of `Docker`.
Installation instructions can be found on [the docker website](https://docs.docker.com/get-docker/).

Once `Docker` has been installed, run the following command to install the data locally:

```bash
docker run  --mount type=bind,source=/PATH/TO/YOUR/OUTPUT/FOLDER,target=/output --rm svdvoort/egd-downloader:1.1 --user <YOUR_USERNAME> --password <YOUR_PASSWORD>
```

In this command three items have to be set by the user:

* `/PATH/TO/YOUR/OUTPUT/FOLDER` needs to be replaced by your desired output folder (folder should exist)
* `<YOUR_USERNAME>` needs to be replaced by the user's username for the BMIA XNAT.
* `<YOUR_PASSWORD>` needs to be replaced by the user's password for the BMIA XNAT.

# Notes

Some scans might have a poor image quality or errors due to registration issues. We have marked this scans as 'unacceptable' scan quality in the XNAT database.
