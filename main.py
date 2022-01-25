"""  Tool Execution entry point """

import asyncio
import time
import json
import pandas as pd

from QueryStatus import init_myscript
from config import BASE_DIR, HOSTS_COUNT, REPORT_FILEPATH, HTTP_HEADERS

if __name__ == "__main__":
    start = time.time()
    asyncio.run(init_myscript())
    # Time to run final report 
    reportData = []
    with open(REPORT_FILEPATH) as inputData:
        for line in inputData:
            #print(line)
            try:
                reportData.append(json.loads(line.rstrip('\n')))
            except ValueError:
                # Skipping invalid line {0}").format(repr(line))
                pass

    df = pd.DataFrame(reportData)
    #df2 = df.groupby(['application', 'version'])['rate'].sum()
    #pd.set_option("display.max_rows", None, "display.max_columns", None)
    #df_final = df.groupby(['application', 'version'])['rate'].agg([('Average','mean'),('Total','sum')])
    df_final = df.groupby(['application', 'version'])['rate'].agg([('Aggregated Success Rate','mean')])
    df_final["Aggregated Success Rate"] = round((100 * df_final["Aggregated Success Rate"]), 2)
    final_report = df_final.to_csv(index=True)
    print(final_report)
    end = time.time() - start
    rows_count = len(df_final.index)
    print("Finished building report in {} seconds for {} hosts".format(end, HOSTS_COUNT))