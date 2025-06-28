Call a customer number:
curl -X POST http://localhost:8000/api/v1/outbound   -H "Content-Type: application/json"   -d '{
    "phoneNumberId": "914e5125-fb31-40d7-a158-7c56a15d5b2a",
    "assistantId": "8c7fcc6d-f791-4255-9084-9c0684916f84",
    "customerNumber": "+14057618211"
}'

Vapi call local hosted url
curl -X PATCH https://api.vapi.ai/phone-number/914e5125-fb31-40d7-a158-7c56a15d5b2a \
     -H "Authorization: Bearer 200ab753-8aac-40c7-bdf9-22d5842cc606" \
     -H "Content-Type: application/json" \
     -d '{
         "server": {
             "url": "https://0d4f-24-161-48-200.ngrok-free.app/v1/assistant"
         }
     }'