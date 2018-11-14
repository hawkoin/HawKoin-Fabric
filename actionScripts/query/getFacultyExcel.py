
import json
import csv
import requests
import sys, getopt


def main(argv):
    
    url = 'http://localhost:3000/api/org.hawkoin.network.Faculty' 
    
    try:
        response = requests.get(url)

        d = response.json()
        #d = json.loads(json_string)
       # formatted_json = json.dumps(json_string, sort_keys=True, indent=4, separators=(',',': '))
#        f = csv.writer(open('dataReport.xlsx', 'wb+'))
        f = csv.writer(open('../../Reports/facultyReport.csv', 'w'))
        cj = {}
        count = 0
        for item in d:
            cj['dept'] = item['dept']
            cj['id'] = item['id']
            cj['balance'] = item['balance']
            cj['accessLevel'] = item['accessLevel']
            cj['isActive'] = item['isActive']
            cj['firstName'] = item['contactInfo']['firstName']
            cj['lastName'] = item['contactInfo']['lastName']            
            cj['email'] = item['contactInfo']['email']        
            cj['address'] = item['contactInfo']['address']
            cj['city'] = item['contactInfo']['city']
            cj['state'] = item['contactInfo']['state']
            cj['zip'] = item['contactInfo']['zip']
            if count == 0:
                header = cj.keys()
                f.writerow(header)
                count += 1
            f.writerow(cj.values())
            #print(item['contactInfo'].values())
        
        
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
    #except:
        #print("*** Key not found ***")


if __name__ == '__main__':
    main(sys.argv[1:])
    

