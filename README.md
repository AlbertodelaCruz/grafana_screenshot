## Grafana Screenshot

This app gets a graph from a Grafana instance, makes a screenshot and post it to slack.

## Configuration

An `.env.example` file is included with needed variables

```
GRAFANA_URL "Full grafana url dashboard
GRAFANA_USERNAME 
GRAFANA_PASSWORD
SLACK_BOT_TOKEN "It should starts with xoxb
SLACK_CHANNEL 
``````

### How to run it

Just launch `run_app.sh` script. 

It will raise up dependencies and also a container running the code.
