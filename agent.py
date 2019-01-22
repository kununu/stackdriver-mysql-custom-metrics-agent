#!/usr/bin/env python3

import sys
import os
import urllib.parse
import yaml
import pymysql
import time

from google.cloud import monitoring_v3

def fetch_metric(connection, query, metric):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()[0]

    print(metric, result)

    series = monitoring_v3.types.TimeSeries()
    series.metric.type = "custom.googleapis.com/{}".format(metric)
    series.resource.type = "global"

    point = series.points.add()
    point.value.double_value = result
    point.interval.end_time.seconds = int(time.time())

    return series

def main():
    with open(sys.argv[1], "r") as stream:
        config = yaml.load(stream)

    # set up google cloud service account if we have one
    if "google_application_credentials" in config["settings"]:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config["settings"]["google_application_credentials"]

    database_config = urllib.parse.urlparse(config["settings"]["database_url"])

    connection = pymysql.connect(
        host=database_config.hostname,
        port=database_config.port,
        user=database_config.username,
        password=database_config.password,
        db=database_config.path.strip("/")
    )

    client = monitoring_v3.MetricServiceClient()
    project = client.project_path(config["settings"]["google_cloud_project_id"])

    for metric in config["metrics"]:
        client.create_time_series(project,
            [fetch_metric(connection, metric["query"], metric["type"])])

    connection.close()

if __name__ == "__main__":
    main()
