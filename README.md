# How to run the project

## Get started

Put a `.env` file into the `src/core` directory. You can start with a template file:

```
cp src/core/.env.ci src/core/.env
```

Run the containers with
```
make run
```

and then run the installation script with:

```
make install
```

## Tests

`make test`

## Linter

`make lint`

# Technical and design solutions

## Technical solutions
Transaction Outbox pattern is used in order to guarantee
reliable events delivery to Clickhouse. There is how it works:
1. There is a PostgreSQL table where the events are stored during
   the main transaction.
2. Celery background process reads the events from Outbox and sends
   them to Clickhouse.
3. In case of error, background process tries to send evens again.

## Design solutions
The main goal is establishing ACID for Clickhouse insert
operations, since Clickhouse does not support transactions. So
the simplest solution is using the existing RDB, i.e. PostgreSQL.
Since Celery is already used in the project, it fits well for some
kind of a background process for sending logs to Clickhouse. Also
Celery is quite simpler than other similar libraries. Finally,
struclog and Sentry are used for handling Celery task errors as
it is described in provided documentation.
