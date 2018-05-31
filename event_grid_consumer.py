import os
import json

#
# This code is designed to be copied/pasted into an Azure Function for Python.
# Note that Azure Function and Python is considered experimental
#

# The validation event, see https://aka.ms/esvalidation for details
SUBSCRIPTION_VALIDATION_EVENT = "Microsoft.EventGrid.SubscriptionValidationEvent"
# Blob created in a storage account
STORAGE_BLOB_CREATED_EVENT = "Microsoft.Storage.BlobCreated"
# The one used in the "Publisher" sample
CUSTOM_EVENT = "PersonalEventType"

postreqdata = json.loads(open(os.environ['req']).read())
print("Received events: {}".format(postreqdata))

response = open(os.environ['res'], 'w')
for event in postreqdata:
    event_data = event['data']

    # Deserialize the event data into the appropriate type based on event type using if/elif/else

    if event['eventType'] == SUBSCRIPTION_VALIDATION_EVENT:
        validation_code = event_data['validationCode']
        validation_url = event_data.get('validationUrl', None) # If you don't use the preview version of EventGrid, this might no exist
        print("Got a SubscriptionValidation event data, validation code is: {}, validation url is {}".format(
            validation_code,
            validation_url
        ))
        answer_payload = {
            "validationResponse": validation_code
        }
        response.write(json.dumps(answer_payload))
    elif event['eventType'] == STORAGE_BLOB_CREATED_EVENT:
        print("Got BlobCreated event data, blob URI {}".format(event_data['url']))
    elif event['eventType'] == CUSTOM_EVENT:
        print("Got a custom event {} and received {}".format(CUSTOM_EVENT, event_data))

response.close()