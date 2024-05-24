
# COVID-19 Dashboard

This project is a COVID-19 dashboard that visualizes the confirmed cases data from the CSSEGISandData repository.

## Installation

1. Clone the repository or download the ZIP file.
2. Navigate to the project directory.
3. Create a virtual environment (optional):
4. Install the required packages:

```sh
pip install -r requirements.txt
```

## Running the App

Run the application:

```sh
python app.py
```

Open your web browser and go to http://127.0.0.1:8050/.

## Dependencies
- pandas
- dash
- plotly

## Report

## Data Extraction and Manipulation Process
### Data Extraction
The data was extracted directly from the GitHub repository using the following URL:

```python
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
```

Using the pandas library, the CSV file was read into a DataFrame:

```python
df = pd.read_csv(url)
```

### Data Preparation
After loading the data, the next step was to prepare it for visualization.

#### Grouping and Summing
The data was grouped by the 'Country/Region' column to aggregate the total confirmed cases for each country. This was achieved using the groupby method followed by summation:

```python
df_grouped = df.groupby('Country/Region').sum()
```

#### Data Cleaning
The dataset included columns such as 'Province/State', 'Lat', and 'Long', which were not necessary for this analysis. These columns were dropped to clean the data:

```python
df_grouped = df_grouped.drop(columns=['Province/State', 'Lat', 'Long'], errors='ignore')
```

#### Sorting
To identify the countries with the highest number of confirmed cases, the data was sorted based on the latest date's total confirmed cases in descending order:

```python
df_sorted = df_grouped.sort_values(by=df_grouped.columns[-1], ascending=False)
```

#### Selecting Top 5 Countries
Finally, the top 5 countries with the highest total confirmed cases were selected for visualization:

```python
top_5_countries = df_sorted.head()
```

## Challenges and Solutions
Building the COVID-19 dashboard presented several challenges along the way. However, through determination and problem-solving, I was able to overcome these obstacles.

### Cleaning and Transforming Data
**Challenge**: The dataset contained unnecessary columns that could potentially hinder the application's performance.

**Solution**: I carefully analyzed the data and identified the irrelevant columns. After removing them, the data was much cleaner and more manageable.

### Updating Data Dynamically
**Challenge**: Ensuring the visualizations updated seamlessly based on user input was a crucial requirement.

**Solution**: While implementing the callback functions in Dash was initially daunting, I persevered and eventually mastered the concept. This allowed me to create a smooth and responsive user experience.

### Accurate Visualizations
**Challenge**: Representing the data accurately and creating clear, informative visualizations was a top priority.

**Solution**: I spent considerable time experimenting with different visualization techniques in Plotly. Through trial and error, I was able to create visuals that not only accurately portrayed the data but also provided an interactive and engaging experience for users.

## Conclusion
Developing the COVID-19 dashboard was a challenging yet rewarding journey. Despite the obstacles I faced, I remained determined and found creative solutions to overcome them. By leveraging the libraries of Python, Dash, and Plotly, I was able to create a dynamic and insightful tool for tracking and analyzing COVID-19 confirmed cases.