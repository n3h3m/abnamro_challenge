## ABN AMRO Coding Challenge:
This Python script tries to address the challenge in parsing and generating a summary report based on input files that contain executed trade details. 

However this program can be easily re-purposed to add more business logic to parse and process any ad-hoc report. 

### Workflow:

The workflow roughly follows as below:

               A                               B                          C                                 D
    +------------------------+     +------------------------+     +-------------------------+      +------------------+
    | Fields configuration   |     |Input file              |     |Business logic           |      | Output file      |
    |   Contains fieldnames  +---->| Contains fixed         +---->|  Often groupby          +----->|   Ideally .csv   |
    |     start,end positions|     |   Width parseable data |     |    Or other aggregation |      |                  |
    +------------------------+     +------------------------+     +-------------------------+      +------------------+
    
    
    
### Pandas:
Due to the nature of the problem scenario it is a good decision to make use of of Pandas library for Python. As Pandas makes most of the data handling easier especially here in parsing fixed-width datafiles, dealing with aggregation and grouping, also outputting to csv file. We will be using the latest Pandas version 1.3.4 however any previous version would work smoothly since the functionality used here are very basic to Pandas. 

The entire report can be generated in less then 10 lines using Pandas without any complex calculations. 

	df = pd.read_fwf("input.txt")

	df["total_transaction_amount"] = df["quantity_long"] - df["quantity_short"]

	client_information = ["client_type", "client_number", "account_number", "subaccount_number"]
	product_information = ["exchange_code", "product_group_code", "symbol", "transaction_date"]

	output_df = df.groupby(client_information + product_information, as_index=False)["total_transaction_amount"].sum()

	output_df.to_csv("output.csv")

### Setup:
The code is written in Python 3 and tested in Python 3.9, However any reasonable Python 3 version would work. To start with we need a Python 3 interpreter and a choice of virtualenv toolchain. 

After creating the virtual environment and activating start by installing the dependencies pinned in the `requrements.txt` file by running

`  pip install -r requirements.txt`

### Running:
The project folder has been organised as below

    .
    |-- Readme.md           # This file responsible that you are currently reading 
    |-- configs             # Where field configuration files are maintained
    |-- data                # Where input files have been placed, also where output files are generated to
    |   |-- Input.txt
    |   `-- output.csv
    |-- logs                # Place for log files
    |-- misc                # Miscellaneous files, scraps, pdfs and other project related info
    |-- report_generator.py # Main mehod
    |-- requirements.txt    # List of dependencies pinned down with proper versions
    `-- tests               # Package that contains unittests. 
    
To run the project simply type `python report_generator.py`

### Reusability:
The program anticipates few immediate to possible long term expectations in terms of ever changing business needs. Here are the possible scenarios and the suggestions on how the program can be made to work with minimal friction. 

The outline of the program can be summed as below

    class ReportGenerator:
        def __init__(self, input_filename, output_filename, field_configs):
	    # responsile for loading the dataframe from the input file
            ...
            
        def generate_summary_report():
	    # responsible for groupby and aggregation and writing into output.csv
            ...
    
    def main():
        rg = ReportGenerator(input_filename, output_filename, field_configs)
        rg.generate_summary_report()
        
With that in mind here are the suggestions for the different possible upcoming scenarios. 

#### Case 1:The definitions of `product_info` and `customer_info` change. 
Currently the definition of product and customer have been defined as combination of the exchange code, product group code, symbol, expiration date and client type, client number, account number, subaccount number respectively 

This definition directly affect the groupby there by affecting the total sum value and the number of rows too. 

Solution:
Any change in the product and customer info definition can be easily done by adding/removing fields to/from these two lists

    client_info = [
        "client_type",
        "client_number",
        "account_number",
        "subaccount_number",
    ]
    product_info = [
        "exchange_code",
        "product_group_code",
        "symbol",
        "transaction_date",
    ]

#### Case 2: Adding a new report

Currently this program generates daily summary report resulting the total transaction amount of each unique product they have done for the day. That doesn't mean this program cannot be used for other reports. 
    
   Solution: To facilitate a new report simply add a new method under the class `ReportGenerator`. As constructing a `ReportGenerator` object automatically loads the dataframe, the new method has to only incorporate additional logic and aggregations. 
    
