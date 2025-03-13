import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def graphdata(data_path):
    """Function for graphing IMDb ratings by Bond car manufacturers."""
    with sqlite3.connect(data_path) as con:
        df = pd.read_sql_query(''' 
            SELECT Bond_Car_MFG, AVG(Avg_User_IMDB) as Bond_AVG
            FROM movies
            GROUP BY Bond_Car_MFG;
        ''', con)  # Querying the data, sorting it, and grouping it as requested in the lab.

    print(df)

    # Setting the car manufacturer as the index and plotting
    df.set_index('Bond_Car_MFG', inplace=True)  
    df.plot(kind='bar', legend=False, color='teal')  # Customizing the Graph.

    # Adding labels and title to the graph
    plt.xlabel('Bond Car Brands')
    plt.ylabel('Average IMDb Rating')
    plt.title('Average IMDb Ratings for Each Bond Car Manufacturer')
    plt.tight_layout()  # Adjust layout to fit the graph
    plt.show()

def singlerecord(data_path):
    """Function that takes the inputted year, searches for the record, and returns the requested movie data."""
    with sqlite3.connect(data_path) as con:
        movie_year = input("Please enter the James Bond movie release year: ")
        
        cur = con.cursor()
        data = '''SELECT Year, Movie, Bond FROM movies WHERE Year = ?;'''
        cur.execute(data, (movie_year,))

        record = cur.fetchone()
        
    return [record] if record else []

def main():
    """Main function where everything is processed."""
    data_path = 'bond_movies.db'

    # Fetch and display movie data based on user input year
    record = singlerecord(data_path)

    if record:
        for year, movie, bond in record:
            print(f'In  {year} the movie was been released and the tittle of the  movie is {movie} and the actor is {bond}')
    else:
        print("Movie either doesn't exist or isn't in the database.")

    # Generate the graph for average IMDb ratings by car manufacturer
    graphdata(data_path)

if __name__ == '__main__':
    main()
