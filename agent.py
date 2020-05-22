#!/usr/bin/env python3

import datetime
import os
import pymysql
import sys
import time
import yaml

from google.cloud import monitoring_v3

def apply_substitutions(query, substitutions):
    for key, val in substitutions.items():
        target = "{%s}" % key
        query = query.replace(target, val)

    return query

def fetch_metric(connection, query, metric, labels):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()[0]

    series = monitoring_v3.types.TimeSeries()
    series.metric.type = "custom.googleapis.com/{}".format(metric)
    series.resource.type = "global"

    for key, val in labels.items():
        series.metric.labels[key] = val

    point = series.points.add()
    point.value.double_value = result
    point.interval.end_time.seconds = int(time.time())

    return (series, result)

def main():
    with open(sys.argv[1], "r") as stream:
        config = yaml.load(stream)

    if not "google_project_id" in config:
        config["google_project_id"] = os.environ["GOOGLE_PROJECT_ID"]

    if not "connection" in config:
        config["connection"] = {
            "host": os.environ["DB_HOST"],
            "port": int(os.environ["DB_PORT"]),
            "user": os.environ["DB_USER"],
            "password": os.environ["DB_PASSWORD"],
            "db": os.environ["DB_NAME"],
        }

    if not "labels" in config:
        config["labels"] = {}

    if "labels_from_env" in config:
        for key, val in config["labels_from_env"].items():
            config["labels"][key] = os.environ[val]

    connection = pymysql.connect(**config["connection"])
    client = monitoring_v3.MetricServiceClient()
    project = client.project_path(config["google_project_id"])

    for metric in config["metrics"]:
        if not "labels" in metric:
            metric["labels"] = {}

        query = apply_substitutions(metric["query"], config["labels"])

        try:
            (series, result) = fetch_metric(
                connection,
                query,
                metric["type"],
                {**config["labels"], **metric["labels"]})
            client.create_time_series(project, [series])
        except BaseException as ex:
            result = ex

        print(datetime.datetime.now(), metric["type"], result)

    connection.close()

if __name__ == "__main__":
    main()
