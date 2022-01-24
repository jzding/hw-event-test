// Copyright 2021 The Cloud Native Events Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package main

import (
	"fmt"
	"net/http"
	"sync"
	"time"

	jsoniter "github.com/json-iterator/go"
	"github.com/valyala/fasthttp"
	"k8s.io/apimachinery/pkg/util/wait"
)

const (
	hwEventVersion string = "v1"
	// in seconds
	publisherRetryInterval = 5
	webhookRetryInterval   = 5
)

var (
	apiPath         = "/api/cloudNotifications/v1/"
	apiPort         int
	json            = jsoniter.ConfigCompatibleWithStandardLibrary
	resourceAddress string
	hwEventPort     = "4443"
)

func main() {
	var wg sync.WaitGroup
	wg.Add(1)
	startWebhook(&wg)
	fmt.Print("waiting for events")
	wg.Wait()
}

func fastHTTPHandler(ctx *fasthttp.RequestCtx) {
	switch string(ctx.Path()) {
	case "/ack/event":
		ackEvent(ctx)
	case "/webhook":
		handleHwEvent(ctx)
	default:
		ctx.Error("Unsupported path %s", fasthttp.StatusNotFound)
	}

}

func startWebhook(wg *sync.WaitGroup) {
	go wait.Until(func() {
		defer wg.Done()

		err := fasthttp.ListenAndServe(fmt.Sprintf(":%s", hwEventPort), fastHTTPHandler)
		if err != nil {
			fmt.Printf("error starting webhook: %s\n, will retry in %d seconds", err.Error(), webhookRetryInterval)
		}
	}, webhookRetryInterval*time.Second, wait.NeverStop)
}

func ackEvent(ctx *fasthttp.RequestCtx) {
	body := ctx.PostBody()
	if len(body) > 0 {
		fmt.Printf("received ack %s", string(body))
	} else {
		ctx.SetStatusCode(http.StatusNoContent)
	}
}

// handleHwEvent gets redfish HW events and converts it to cloud native event
// and publishes to the event framework publisher
func handleHwEvent(ctx *fasthttp.RequestCtx) {
	fmt.Printf("webhook received event %s", string(ctx.PostBody()))
}
