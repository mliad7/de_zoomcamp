# Module 1 Homework: Docker & SQL

In this homework we'll prepare the environment and practice
Docker and SQL

When submitting your homework, you will also need to include
a link to your GitHub repository or other public code-hosting
site.

This repository should contain the code for solving the homework. 

When your solution has SQL or shell commands and not code
(e.g. python files) file formad, include them directly in
the README file of your repository.


## Question 1. Knowing docker tags

If you don't remember docker commands, you can always use
`--help`:

```bash
docker --help
```

You can do that for each subcommand like `build` and `run`:

```bash
docker build --help
```

Do the same for `docker run`.

Which subcommand does this?

*Remove one or more images*

- `delete`
- `rc`
- `rmi`
- `rm`

Answer : rmi

## Question 2. Understanding docker first run 

Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint `bash`.

What's the version of `pip` in the image?

- 24.3.1
- 24.2.1
- 23.3.1
- 23.2.1

Answer 24.3.1

##  Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from October 2019:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
```

You will also need the dataset with zones:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

Download this data and put it into Postgres.

You can use the code from the course. It's up to you whether
you want to use Jupyter or a python script.


## Question 3. Count records 

How many taxi trips were made on October 18th, 2019?

(Trips that started and finished on that day) 

- 13417
- 15417
- 17417
- 19417

Answer: 17417

```sql
SELECT
	COUNT(*) AS number_of_trips
FROM
	yellow_taxi_data
WHERE
	lpep_pickup_datetime::DATE = '2019-10-18'
	AND
	lpep_pickup_datetime::DATE = lpep_dropoff_datetime::DATE;
```


## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance. 

- 2019-10-11
- 2019-10-24
- 2019-10-26
- 2019-10-31

Answer: 2019-10-31

```sql
WITH RankedTrips AS (
    SELECT 
        lpep_pickup_datetime::DATE AS date, 
        trip_distance,
        ROW_NUMBER() OVER (PARTITION BY lpep_pickup_datetime::DATE ORDER BY trip_distance DESC) AS rank
    FROM 
        public.yellow_taxi_data
)
SELECT 
    date,
    trip_distance AS maxtrip
FROM 
    RankedTrips
WHERE
    rank = 1
ORDER BY 
    maxtrip DESC;
```

## Question 5. Three biggest pickup zones

Which where the top pickup locations with over 13,000 in
`total_amount` (across all trips) for 2019-10-18?

Consider only `lpep_pickup_datetime` when filtering by date.
 
- East Harlem North, East Harlem South, Morningside Heights
- East Harlem North, Morningside Heights
- Morningside Heights, Astoria Park, East Harlem South
- Bedford, East Harlem North, Astoria Park

Answer: East Harlem North, East Harlem South, Morningside Heights

```sql
SELECT
    z.location, 
    COUNT(y.PULocationID) AS num_of_pickup,
	SUM(y.total_amount) AS total_amount
FROM
    yellow_taxi_data y
JOIN zones z
    ON y.PULocationID = z.LocationID
WHERE
    lpep_pickup_datetime::DATE = '2019-10-18'
GROUP BY
    z.location
HAVING
    SUM(y.total_amount) > 13000
ORDER BY
    num_of_pickup DESC;
```

## Question 6. Largest tip

For the passengers picked up in Ocrober 2019 in the zone
name "East Harlem North" which was the drop off zone that had
the largest tip?

Note: it's `tip` , not `trip`

We need the name of the zone, not the ID.

- Yorkville West
- JFK Airport
- East Harlem North
- East Harlem South

Answer: Two possible answer

If october 2019

Answer is Upper East Side North

```sql
SELECT
    z2.location AS dropoff_location, 
    SUM(y.tip_amount) AS total_tip
FROM
    yellow_taxi_data y
JOIN zones z1
    ON y.PULocationID = z1.LocationID  
JOIN zones z2
    ON y.DOLocationID = z2.LocationID 
WHERE
    EXTRACT(YEAR FROM y.lpep_pickup_datetime) = 2019  
	AND EXTRACT(MONTH FROM y.lpep_pickup_datetime) = 10  
    AND z1.location = 'East Harlem North'
GROUP BY
    z2.location
ORDER BY
    total_tip DESC;
```

If October 18th 2019
Answer is East Harlem South

```sql
SELECT
    z2.location AS dropoff_location, 
    SUM(y.tip_amount) AS total_tip
FROM
    yellow_taxi_data y
JOIN zones z1
    ON y.PULocationID = z1.LocationID  
JOIN zones z2
    ON y.DOLocationID = z2.LocationID 
WHERE
    y.lpep_pickup_datetime::DATE = '2019-10-18'  
    AND z1.location = 'East Harlem North'
GROUP BY
    z2.location
ORDER BY
    total_tip DESC;
```

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](../../../01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the `main.tf` and `variable.tf` files run:

```bash
terraform apply
```

Paste the output of this command into the homework submission form.


## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw01
