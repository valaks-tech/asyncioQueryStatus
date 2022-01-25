# TwitterQueryStatus
### Status page query for thousands of servers and build report 

Create a tool that will query the ‘status’ page on 1000 fictitious servers and create a report based on data within the status pages.

Each server has a ‘status’ endpoint that returns JSON data with the service information, a count of requests, and a success count. The tool reports the aggregated success rate (total success / total requests) broken down by application and version for all of the servers.

Sample endpoint: 
http://storage.googleapis.com/revsreinterview/hosts/host578/status 
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
