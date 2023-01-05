[![Python package](https://github.com/ceesvandegriend/swrf/actions/workflows/main.yml/badge.svg)](https://github.com/ceesvandegriend/swrf/actions/workflows/main.yml)

# swrf / Sorrowful

Check that the home network is connected to the internet by the main 
connection and not by the fall-back connection.

## MessageQueue

1. Run Apache ActiveMQ

2. Try to connect to a public, well known website and publish the result to a MessageQueue `topic`. 
   Multiple checks may publish to the MQ `topic`

3. A subscriber receives the message from the `topic`.

Multiple receivers may connect to the `topic`.
   * To store the checks in a database
   * To notify when the main connection is down

## Containers
Each component runs seperate in a container.

1. ActiveMQ

2. Publisher for Google.com checks

3. Subscriber for the checks to record them in a SQLite database

4. Subscriber for the checks to notify by email
