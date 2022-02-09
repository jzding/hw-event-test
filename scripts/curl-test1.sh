#curl -v -k -X POST https://hw-event-proxy-cloud-native-events.apps.cnfdd4.t5g.lab.eng.bos.redhat.com/webhook -H "Content-Type: application/json" --data @event-data.json
#curl -v -k -X POST https://10.19.17.161:4443 -H "Content-Type: application/json" --data @event-data.json
#curl -v -k -X POST http://127.0.0.1:9087/webhook -H "Content-Type: application/json" --data @event-data.json
curl -v -k -X POST https://192.168.13.14:4443 -H "Content-Type: application/json" --data @event-data.json



