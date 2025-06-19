***Welcome to near neighbors queries for Fréchet distance project!***

The purpose of this project is to find similar curves to a query curve using the Fréchet distance as metric. We implement both the classic Alt and Godau algorithm from 1995 (Paper title: Computing the Fréchet distance between two polygonal curves) and the modern Baldus and Bringmann algorithm from 2017 (Paper title: A fast implementation of near neighbors queries for Frechet distance (GIS Cup)).

**Programming Language**

Python is used. Not ideal for a lot of iterations but awesome variety of useful packages like Numpy and matplotlib. Also used because of its simplicity, since we want to focus on the algorithms themselfs and not waste time defining variables and using parenthesis. 

**csv files**

The csv files are used as our databaseses. Each csv file contains polygonal curves, a collection of points (x,y). Each line holds the points of 1 polygonal curve seperated by (x1,y1) | (x2,y2) | (x3,y3) ..... etc. The first line is used for labels. Those could be x y or latitude longtitude or whatever you want. The code will skip the first line. 

Several database files are provided to test the code. When the file ends with two numbers like: generated_curves_10_30, the 10 and 30 are the min and max number of points per polygonal curve. Each curve have some random number of points between those values. On the other hand, csv files with one number are a collection of said number curves with fixes 10-30 points. 

The query_dataset holds the query curves.

!!!You can create your own database with any polygonal curves but please remember to follow the guidlines mentioned above or the code will fail!!!

**Code files**

The code is logically split into the classic and the modern algorithms. Files starting with classic holds functions used to find the classic Frechet distance. Files starting with modern holds function used to find the modern distance. Each file name describes what type of functions each file contains. In the end there are a couple of visualize files to create graphs. 

**How to run the code**

Some file contains only functions while other can be run. Below we describe the files you can actually run. In order to do so, you need: 

- Python 
- A python virtual enviroment with requirements.txt installed. (Its just Numpy and matplotlib for visualize files).
- Terminal

On to the files that can be run. The arguments are mostly the same every time:


- classic_Frechet_distance.py

This file executes the classic algorithm and requires 4 arguments. 1) The database name, 2) the number of database curves you want to use (as mentioned we ignore the first row so it will start counting from second row.), 3) the query curve database name and 4) the query curve. 

Example (Windows, linux could be python3): python classic_Frechet_distance.py generated_curves_10_30.csv 100 query_dataset.csv 0

- modern_lower_bound.py

A fifth parameter is added, the delta threshold.

Example: python modern_lower_bound.py generated_curves_10_30.csv 100 query_dataset.csv 0 0.01

- modern_positive_filter.py

Example: python modern_positive_filter.py generated_curves_10_30.csv 100 query_dataset.csv 0 0.01

- modern_negative_filter.py

Example: python modern_negative_filter.py generated_curves_10_30.csv 100 query_dataset.csv 0 0.01

- modern_Frechet_distance.py

No threshold here. We execute the recursive algorithm.

Example: python modern_Frechet_distance.py generated_curves_10_30.csv 100 query_dataset.csv 0

- modern_vs_classic.py

Example: python modern_vs_classic.py generated_curves_10_30.csv 100 query_dataset.csv 0 0.01

- visualize_database.py

You will see a visualization of your database curves in 2D space.

Example: python visualize_dataset.py geolife_trajectories_under_5km.csv 100 query_dataset.csv 1

- visualize_results.py

This one will uses the file results.txt created by the modern_vs_classic.py. So no parameters are needed. Just run it.

Example: python visualize_results.py


Have fun! For full explanation of the code and the Frechet distance, check the pdf (its in Greek, sorry.).
The pdf explaining everything can be found here: http://users.uoa.gr/~chrzacharis/Papers/papers.html

