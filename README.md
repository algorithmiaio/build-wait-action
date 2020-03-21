# build-wait github action
When attached to a github backed Algorithmia repository's action workflow, 
this action can wait for the downstream algorithmia build event to finish.
In the event of a build failure, this action will provide docker build logs as well.


## Action Input


```
inputs:
  mgmt_api_key:
    description: 'your Algorithmia Management API key'
    required: true
  api_address:
    description: 'The API address for the Algorithmia Cluster you wish to connect to'
    required: false
    default: 'https://api.algorithmia.com'
  algorithm_name:
    description: 'The name of the Algorithm you want to test'
    required: true
 ```
 
* mgmt_api_key - (required) - your Algorithmia Management API key, which you can learn about [here](https://algorithmia.com/developers/platform/customizing-api-keys).
* algorithm_name (required) - The algorithmia algorithm name for project you're testing. This algorithm name must refer to the github repository you attach this action to in order to work properly.
* api_address - (optional) - The Algorithmia API cluster address you wish to connect to, if using a private cluster; please provide the correct path to your environment.


## Example

```
name: Algorithmia build-wait

on:
  commit

jobs:
  build-wait:

    runs-on: ubuntu-latest
    - name: Algorithmia build-wait
      uses: algorithmiaio/build-wait-action@v0.1.0-rc4
      id: build-wait-step
      with:
        mgmt_api_key: {{ secrets.ALGORITHMIA_MGMT_API_KEY }}
        api_address: {{ secrets.ALGORITHMIA_API_ADDRESS }}
        algorithm_name: your_username/your_algorithm
```
