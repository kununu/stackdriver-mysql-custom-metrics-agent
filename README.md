# How to run
* First make sure you have a GCP service account set up and the credentials file ready as `google-creds.json`. The account needs permission to push metric data to Google Stackdriver
* Get your Google Cloud Project Id ready, you'll need it in the next step. Of course Stackdriver Monitoring needs to be enabled on your project.
* Create a configuration file:
```bash
$ cat > config.yaml <<EOF
google_project_id: some-123456
labels_from_env:
    pwd: PWD
labels:
    server: "staging"
connection:
    host: 127.0.0.1
    port: 3306
    user: root
    password: secret
    db: information_schema
metrics:
- name: "Check if the database is up"
  type: "database/general/is-up"
  query: >
    SELECT 1
EOF
```
Or alternatively set the following environment variables:
```
GOOGLE_PROJECT_ID=some-123456
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=secret
DB_NAME=information_schema
```
* Build the docker image
```bash
docker-compose build
```
* Run the docker image
```bash
docker-compose up
```
