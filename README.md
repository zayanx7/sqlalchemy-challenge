# sqlalchemy-challenge
## Overview
This project involves conducting a climate analysis of Honolulu, Hawaii, and creating a Flask API to provide access to the analysis results. The analysis includes exploring precipitation and temperature data, as well as designing a Flask API with specific routes to query and present the data.

## Project Structure

The project consists of two main parts:

### Climate Analysis

The analysis is performed using Python, SQLAlchemy, and various data manipulation libraries.
Data from the provided hawaii.sqlite database is used to conduct the analysis.
The analysis includes:
Precipitation analysis.
Station analysis.
Calculation of temperature statistics.
Creation of temperature observation histograms.
The analysis results are used to answer specific questions and generate insights about the climate in Honolulu.

### Flask API
A Flask API is created to provide access to the analysis results through web-based endpoints.
The following routes are defined in the API:
/api/v1.0/precipitation - Retrieves precipitation data for the last 12 months.
/api/v1.0/stations - Lists all available weather stations.
/api/v1.0/tobs - Retrieves temperature observations for the most active station in the last year.
/api/v1.0/<start> - Provides temperature statistics (TMIN, TAVG, TMAX) for dates greater than or equal to a specified start date.
/api/v1.0/<start>/<end> - Provides temperature statistics for a specified date range.
The API returns data in JSON format.
