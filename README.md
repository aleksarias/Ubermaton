# Ubermaton
A rideshare system for autonomous vehicles

## Description
The current application only has a cli. The cli can be used to simulate what the autonomous vehicle would do if its
movements and user requests occur in "step units". The app only has in memory persistence so once the cli is terminated
all data is lost.
The application was designed using domain driven principles. This makes it easy to switch out in memory repos with 
other types of persistence like mongo or a relational/sql variant.

## Requirements
 - pipenv
 - python 3.7

## Installation

 - git clone https://github.com/aleksarias/Ubermaton/
 - pipenv install 
 - pipenv shell 
 
 ## Running the command line interface
 - python cli.py
 
 ## Project Structure
 - domain: all business specific data models
 - infrastructure: all io for domain
 - usecases: specific unit of work for the application
 
 ## Application Domain Models
 
 - Person: Stores data on users of the autonomous vehicle
 - Vehicle: Stores the state of the car and its planned itinerary
 - LocationMap: Used to calculate distances and shortests paths... essentially the map that's used by the vehicle for 
 navigating
 
 ## TODO
 
 - Cleanup interfaces, need to transport more data on per call rather than performing many calls to get data
 - Create better command line tool. Used cmd2 which has too limited features to design a good cli for this application
 - Complete writing tests for full coverage
 - Complete google LocationMap gateway in order for the app to be used in a more "real world" way
 - Complete mongo persistence 
 