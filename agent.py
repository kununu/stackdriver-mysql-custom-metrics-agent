#!/usr/bin/env python3

import sys
import os
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

    connection = pymysql.connect(**config["connection"])
    client = monitoring_v3.MetricServiceClient()
    project = client.project_path(config["google_cloud_project_id"])

    for metric in config["metrics"]:
        client.create_time_series(project,
            [fetch_metric(connection, metric["query"], metric["type"])])

    connection.close()

if __name__ == "__main__":
    main()
