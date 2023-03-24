from time import sleep

from jnius import autoclass

PythonService = autoclass("org.kivy.android.PythonService")
PythonService.mService.setAutoRestartService(True)
from os import environ

argument = environ.get("PYTHON_SERVICE_ARGUMENT", "")

from plyer import gps
from kivy.app import App
from kivy.logger import Logger
from time import sleep
from paho.mqtt import client as mqtt_client
import json
import random

broker = "broker.emqx.io"
port = 1883
topic = str(argument)
client_id = f"python-mqtt-{random.randint(0, 1000)}"


class MQTT:
    @staticmethod
    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        # client.username_pw_set(username, password)
        print("ok 1111111111111")
        client.on_connect = on_connect
        client.connect(broker, port)
        print("kết nối .............")
        return client

    @staticmethod
    def publish(client, lat, lon):
        msg = json.dumps({"lat": lat, "lon": lon})
        result = client.publish(topic, msg)


class GpsService:
    def __init__(self):
        self.gps_enabled = False
        self.gps_status = "Click Start to get GPS location updates"

    def start(self):
        try:
            gps.configure(
                on_location=self.on_location, on_status=self.on_status
            )
        except NotImplementedError:
            import traceback

            traceback.print_exc()
            self.gps_status = "GPS is not implemented for your platform"

        self.gps_enabled = gps.start(1000, 0)
        while True:
            print(">>>>>>>>>>>>>>>", argument)
            sleep(1)

    def stop(self):
        gps.stop()
        self.gps_enabled = False

    def on_location(self, **kwargs):
        lat = kwargs["lat"]
        lon = kwargs["lon"]
        Logger.info("Location: lat={0}, lon={1}".format(lat, lon))
        MQTT().publish(client, lat, lon)
        print(lat, lon)

    def on_status(self, stype, status):
        self.gps_status = "type={}\n{}".format(stype, status)


class MyApp(App):
    def build(self):
        self.gps_service = GpsService()
        self.gps_service.start()


if __name__ == "__main__":
    client = MQTT().connect_mqtt()
    print("connect success *****************************************\n ")
    client.loop_start()
    MyApp().run()