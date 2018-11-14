
import json
import csv 
import requests
import sys, getopt


def main(argv):
    
    url = 'http://localhost:3000/api/org.hawkoin.network.TransferFunds' 
    
    try:
        response = requests.get(url)

        d = response.json()
        #formatted_json = json.dumps(json_string, sort_keys=True, indent=4, separators=(',',': '))
        f = csv.writer(open('../reports/transactionReport.csv', 'w'))
        cj = {}
        count = 0
        for item in d:
            cj['amount'] = item['amount']
            cj['fromuser'] = item['fromUser'].split('#',1)[1]
            cj['toUser'] = item['toUser'].split('#',1)[1]
            cj['transactionId'] = item['transactionId']
            cj['timestamp'] = item['timestamp']
            if count == 0:
                header = cj.keys()
                f.writerow(header)
                count += 1
            f.writerow(cj.values())
        #print(formatted_json)
        
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
    except:
        print("Could not perform query")


if __name__ == '__main__':
    main(sys.argv[1:])
    

