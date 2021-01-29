import argparse
import os
import shutil
import sys

import xnat

XNAT_URL = "https://xnat.bmia.nl"
XNAT_PROJECT = "egd"
OUTPUT_DIRECTORY = "/output/"

parser = argparse.ArgumentParser(description="")

parser.add_argument("--username")
parser.add_argument("--password")
args = parser.parse_args()

folder_owner_uid = os.stat(OUTPUT_DIRECTORY).st_uid
folder_group_uid = os.stat(OUTPUT_DIRECTORY).st_gid

subjects_folder = os.path.join(OUTPUT_DIRECTORY, "SUBJECTS")
os.makedirs(subjects_folder, exist_ok=True)
shutil.chown(subjects_folder, user=folder_owner_uid, group=folder_group_uid)

metadata_folder = os.path.join(OUTPUT_DIRECTORY, "METADATA")
os.makedirs(metadata_folder, exist_ok=True)
shutil.chown(metadata_folder, user=folder_owner_uid, group=folder_group_uid)

license_file = os.path.join(OUTPUT_DIRECTORY, "DATA_LICENSE.pdf")


with xnat.connect(XNAT_URL, user=args.username, password=args.password) as session:
    project = session.projects[XNAT_PROJECT]
    print("Downloading metadata")
    for i_file in project.resources["PROJECT_DATA"].files.values():
        if "license" not in i_file.id:
            i_output_file = os.path.join(metadata_folder, i_file.id)
            i_file.download(i_output_file, verbose=False)
            shutil.chown(i_output_file, user=folder_owner_uid, group=folder_group_uid)
        else:
            i_file.download(license_file, verbose=False)
            shutil.chown(license_file, user=folder_owner_uid, group=folder_group_uid)

    print("Downloading subjects")
    subjects = project.subjects.values()

    for i_subject in subjects:
        subject_name = i_subject.label
        print("Now downloading data for subject {subject_id}".format(subject_id=subject_name))
        this_subject_folder = os.path.join(subjects_folder, subject_name)
        os.makedirs(this_subject_folder, exist_ok=True)
        shutil.chown(this_subject_folder, user=folder_owner_uid, group=folder_group_uid)

        subject_metadata_resource = i_subject.resources["METADATA"].files["metadata.json"]
        metadata_output_file = os.path.join(this_subject_folder, "metadata.json")
        subject_metadata_resource.download(metadata_output_file, verbose=False)
        shutil.chown(metadata_output_file, user=folder_owner_uid, group=folder_group_uid)

        experiment = i_subject.experiments["MR_" + subject_name]

        for i_scan in experiment.scans.values():
            scan_type = i_scan.type
            nifti_resource = i_scan.resources["NIFTI"].files[scan_type +".nii.gz"]
            nifti_output_file = os.path.join(this_subject_folder, nifti_resource.id)
            nifti_resource.download(nifti_output_file, verbose=False)
            shutil.chown(nifti_output_file, user=folder_owner_uid, group=folder_group_uid)
