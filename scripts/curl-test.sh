curl -v -k -location --request POST 'https://hw-event-proxy-openshift-hw-events.apps.worker-1.cluster1.savanna.lab.eng.rdu2.redhat.com/webhook' -H "Content-Type: text/plain" --data @event-data.json

#curl -v -k -X POST https://hw-event-proxy-cloud-native-events.apps.cnfdd4.t5g.lab.eng.bos.redhat.com/webhook -H "Content-Type: application/json" -H "Connection: close"  --data @event-data.json
#curl -v -k -X POST https://hw-event-proxy-cloud-native-events.apps.cnfdd4.t5g.lab.eng.bos.redhat.com/webhook -H "Content-Type: application/json" --data @event-data.json
#curl -v -k -X POST https://10.19.17.161:4443 -H "Content-Type: application/json" --data @event-data.json
#curl -v -k -X POST http://127.0.0.1:9087/webhook -H "Content-Type: application/json" --data @event-data.json
#curl -v -k -X POST https://127.0.0.1:4443 -H "Content-Type: application/json" --data @event-data.json



