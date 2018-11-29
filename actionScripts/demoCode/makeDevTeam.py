import json
import requests
import sys, getopt


def main(argv):
    
    # url = 'http://localhost:3000/api/org.hawkoin.network.Student'
    url = 'http://35.224.160.182:3000/api/org.hawkoin.network.Student'
    

    json_payload_matt = {
            '$class': 'org.hawkoin.network.Student',
            'isAthlete': False,    
            'major': 'CSB',  
            'id': 'mma219@lehigh.edu',        
            'balance': 100,
            'isActive': True,
            'lowBalThreshold': 5,
            'txnThreshold': 75, 
            'accessLevel': 'STUDENT',                 
            'contactInfo': {                           
              '$class': 'org.hawkoin.network.ContactInfo',      
              'firstName': 'Matt',                      
              'lastName': 'Addessi', 
              'email': 'mma219@lehigh.edu',  
              'address': 'Uh uh',
              'city': '',   
              'state': '',  
              'zip': ''                                       
            }                                                   
            }
    json_payload_tim = {
            '$class': 'org.hawkoin.network.Student',
            'isAthlete': False,    
            'major': 'CSB',  
            'id': 'tpl219@lehigh.edu',        
            'balance': 100,
            'isActive': True,
            'lowBalThreshold': 5,
            'txnThreshold': 75, 
            'accessLevel': 'STUDENT',                 
            'contactInfo': {                           
              '$class': 'org.hawkoin.network.ContactInfo',      
              'firstName': 'Tim',                      
              'lastName': 'LaRowe', 
              'email': 'tpl219@lehigh.edu',  
              'address': 'None of your business',
              'city': '',   
              'state': '',  
              'zip': ''                                       
            }                                                   
            }
    json_payload_aaron = {
            '$class': 'org.hawkoin.network.Student',
            'isAthlete': False,    
            'major': 'CSB',  
            'id': 'aar319@lehigh.edu',        
            'balance': 100,
            'isActive': True,
            'lowBalThreshold': 5,
            'txnThreshold': 75, 
            'accessLevel': 'STUDENT',                 
            'contactInfo': {                           
              '$class': 'org.hawkoin.network.ContactInfo',      
              'firstName': 'Aaron',                      
              'lastName': 'Rotem', 
              'email': 'aar319@lehigh.edu',  
              'address': 'Nope',
              'city': '',   
              'state': '',  
              'zip': ''                                       
            }                                                   
            }


    try:
        response = requests.post(url, json=json_payload_matt)
        response = requests.post(url, json=json_payload_aaron)
        response = requests.post(url, json=json_payload_tim)

        status = response.status_code

        if(status != 200):
            json_string = response.text
            parsed_json = json.loads(json_string)
            print(parsed_json['error']['message'])
        elif (status == 200):
            print('Successfully added Matt, Aaron, and Tim')

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
