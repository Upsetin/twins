import requests

url = "https://api.livelab.com.cn/order/app/center/v3/create"

payload = "{\"contactName\":\"康芮绮\",\"contactPhone\":\"18482113801\",\"deliveryName\":\"康芮绮\",\"deliveryPhone\":\"18482113801\",\"expressFee\":0.0,\"deliveryAddress\":\"\",\"addressId\":null,\"deliveryType\":1,\"projectId\":398,\"performId\":555,\"totalPrice\":\"1310.00\",\"payment\":\"1310.00\",\"ordinaryTicketVos\":[{\"seatPlanId\":2118,\"frequentContactsId\":6300673},{\"seatPlanId\":2118,\"frequentContactsId\":6302199}],\"combineTicketVos\":null,\"blackBox\":\"pIPHJ16917227815bh01gitCLf:1\",\"buyerId\":null}"
headers = {
  'user-agent': 'Dart/2.19 (dart:io)',
  'content-type': 'application/json; charset=utf-8',
  'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJjdCI6MTY5MTcxNTg1NDgzMiwibWlkIjozNTA3NzExLCJ0eXBlIjoiYXBwIiwiZGlkIjoiQ0Y3RTk4QzEtQTJEOC00Q0VELTlDRkUtRDU4RjJBQ0JBMEQ0In0.e1ze7oAdtF9PsfzuiMpEJznSQt6soTy7nTBMW49Sg9b7Fbc6GOlOvc1x7hauNZBKulomeQzVJYOYgU6i43lCag',
  'host': 'api.livelab.com.cn'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())
