import json
import requests
import sys, getopt


def main(argv):
    id = -1
    name = '' 
    ccr = ''
    balance = 0

    try:
        opts, args = getopt.getopt(argv,"hi:n:c:b:", ["id=", "name=", "cashConv=", "balance="])
    except getopt.GetoptError as e:
        print ('Usage:\n\nmakeVendor.py -i <id> -n <name> -c <cashConv> -b <balance>\n')
        print(e)
        sys.exit(2)
    if len(sys.argv) == 1:
        print ('Usage:\n\nmakeVendor.py -i <id> -n <name> -c <cashConv> -b <balance>\n')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print ('Usage:\n\nmakeVendor.py -i <id> -n <name> -c <cashConv> -b <balance>\n')
            sys.exit()
        elif opt in ("-i", "--id"):
            id = arg
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-c", "--cashConv"):
            ccr = arg
        elif opt in ("-b", "--balance"):
            balance = arg

    
    url = 'http://localhost:3000/api/org.hawkoin.network.Vendor'
    

    json_payload = {
        "$class": "org.hawkoin.network.Vendor",
        "vendorName": name,
        "ccr": ccr,
        "id": id,
        "balance": balance,
        "isActive": True,
        "accessLevel": "VENDOR",
        "contactInfo": {
          "$class": "org.hawkoin.network.ContactInfo",
          "firstName": name,
          "lastName": "",
          "email": "",
          "address": "",
          "city": "",
          "state": "",
          "zip": ""
        }
    }

    try:
        response = requests.post(url, json=json_payload)

        status = response.status_code

        if(status == 500):
            json_string = response.text
            parsed_json = json.loads(json_string)
            print(parsed_json['error']['message'])
        else:
            print('Successfully added', name)

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
        print("*** ERROR *** Unable to post Student")


if __name__ == '__main__':
    main(sys.argv[1:])