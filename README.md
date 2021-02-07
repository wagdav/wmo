# Website Monitor

Periodically check website availability and store the results in a PostgreSQL
table.

## Getting started

The project is composed of two binaries `check` and `write` to check websites'
availability and write to the database, respectively.  The two programs
communicate via a shared Kafka topic.

The easiest way to run this project is using [nix][nix] because you don't have
to install anything separately.  In the project's root directory run the
following commands:

```
nix-build                   # build the project and put the results under ./results
./results/bin/check --help  # run the website checker
./results/bin/write --help  # run the database writer
```

If you cannot or don't want to use Nix, use [poetry][poetry]:

```
poetry run check --help
poetry run write --help
```

If the installation of `psycopg2` library fails, use your operating system's
package manager to install the PostgreSQL libraries.

## Walk-through using services hosted by aiven.io

### Create a Kafka service

Use the [Aiven console](https://console.aiven.io) to create a Kafka service.

Download the generated credentials and store them on the local disk in the
following directory layout:

```
<KAFKA-SERVICE-NAME>.aivencloud.com:24387
├── ca.pem
├── service.cert
└── service.key
```

The name of the directory corresponds to the generated URI of your Kafka
service.  This directory contains the SSL keys required for the connection.
Use restrictive permissions on these files (for example `chmod 600`).

The rest of the guide assumes you created this directory in your home
directory.

Create a new Kafka topic with the name `wmo`.

### Create a PostgreSQL service

Use the [Aiven console](https://console.aiven.io) to create a Kafka service.

Copy the generated PostgreSQL service URI and store it in an environment variable:

```
export POSTGRES_URI=postgres://<SERVICE-PASSWORD>@<POSTGRES-SERVICE-NAME>.aivencloud.com:24385/defaultdb?sslmode=require
```

Create the database table where the check results will be stored:

```
psql $POSTGRES_URI < scripts/create_db.sql
```

### Start the checker and writer

To start the checker run:

```
check --kafka ~/<KAFKA-SERVICE-NAME>.aivencloud.com:24387 \
    https://httpbin.org https://google.com https://wikpedia.org
```

In a separate terminal window start the writer

```
write --kafka ~/<KAFKA-SERVICE-NAME>.aivencloud.com:24387 --db $POSTGRES_URI
```

From the logs you should see that the two services communicate.  Monitor what
is written in the database table:

```
psql $POSTGRES_URI < scripts/list_results.sql
```

## Continuous builds

This project uses [GitHub Actions][./.github/workflows/test.yml] to validate
the following aspects in each pach:

* consistent style in the code (black, isort)
* conisstent style in other documents (yamllint, markdown)
* static analysis (flake8)
* unit tests pass

You can also all these checks locally:

```
nix-build -A checks.x86_64-linux
```

## Acknowledgements

I modeled the [flake.nix](./flake.nix) file after that of
[nixops](https://github.com/NixOS/nixops)

[nix]: https://nixos.org/guides/install-nix.html
[poetry]: https://python-poetry.org/docs/#installation
