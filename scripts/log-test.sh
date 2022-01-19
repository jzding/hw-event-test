#!/bin/bash

NAMESPACE=cloud-native-events

kubectl -n ${NAMESPACE} logs -f `kubectl -n ${NAMESPACE} get pods | grep redfish-event-test | cut -f1 -d" "` 
