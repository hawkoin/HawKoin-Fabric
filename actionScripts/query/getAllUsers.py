
import json
import csv
import requests
import sys, getopt


def main(argv):
    
    url = 'http://localhost:3000/api/org.hawkoin.network.Faculty'
    url1 = 'http://localhost:3000/api/org.hawkoin.network.Student' 
    
    try:
        response = requests.get(url)

        d = response.json()
        #d = json.loads(json_string)
       # formatted_json = json.dumps(json_string, sort_keys=True, indent=4, separators=(',',': '))
#        f = csv.writer(open('dataReport.xlsx', 'wb+'))
        f = csv.writer(open('../Reports/allUserReport.csv', 'w'))
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
            cj = {}
            #print(item['contactInfo'].values())

        response = requests.get(url1)
        d = response.json()
        aj = {}
        for item in d:
            aj['dept'] = item['major']
            aj['id'] = item['id']
            aj['balance'] = item['balance']
            aj['accessLevel'] = item['accessLevel']
            aj['isActive'] = item['isActive']
            aj['firstName'] = item['contactInfo']['firstName']
            aj['lastName'] = item['contactInfo']['lastName']            
            aj['email'] = item['contactInfo']['email']        
            aj['address'] = item['contactInfo']['address']
            aj['city'] = item['contactInfo']['city']
            aj['state'] = item['contactInfo']['state']
            aj['zip'] = item['contactInfo']['zip']
            f.writerow(aj.values())

        
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
    

