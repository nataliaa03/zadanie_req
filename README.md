## zadanie_req

## the branch 'master' is the solution of my task. To not mix both README, I place MY README here.

I used pytest.<br>

# Project structure
I placed tests (test cases) in the [test_api.py](test_api.py) file,
<br>
the methods used for exectuing the test cases are placed in  [request_methods.py](request_methods.py) file. 
<br>
The test data is placed in [test_data.py](test_data.py) file.
<br>
<br>

Test cases are divided into 4 sections (@pytest.mark.tc<number>).<br>
  tc1(a-g) - GET apps testing <br>
  tc2(a-f) - POST Create App and DELETE Delete App <br>
  tc3(a-d) - GET app by id <br>
  tc4(a-d) - PATCH Update App <br>
<br>
  Some of test cases are parametrized - to not repeat the code. In total there is <b>27 test cases<b>.<br>

## **Usage:**

You can run each test case separately, for exmple:

> bin/run.sh tests tc1
