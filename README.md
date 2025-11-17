# Coding Challenge – Python Assignments 1 & 2

This repository contains solutions for both assignments implemented in Python.

---

## Assignment 1 – Producer–Consumer with Thread Synchronization

### Description
Implements the classic **Producer–Consumer pattern** demonstrating thread synchronization and inter-thread communication.  
It uses a custom **bounded buffer** where producers add items and consumers remove them concurrently.  
Synchronization is handled using Locks and Condition variables.

### Testing Objectives
- Thread synchronization  
- Concurrent programming  
- Blocking queue behavior  
- Wait/Notify mechanism  

### How to Run
```bash
python -m assignment1.producer_consumer
```
### How to Test
```bash
python -m unittest discover -s assignment2/tests -p "test_*.py" -v
```
## Assignment 2 – CSV Data Analysis using Functional Programming
### Description

Develops a program that performs data aggregation and grouping operations on sales data using functional programming concepts.
The program reads from a CSV file and performs multiple analytical queries such as totals, groupings, and trends, and visualizes results with Matplotlib.

### Testing Objectives
- Functional programming
- Stream operations
- Data aggregation
- Lambda expressions
### How to Run
```bash
python -m assignment2.sales_analysis
```

### How to Test
```bash
python -m unittest discover -s assignment2/tests -p "test_*.py" -v
```
## Setup Instructions
### Clone the Repository
```bash
git clone https://github.com/yashiagar2507/Coding_Challenge.git
cd Coding_Challenge
``` 
### Ensure Python Version
### Make sure Python 3.10+ is installed.
### Install Dependencies
```bash
pip install matplotlib
```

### Run Programs and Tests

### Use the commands shown above to execute each assignment and its tests.

## Results

Assignment 1: Producer–Consumer program executes successfully with multiple producers and consumers.

Assignment 2: Sales analytics program runs correctly, printing aggregated results and displaying monthly revenue visualization.

All unit tests for both assignments pass successfully.
