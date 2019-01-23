# How to run
* First make sure you have a GCP service account set up and the credentials file ready as `google-creds.json`. The account needs permission to push metric data to Google Stackdriver
* Get your Google Cloud Project Id ready, you'll need it in the next step. Of course Stackdriver Monitoring needs to be enabled on your project.
* Create a configuration file:
```bash
$ cat > config.yaml <<EOF
google_cloud_project_id: some-123456
connection:
    host: 127.0.0.1
    port: 3306
    user: root
    password: secret
    db: information_schema
metrics:
- name: "Check of the database is up"
  type: "database/general/is-up"
  query: >
    SELECT 1
EOF
```
* Build the docker image
```bash
docker-compose build
```
* Run the docker image
```bash
docker-compose up
```
