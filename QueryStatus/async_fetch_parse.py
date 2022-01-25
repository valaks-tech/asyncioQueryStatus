"""Query URLs, extract json data, and write aggregated data to file"""
from aiofiles.threadpool.text import AsyncTextIOWrapper as AsyncIOFile
from aiohttp import ClientError, ClientSession, InvalidURL
import json

async def fetch_parse_report_data(
    session: ClientSession,
    url: str,
    outfile: AsyncIOFile,
    total_count: int,
    i: int,
):
    """
    Fetch raw JSON from a URL prior to parsing.

    : ClientSession session: Async HTTP requests session.
    : url: Target URL to be fetched.
    : AsyncIOFile outfile: Path of local file to write to.
    : total_count: Total number of URLs to be fetched.
    : i: Current iteration of URL out of total URLs.
    """
    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                pass
                # Place to handle errors
                # May be, create status failure reports?
                # FIXME LATER!
            #IGNORING ANY query status NOT SUCCESSFUL !
            if resp.status == 200:
                resptxt = await resp.read()
                respdata = json.loads(resptxt)
                #print(resptxt)
                # IGNORE if data is empty
                if bool(respdata):
                    # lets manipulate the data
                    rptdata = {}
                    rptdata['application'] = respdata['application']
                    rptdata['version'] = respdata['version']
                    rptdata['rate'] = round((respdata['success_count'] / respdata['requests_count']), 2)

                    # well, json.dumps does not add "["(square bracket) by itself, need to create an array
                    #rptdata_arr = [rptdata] # Create array
                    # Serializing json
                    json_object = json.dumps(rptdata)
                    #csv_str = respdata['application']+","+respdata['version']+","+ rate
                    await outfile.write(f"{json_object}\n")
            """
            Example:
            #print("Status:", resp.status)
            #print("Content-type:", resp.headers['content-type'])

            Content-type: application/octet-stream
            {
                "requests_count": 95366,
                "application": "WebApp2",
                "version": "1.0",
                "success_count": 16953,
                "error_count": 78413
            }

            """
            
    except InvalidURL as e:
        print("invalid URL ?")
    except ClientError as e:
        print("ClientError while querying url")
    except Exception as e:
        print(" Some Unexpected error while querying URL ?".format(e))