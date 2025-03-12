"""Norlon Sibug Lab 8.1: Create a Database Table and Insert Data from a CSV File"""
import sqlite3
import pandas as pd

def movies_table(con):
    """Function to create the 'movies' table in the database."""
    cur = con.cursor()

    create_bond_table_setup = '''CREATE TABLE IF NOT EXISTS movies ( 
    ID INTEGER NOT NULL UNIQUE,
    Year INTEGER NOT NULL,
    Movie TEXT NOT NULL UNIQUE,
    Bond TEXT NOT NULL,
    Bond_Car_MFG TEXT,
    Depicted_Film_Loc TEXT,
    Shooting_Loc TEXT,
    BJB INTEGER,
    Video_Game BOOLEAN,
    Avg_User_IMDB REAL,
    PRIMARY KEY("ID" AUTOINCREMENT)
    )'''
    cur.execute(create_bond_table_setup)  # Execute the SQL to create the table
    con.commit()

def data_into_table(con, bond_csv):
    """Function to insert data from a CSV file into the 'movies' table."""
    bond_data = pd.read_csv(bond_csv)  # Load CSV data into a DataFrame

    # Check if data is already inserted into the table
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM movies')
    if cur.fetchone()[0] < 1:
        # Insert data into the database from the CSV file
        for row in bond_data.itertuples(index=False):
            cur.execute('''INSERT INTO movies (
                Year, Movie, Bond, Bond_Car_MFG, Depicted_Film_Loc, Shooting_Loc, 
                BJB, Video_Game, Avg_User_IMDB)
                VALUES (?,?,?,?,?,?,?,?,?)''', 
                (row.Year, row.Movie, row.Bond, row.Bond_Car_MFG, row.Depicted_Film_Loc,
                 row.Shooting_Loc, row.BJB, row.Video_Game, row.Avg_User_IMDB))

        # Insert 'No Time to Die' directly
        cur.execute('''INSERT INTO movies 
        (Year, Movie, Bond, Bond_Car_MFG, Depicted_Film_Loc, Shooting_Loc, 
        BJB, Video_Game, Avg_User_IMDB)
        VALUES (2021, 'No Time to Die', 'Daniel Craig', 'Aston Martin',
        'Italy, Norway, Jamaica, UK, Faroe Islands', 'Norway, Italy, UK, Jamaica', 
        0, 0, 7.3)''')
        con.commit()

def main():
    """Main function to execute the operations."""
    data_path = 'bond_movies.db'  # Database name
    bond_csv = 'jamesbond.csv'  # CSV file path

    # Create the database connection
    con = sqlite3.connect(data_path)

    # Create the movies table
    movies_table(con)

    # Insert data into the table
    data_into_table(con, bond_csv)

    # Print the records from the movies table
    print(pd.read_sql_query('''SELECT Year, Movie, Bond, Bond_Car_MFG, 
    Depicted_Film_Loc, Shooting_Loc, BJB, Video_Game, Avg_User_IMDB 
    FROM movies''', con))

    # Close the database connection
    con.close()

if __name__ == "__main__":
    main()
