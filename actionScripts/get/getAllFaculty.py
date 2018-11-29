

import json
import csv
import requests
import sys, getopt


def main(argv):
    
    # url = 'http://localhost:3000/api/org.hawkoin.network.Faculty' 
    url = 'http://35.224.160.182:3000/api/org.hawkoin.network.Faculty'
    
    try:
        response = requests.get(url)
        json_string = response.json()
        # print(json_string)
        formatted_json = json.dumps(json_string, sort_keys=True, indent=4, separators=(',',': '))
        #print(formatted_json)
        
        j = json.loads(formatted_json)

        f = csv.writer(open('../Reports/Faculty_Summary.csv', 'wb+'))
        #f.writerow()
        thing = {'first_name': 'Baked', 'last_name': 'Beans'}

        for row in j: 
            f.writerow(thing)

        # count = 0
        # for item in formatted_json:
        #     if count == 0:
        #         header = item.keys()
        #         f.writerow(header)
        #         count += 1
        #     f.writerow(item.values())

        #print(formatted_json)

        #f.close()
        
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print("***Error***: Timeout")
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("***Error***: URL is bad")
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print (e)
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])