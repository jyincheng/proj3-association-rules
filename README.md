# Project 3 - Apriori Algorithm (Association Rule)

## Contributor
* Yin Cheng (cc4717)
* Chi Wu (cw3326)

## Files
```
├── proj3.tar.gz
│   └── main.py
│   └── INTEGRATED-DATASET.csv
│   └── example-run.txt
│
├── README.md
```

## Executing Instruction

Unpack proj2.tar.gz in local.

```
tar -xzvf proj3.tar.gz
```

In proj3 directory, there is a `main.py`. Upload main.py to Google Cloud Platform by using user interface

<img src="./gcp.png" alt="tinder_recreation" style="zoom:80%;" />

Run main.py

```
python3 main.py
```

## Project Desgin

### Data Description
* Data set: [NYPD Hate Crimes]("https://data.cityofnewyork.us/Public-Safety/NYPD-Hate-Crimes/bqiq-cu78")

* Data processing Procedure: We keep the following attributes because we want to see the association rule among them. We might get a result of certain offense category cases often happen in certain county. For example, anti-female cases is associated with county King. We can provide information to raise safety matters.
    * County
    * Law Code Category Description
    * Offense Description
    * PD Code Description
    * Bias Motive Description
    * Offense Category

### Related Functions:
* `read_data()`: To read data from `INTEGRATED-DATASET.csv`
* `create_next_candidates()`: 
* `find_all_items()`: Create a dictionary with item as key and support value as value.
* `construct_L1`: Create a set of large frequency item.
* `apriori`: Update `items_to_support` with items which supoort value is larger than or eqaul to `MIN_SUPPORT`.
* `find_associate_rules`: Create association rules which confidence value is larger than or equal to `MIN_CONFIDENCE`.
* `print_associate_rules`: Print association rules.
* `output_example_txt`: Output example to `example-run.txt`.

### Variable Initialization
* `MIN_SUPPROT`: 0.01
* `MIN_CONFIDENCE`: 0.6


### Main Operations
#### Step 1: Find all Items
* `items_to_support`: a dictionary stores every items appeared in the data set as key and support value as value; `{item1: 0.03, item2: 0.02, ...}`

#### Step 2: Construct largest One-item Set
* Traverse all sorted item and store item with support value which is larger than or eqaul to the `MIN_SUPPORT` into `L1`.

#### Step 3: Calculate Support Value with Apriori Algorithm
* Update `items_to_support` with `apriori()` function. In this function, we return items with support value which is larger than or eqaul to `MIN_SUPPORT`.

#### Step 4: Find Association Rules
* For each combination in dictionary `items_to_support`, we generated association rules with confidence value larger than or eqaul to `MIN_CONFIDENCE`.

#### Step 5: Print Association Rules & Output Example Text
* Print association rules and output example text using association rules generated from `Setp 4`.


## Result
.. to be done ..


## Google Crendential
* API_KEY = "AIzaSyCm7IbxyiUyAYGywbz9gxw3rnHR0rIIQbI"
* ENGINE_ID = "a726fb79aeb1e8c10"

## Reference
* 