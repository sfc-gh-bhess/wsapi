# Example Websocket API in Snowpark Container Services
This is a simple websocket API. It queries the TPC-H 100 
data set and returns the top sales clerks. The API allows
you to restrict the range of the sales data and to determine 
how many top clerks to return.

# Setup
This example requires importing the `SNOWFLAKE_SAMPLE_DATA`
data share, and an account with Snowpark Container Services
enabled.

1. Follow the "Common Setup" [here](https://docs.snowflake.com/en/LIMITEDACCESS/snowpark-containers/tutorials/common-setup)
2. In a SQL Worksheet, execute `SHOW IMAGE REPOSITORIES` and look
   for the entry for `TUTORIAL_DB.DATA_SCHEMA.TUTORIAL_REPOSITORY`.
   Note the value for `repository_url`.
3. Create the compute pool:
   ```sql
   USE ROLE ACCOUNTADMIN;

   CREATE COMPUTE POOL frontend_compute_pool
      MIN_NODES = 1
      MAX_NODES = 1
      INSTANCE_FAMILY = CPU_X64_XS;
   GRANT USAGE, MONITOR ON COMPUTE POOL frontend_compute_pool TO ROLE test_role;
   ```
4. In the main directory of this repo, execute 
   `bash ./configure.sh`. Enter the URL of the repository that you
   noted in step 2 for the repository. Enter the name of the warehouse
   you set up in step 1 (if you followed the directions, it would be
   `tutorial_warehouse`). Enter the name of the compute pool you set
   up in step 3.
4. Log into the Docker repository. You can run `make login` or, if you
   have MFA enabled, you can use SnowCLI to login to the image-registry.
5. Build the Docker image and push the image to the repository by 
   running `make all`.
5. Create the service by executing the DDL. You can get this DDL
   by running `make ddl`:
```
CREATE SERVICE wsapi
  IN COMPUTE POOL tutorial_compute_pool
  FROM SPECIFICATION $$
spec:
  containers:
    - name: wsapi
      image: <REPO_URL>/wsapi
  endpoints:
    - name: wsapi
      port: 8080

  $$
  QUERY_WAREHOUSE='<WAREHOUSE>'
;
```
6. See that the service has started by executing `SHOW SERVICES IN COMPUTE POOL tutorial_compute_pool` and `SELECT system$get_service_status('wsapi')`.
8. Find the public endpoint for the service by executing `SHOW ENDPOINTS IN SERVICE st_spcs`.
9. Grant permissions for folks to visit the Streamlit. You do this by granting 
   the SERVICE ROLE: `GRANT SERVICE ROLE wsapi!wsapi TO ROLE some_role`, 
   where you specify the role in place of `some_role`.

## Test the API
This repo comes with a websocket client app to test the websocket
API we stood up in SPCS, `wsclient.py`. The Python requirements for
this app are in `requirements.txt`.

For now, we will use a username/password to get a token to access
the websocket programmatically. The `wsclient.py` app expects these
credentials in environment variables:
* `SNOWFLAKE_ACCOUNT` - the account locator for the Snowflake account
* `SNOWFLAKE_USER` - the Snowflake username to use
* `SNOWFLAKE_PASSWORD` - the password for the Snowflake user
* `SNOWFLAKE_HOST` - the host URL for the Snowflake account (typically, `https://SNOWFLAKE_ACCOUNT.snowflakecomputing.com`)

The application takes the following arguments:
* `--url` - the websocket endpoint, which is `wss://ENDPOINTURL/ws/`, where `ENDPOINTURL` is the URL returned in step 8. This is required.
* `--start_date` - the starting date range for the query. Default is `1995-01-01`.
* `--end_date` - the ending date range for the query. Default is `1993-05-31`.
* `--topn` - the number of results to return. Default is `10`.

The application will print one JSON object for each result:
```
{'O_CLERK': 'Clerk#000007713', 'CLERK_TOTAL': 13388146.35}
{'O_CLERK': 'Clerk#000002975', 'CLERK_TOTAL': 13152602.76}
{'O_CLERK': 'Clerk#000004087', 'CLERK_TOTAL': 13019096.68}
{'O_CLERK': 'Clerk#000005062', 'CLERK_TOTAL': 12919950.95}
{'O_CLERK': 'Clerk#000008155', 'CLERK_TOTAL': 12889351.77}
{'O_CLERK': 'Clerk#000008276', 'CLERK_TOTAL': 12881330.2}
{'O_CLERK': 'Clerk#000008400', 'CLERK_TOTAL': 12852466.07}
{'O_CLERK': 'Clerk#000001038', 'CLERK_TOTAL': 12777510.93}
{'O_CLERK': 'Clerk#000004235', 'CLERK_TOTAL': 12759892.92}
{'O_CLERK': 'Clerk#000000766', 'CLERK_TOTAL': 12746685.43}
```

## Local Testing
This API can be tested running locally. To do that, build the
image for your local machine with `make build_local`.

In order to run the web app in the container, we need to set some 
environment variables in our terminal session before running the 
container. The variables to set are:
* `SNOWFLAKE_ACCOUNT` - the account locator for the Snowflake account
* `SNOWFLAKE_USER` - the Snowflake username to use
* `SNOWFLAKE_PASSWORD` - the password for the Snowflake user
* `SNOWFLAKE_WAREHOUSE` - the warehouse to use
* `SNOWFLAKE_DATABASE` - the database to set as the current database (does not really matter that much what this is set to)
* `SNOWFLAKE_SCHEMA` - the schema in the database to set as the current schema (does not really matter that much what this is set to)

Once those have been set, run the API container with `make run`. This will 
use Docker Compose to start the container to host the API. 

There is a `wsclient_local.py` that you can use with this local container.
For the `--url`, use `ws://localhost:8080/ws/`.
