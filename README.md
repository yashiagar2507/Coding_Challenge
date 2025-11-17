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
python -m unittest discover -s assignment1/tests -p "test_*.py" -v
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

## Sample Output

### Assignment 1 – Producer–Consumer
=== Fast Producer–Consumer Demo ===
Dict Data: produced=20, consumed=20
Tuple Data: produced=20, consumed=20
Dataclass Orders: produced=10, consumed=10
Nested JSON: produced=10, consumed=10

--- Multi-Producer Test ---
Total produced: 30, consumed: 30

### Assignment2
=== SALES ANALYTICS REPORT ===
Total Records: 120
Total Revenue: $104,575.50

Revenue by Region:
  North      $28,642.50
  South      $28,383.50
  East       $36,495.00
  West       $11,054.50

Top 5 Products by Revenue:
  Phone           $27,720.00
  Laptop          $16,560.00
  Camera          $12,302.50
  Tablet          $9,690.00
  Headphones      $8,034.00

Highest Order Value: Order O81 → $4,320.00


## Results

Assignment 1: Producer–Consumer program executes successfully with multiple producers and consumers.

Assignment 2: Sales analytics program runs correctly, printing aggregated results and displaying monthly revenue visualization.

All unit tests for both assignments pass successfully.


## Author
**Yashi Agarwal**  
[GitHub Profile](https://github.com/yashiagar2507)
