from paho.mqtt import client as mqtt_client
import random, json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

broker = 'broker.emqx.io'
port = 1883
topic = "rgps/hello"
client_id = f'python-mqtt-{random.randint(0, 100)}'
values,Username = None,None 
lat, lon = 0,0 

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    
    def on_message(client, userdata, msg):
        global lat,lon,values 

        #print(json.loads(msg.payload))
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        values = json.loads(msg.payload)
        lat, lon = values.get("lat"),values.get("lon")

    client.subscribe(topic)
    client.on_message = on_message

@csrf_exempt
def get_location(request):
    global lat,lon 
    print(lat,lon )
    # Lấy tọa độ lat, lon từ thiết bị hoặc database của bạn
    #lat, lon = random.uniform(15.563000, 15.565500) , random.uniform(108.481100, 108.481533) #15.563477, 108.481533

    # Trả về JSON chứa tọa độ
    data = {'lat': lat, 'lon': lon}
    return JsonResponse(data)
