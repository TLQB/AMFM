from .import mqtt

client = mqtt.connect_mqtt()
mqtt.subscribe(client)
client.loop_start()
