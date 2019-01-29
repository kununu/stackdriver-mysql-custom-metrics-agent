#!/usr/bin/env python3

import datetime
import os
import pymysql
import sys
import time
import yaml

from google.cloud import monitoring_v3

def fetch_metric(connection, query, metric):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()[0]

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

    if not "google_project_id" in config:
        config["google_project_id"] = os.environ["GOOGLE_PROJECT_ID"]

    if not "connection" in config:
        config["connection"] = {
            "host": os.environ["DB_HOST"],
            "port": os.environ["DB_PORT"],
            "user": os.environ["DB_USER"],
            "password": os.environ["DB_PASSWORD"],
            "db": os.environ["DB_NAME"],
        }

    connection = pymysql.connect(**config["connection"])
    client = monitoring_v3.MetricServiceClient()
    project = client.project_path(config["google_project_id"])

    for metric in config["metrics"]:
        try:
            result = fetch_metric(connection, metric["query"], metric["type"])
            client.create_time_series(project, [result])
        except BaseException as ex:
            result = ex

        print(datetime.datetime.now(), metric, result)

    connection.close()

if __name__ == "__main__":
    main()
