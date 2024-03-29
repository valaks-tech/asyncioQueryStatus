# asyncioQueryStatus 
### Status page query for thousands of servers and build report 

Create a tool that will query the ‘status’ page on 1000 servers and create a report based on data within the status pages.

Each server has a ‘status’ endpoint that returns JSON data with the service information, a count of requests, and a success count. The tool reports the aggregated success rate (total success / total requests) broken down by application and version for all of the servers.

Sample endpoint:  
(you can find other endpoints at /hosts/host0/status, /hosts/host1/status, …, /hosts/host999/status):

{
    "requests_count": 96447,
     "application": "WebApp1",
     "version": "2.0",
     "success_count": 96427,
     "error_count": 20
}
Sample Report Output:

Application,Version,Aggregated Success Rate
WebApp1,1.0,60.0
WebApp1,1.3,90.5
WebApp2,2.0,21.5
IMPORTANT NOTES
1. The success rate column is an aggregate, or a sum of the success rate for all servers grouped by a particular unique combination of application and version. We’re explicitly calling this out, as it’s a common cause of confusion.
2. Please make reasonable assumptions and clearly state them.

### Thought process:
Tool needs to send ~1000 requests, parse the json data and calculate the aggregate success rate grouped by application_name + version. 
-	Fetch the status responses from 1k servers ==>  Each request can be sent asynchronously to optimize the speed
grequests library in python would work , it took about ~4.2 seconds to do 1k requests, where as aiohttp+asyncio libraries took 50% of the time i.e ~2 secs. So going to use asyncio + aiohttp libraries in the tool
-	Parse the response and calculate the rate grouped by application + version

Going to choose python to write this tool  and structure of the project will be as below -

Project structure of the tool:
/asyncioQueryStatus
    |-- main.py
    |-- config.py
    |-- requirements.txt
    |__ /QueryStatus
         |-- __init__.py
         |-- async_fetch_parse.py 
         |-- async_tasks.py                 
         |__ /reports
             |-- query_status_report.json

Assumptions/Known limitations:
1.	What if the server/host is not up or available for status check i.e status check times out or returns nothing.   So, in this tool, those hosts will be exempted from the actual aggregation calculation.
2.	If the request response comes back with junk/garbage characters, those servers will be exempted from the report as well. 
3.	Final report is directly printed to STDOUT/screen, not written to disk.
4.	Tool is not going to handle any rate limiting aspect for how many requests being sent.
5.	Tool is not tested with huge number of requests (>100k) mainly how it works if all data loaded directly into pandas DataFrame.

# Some test outputs:
```
C:\Users\shail\Documents\TwitterQueryStatus> python3 .\main.py
application,version,Aggregated Success Rate
WebApp1,1.0,91.03
WebApp1,2.0,90.47
WebApp2,1.0,91.68
WebApp2,2.0,89.88

Finished building report in 2.7296998500823975 seconds for 1000 hosts
PS C:\Users\shail\Documents\TwitterQueryStatus>

PS C:\Users\shail\Documents\asyncioQueryStatus> python3 .\main.py
application,version,Aggregated Success Rate
WebApp1,1.0,91.11
WebApp1,2.0,90.46
WebApp2,1.0,91.74
WebApp2,2.0,90.23

Finished building report in 23.257724046707153 seconds for 10000 hosts
PS C:\Users\shail\Documents\asyncioQueryStatus>


(env) PS C:\Users\shail\Documents\asyncioQueryStatus> python .\main.py
application,version,Aggregated Success Rate
WebApp1,1.0,91.06
WebApp1,2.0,90.5
WebApp2,1.0,91.71
WebApp2,2.0,90.04

Finished building report in 4.364496946334839 seconds for 1000 hosts
(env) PS C:\Users\shail\Documents\asyncioQueryStatus>
```
