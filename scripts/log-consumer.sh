#!/bin/bash

NAMESPACE=cloud-native-events

kubectl -n ${NAMESPACE} logs -f -c cloud-event-consumer `kubectl -n ${NAMESPACE} get pods | grep consumer | cut -f1 -d" "`
