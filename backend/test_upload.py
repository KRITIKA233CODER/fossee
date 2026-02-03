import requests

BASE_URL = 'http://127.0.0.1:8000/api'
USERNAME = 'testuser'
PASSWORD = 'password123'
EMAIL = 'test@example.com'

def test_upload():
    # 1. Signup/Login to get token
    session = requests.Session()
    
    # Try login first
    print(f"Logging in as {USERNAME}...")
    resp = session.post(f'{BASE_URL}/auth/login/', json={'username': USERNAME, 'password': PASSWORD})
    
    if resp.status_code == 401 or resp.status_code == 400:
        print("Login failed, trying signup...")
        resp = session.post(f'{BASE_URL}/signup/', json={'username': USERNAME, 'password': PASSWORD, 'email': EMAIL})
        if resp.status_code != 201:
            print(f"Signup failed: {resp.text}")
            return
            
    # Create test CSV matching user's file
    csv_content = """Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,12.5,1.2,45
Valve B,Valve,5.0,0.8,30
Reactor 1,Reactor,100,2.5,120
Pump C,Pump,9.0,1.1,40
Sensor X,Sensor,0.5,0.1,25
Heat Exchanger 1,Heat Exchanger,25.5,1.5,85
Pump D,Pump,14.2,1.3,48
Valve C,Valve,4.2,0.9,28
Reactor 2,Reactor,95,2.6,125
Sensor Y,Sensor,0.1,0.1,22
Pump E,Pump,11.0,1.15,42
Tank A,Storage Tank,0,1.0,20
Pump F (Faulty),Pump,2.0,0.2,95
Reactor 3,Reactor,110,3.0,135
Valve D,Valve,6.1,0.85,31
Mixer 1,Mixer,45.0,1.1,55
Mixer 2,Mixer,42.5,1.05,53
Pump G,Pump,13.0,1.25,46
Sensor Z,Sensor,0.2,0.1,24
Reactor 4,Reactor,105,2.8,130
Valve E (Leaking),Valve,12.0,0.3,29
Heat Exchanger 2,Heat Exchanger,28.0,1.6,88
Pump H,Pump,8.5,1.0,38
Tank B,Storage Tank,0,1.0,21
Cooling Tower 1,Cooling Unit,150,1.1,15"""
    
    with open('user_test.csv', 'w') as f:
        f.write(csv_content)

    if resp.status_code == 200 or resp.status_code == 201:
        data = resp.json()
        token = data['access']
        print("Got access token")
        
        # 2. Upload CSV
        headers = {'Authorization': f'Bearer {token}'}
        files = {'file': open('user_test.csv', 'rb')}
        
        print("Uploading CSV...")
        upload_resp = requests.post(
            f'{BASE_URL}/datasets/upload/',
            headers=headers,
            files=files
        )
        
        with open('results.txt', 'w') as f:
            f.write(f"Status: {upload_resp.status_code}\n")
            f.write(f"Response: {upload_resp.text}\n")
    else:
        with open('results.txt', 'w') as f:
            f.write(f"Auth failed: {resp.text}\n")

if __name__ == '__main__':
    try:
        test_upload()
    except Exception as e:
        with open('results.txt', 'w') as f:
            f.write(f"Script error: {e}")
