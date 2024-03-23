# Run-Program-on-GPU
Run Program based on GPU available on your system.


## Prerequisites

Before you begin, ensure you have the following installed:

- Python (3.9 or higher)
- pip (Python package installer)


## Installation
- Clone this project from github.
  `git clone https://github.com/Somvit09/Run-Program-on-GPU.git`
- Make a virtual ENV.
  `python3 -m venv venv`
- Activate
  `source venv/bin/activate`
- Install all necessary packages from requirements.txt.
  `pip install -r requirements.txt`
- now add your python modules in this directory and go to gpu_test_program module
- import the module and use the `run_with_gpu` function that takes a function as a parameter and runs it on your desired GPU.
- use `python3 -m gpu_test_program` command to start the execution.
- prompt will come up and show available GPUs in your system, you have to choose your desired GPU by index number.
- an extra function `check_gpu_usage` to check usage  of GPU that you are currently using.
- now you are good to go.

