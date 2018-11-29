import json
import requests
import sys, getopt


def main(argv):
    id = None 
    try:
        opts, args = getopt.getopt(argv,"hi:o:", "id=")
    except getopt.GetoptError:
        print ('getAdmin.py -i <id>')
        sys.exit(2)
    if len(sys.argv) == 1:
        print ('getAdmin.py -i <id>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print ('getAdmin.py -i <id>')
            sys.exit()
        elif opt in ("-i", "--id"):
            id = arg
    
    #url = 'http://localhost:3000/api/org.hawkoin.network.Administrator/' + id 
    url = 'http://35.224.160.182:3000/api/org.hawkoin.network.Administrator/' + id
    
    try:
        response = requests.get(url)

        json_string = response.text
        parsed_json = json.loads(json_string)

        status = response.status_code
       
        if(status == 500):
            print(parsed_json['error']['message'])
        else:
            print('ID: '.ljust(15), parsed_json['id'])          
            print('Name: '.ljust(15), parsed_json['contactInfo']['firstName'], parsed_json['contactInfo']['lastName'])          
            print('Balance: '.ljust(15), parsed_json['balance'])        
            print('isActive: '.ljust(15), parsed_json['isActive'])

        
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
        print("*** Key not found ***")


if __name__ == '__main__':
    main(sys.argv[1:])
    

