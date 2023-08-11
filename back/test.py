import time

import requests
import json

url = "https://api.livelab.com.cn/order/app/center/v3/create"

payload = json.dumps({
  "contactName": "x",
  "contactPhone": "18808164001",
  "deliveryType": 1,
  "combineTicketVos": [],
  "ordinaryTicketVos": [
    {
      "seatPlanId": 2118,
      "seatPlanName": "鐪嬪彴655鍏�",
      "seatPlanPrice": 655,
      "seatPlanQuantity": 1,
      "frequentContactsId": 6244852
    }
  ],
  "payment": 655,
  "totalPrice": 655,
  "performId": 555,
  "projectId": "398",
  "privilegeCodeList": [],
  "blackBox": "lMPHI1691724113TTK1X95bvV6:0"
})
headers = {
  'Host': 'api.livelab.com.cn',
  'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJjdCI6MTY5MTcyMzk3NTg1OCwibWlkIjozNTA3NzExLCJ0eXBlIjoiYXBwbGV0IiwiZGlkIjoiQ0Y3RTk4QzEtQTJEOC00Q0VELTlDRkUtRDU4RjJBQ0JBMEQ0In0.1Xr8JziA8tTFgvnBTJUsjYz-fllQj9yyz_bzEluLZjJfMK5p2N_odBhPtgDg9jLf6v0mr-UCbFwNyxocKCwV2A',
  'content-type': 'application/json',
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x1800282b) NetType/WIFI Language/zh_CN',
  'Referer': 'https://servicewechat.com/wx5a8f481d967649eb/67/page-frame.html'
}


while True:

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.json())

  time.sleep(1)



