import json
import requests
import sys, getopt


def main(argv):
    
    url = 'http://localhost:3000/api/org.hawkoin.network.Vendor' 
    
    try:
        response = requests.get(url)

        json_string = response.json()
        formatted_json = json.dumps(json_string, sort_keys=True, indent=4, separators=(',',': '))

        print(formatted_json)
        
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