#### Case 3: Format of the input file changes
  In a highly unlikely scenario, input file for the futures movement could change, either new fields can be added, or inserted in the middle, or the width could change to accommodate growing number of clients and product code. 
  
  Solution:
  If the format if the input file changes for future movements, then `configs/processed_future_movement.py` adjust the positions accordingly. Also new fields can be introduced and fields can be easily taken out, as the entire configuration are kept as a simply Python list. 
  
#### Case 4: Very different trade category is introduced. 
There can e scenarios the code can accommodate change for additional trade categories, so along with future trades, a new requirement arise to accommodate options trading or crypto trading which will have new set of field specifications. 
    
 Solution:
    Under `configs/` folder introduce a new `.py` file and declare a simple list to hold the field specifications i.e column names and their start and end positions. 
    
  The format as below
  
      new_config = [
          (str:"field1", int:start_pos, int:end_pos),
          (str:"field2", int:start_pos, int:end_pos),
          ...
         ]
   
  which then can be imported in `report_generator.py` and passed as the third arguemet while constructing ReportGenerator() object


#### Case 5: The field specification keeps changing yet backwards compatibility needs to be maintained.

This is a realistic scenario in complex business domains. The idea is to version each changes and request the origination of the input files to add a header row which consists of which version of the field specs needs to be followed while parsing the file. 

Solution:
Under `configs/` folder for each different trade categories, track and keep all spec changes as `_v1` `_v2` and so on. 

Then while constructing the `ReportGenerator` object parse the header row from the input csv and pass the right version of the `field_

configs` accordingly. Ignoring header row while constructing Pandas dataframe can be refactored with single line of code change. 

As seen above most newly arriving requirements can be either resolved by adding a new file, declaring additional rows, changing aggregate or at the most by implementing new method. That way the code is well maintained and the structure wouldn't have to change much. 

### Testing:
Tests are found under `tests/` directory and at present all the tests are maintained in a single file `tests/test.py`. Tests can be invoked with the below command. 
    python -m unittest tests/tests.py

As of now all the 7 tests are passing 

    abn  13:12  ~  abn_amro  master  ⬆  python -m unittest tests/tests.py
    ERROR:root:Check if the file exists or the filename is correct
    Traceback (most recent call last):
      File "/Users/nehem/abn_amro/report_generator.py", line 14, in __init__
        self.input_df = pd.read_fwf(
      File "/Users/nehem/.virtualenvs/abn/lib/python3.9/site-packages/pandas/io/parsers/readers.py", line 762, in read_fwf
        return _read(filepath_or_buffer, kwds)
      File "/Users/nehem/.virtualenvs/abn/lib/python3.9/site-packages/pandas/io/parsers/readers.py", line 482, in _read
        parser = TextFileReader(filepath_or_buffer, **kwds)
      File "/Users/nehem/.virtualenvs/abn/lib/python3.9/site-packages/pandas/io/parsers/readers.py", line 811, in __init__
        self._engine = self._make_engine(self.engine)
      File "/Users/nehem/.virtualenvs/abn/lib/python3.9/site-packages/pandas/io/parsers/readers.py", line 1040, in _make_engine
        return mapping[engine](self.f, **self.options)  # type: ignore[call-arg]
      File "/Users/nehem/.virtualenvs/abn/lib/python3.9/site-packages/pandas/io/parsers/python_parser.py", line 1203, in __init__
        PythonParser.__init__(self, f, **kwds)
      File "/Users/nehem/.virtualenvs/abn/lib/python3.9/site-packages/pandas/io/parsers/python_parser.py", line 96, in __init__
        self._open_handles(f, kwds)
      File "/Users/nehem/.virtualenvs/abn/lib/python3.9/site-packages/pandas/io/parsers/base_parser.py", line 222, in _open_handles
        self.handles = get_handle(
      File "/Users/nehem/.virtualenvs/abn/lib/python3.9/site-packages/pandas/io/common.py", line 702, in get_handle
        handle = open(
    FileNotFoundError: [Errno 2] No such file or directory: 'a_none_existing_filename'
    ..ERROR:root:Error in parsing the configuration at ine record_code
    Traceback (most recent call last):
      File "/Users/nehem/abn_amro/report_generator.py", line 41, in get_colspecs
        assert len(f) == 3
    AssertionError
    ...ERROR:root:Error in parsing the configuration at ine record_code
    Traceback (most recent call last):
      File "/Users/nehem/abn_amro/report_generator.py", line 62, in get_names
        assert len(f) == 3
    AssertionError
    ..
    ----------------------------------------------------------------------
    Ran 7 tests in 0.003s
    
    OK