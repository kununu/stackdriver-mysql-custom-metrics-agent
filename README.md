```bash
# if you don't have it, install virtualenv
$ pip3 install virtualenv

$ cat > config.yaml <<EOF
settings:
    database_url: "mysql://username:password@host:port/dbname"
    google_cloud_project_id: "some-12345"
    #uncomment and provide path if a google cloud service account is available
    #google_application_credentials: "/google-creds.json"
metrics:
- name: "Check of the database is up"
  type: "database/general/is-up"
  query: >
    SELECT 1
EOF

$ virtualenv .
$ bin/activate
$ pip3 install -U -r requirements.txt

# authenticate if in dev mode and we don't have a google cloud service account
$ gcloud auth application-default login
$ gcloud auth login

# run it manually or set it up with a cron
$ ./agent.py config.yaml
```

OR

```bash
docker build -t stackdriver-mysql-custom-metrics-agent .
docker run -d -v $PWD/config.yml:/config.yml -v $PWD/google-creds.json:/google-creds.json stackdriver-mysql-custom-metrics-agent
```
