#! /usr/bin/env python3
"""Run deid-export on session "2025-03-31 13_43_10"

    This script was created to run Job ID 67ffd20bcb00d1892881ddf8
    In project "flywheel/test"
    On Flywheel Instance https://fw.mrrc.upmc.edu/api
"""

import os
import argparse
from datetime import datetime


import flywheel


input_files = {
    "deid_profile": {"container_path": "flywheel/test", "location_name": "deid.yaml"}
}


def main(fw):
    gear = fw.lookup("gears/deid-export")
    print("gear.gear.version in original job was = 1.8.0")
    print(f"gear.gear.version now = {gear.gear.version}")
    print("destination_id = 67f941ae42d06f9c707d7fb2")
    print("destination type is: session")
    destination = fw.lookup("flywheel/test/FAKE123/2025-03-31 13_43_10")

    inputs = dict()
    for key, val in input_files.items():
        if val["container_path"][:8] == "analysis":
            path = val["container_path"][9:]
            parent_of_analysis = fw.lookup(path)
            # find analysis that has the right file
            analyses = parent_of_analysis.reload().analyses
            for analysis in analyses:
                for file in analysis.files:
                    if file.name == val["location_name"]:
                        container = analysis
        else:
            container = fw.lookup(val["container_path"])
        inputs[key] = container.get_file(val["location_name"])

    config = {
        "debug": True,
        "overwrite_files": "Replace",
        "project_path": "flywheel/deid-test",
    }

    tags = ["deid-export"]

    now = datetime.now()
    analysis_label = (
        f'{gear.gear.name} {now.strftime("%m-%d-%Y %H:%M:%S")} SDK launched'
    )
    print(f"analysis_label = {analysis_label}")

    analysis_id = gear.run(
        analysis_label=analysis_label,
        tags=tags,
        config=config,
        inputs=inputs,
        destination=destination,
    )
    print(f"analysis_id = {analysis_id}")
    return analysis_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()

    fw = flywheel.Client("")
    print(fw.get_config().site.api_url)

    analysis_id = main(fw)

    os.sys.exit(0)
