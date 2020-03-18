#!/usr/bin/python
import Algorithmia
import os
import requests
import time


#TODO: Make sure this works even when a build id isn't visible just yet
def get_build_id(api_key, api_address, algo_name, hash, marker=None):
    headers = {'content-type': 'application/json', 'Authorization': "Simple {}".format(api_key)}
    if marker:
        url = "{}/{}/builds?limit={}&marker={}".format(api_address, algo_name, 10, marker)
    else:
        url = "{}/{}/builds?limit={}".format(api_address, algo_name, 10)
    response = requests.get(headers=headers, url=url)
    result = response.json()
    if "error" in result:
        raise Exception(result['error']['message'])
    else:
        builds = result['results']
        for build in builds:
            if hash in build['commit_sha']:
                build_id = build['build_id']
                return build_id
        marker = result['marker']
        return get_build_id(api_key, api_address, algo_name, hash, marker)


def wait_for_result(api_key, api_address, algo_name, build_id):
    waiting = True
    headers = {'content-type': 'application/json', 'Authorization': "Simple {}".format(api_key)}
    url = "{}/{}/builds/{}".format(api_address, algo_name, build_id)
    while waiting:
        response = requests.get(headers=headers, url=url)
        result = response.json()
        if "error" in result:
            raise Exception(result['error']['message'])
        else:
            if result['status'] != "in-progress":
                if result['status'] is "succeeded":
                    return
                else:
                    url_logs = "{}/{}/builds/{}/logs".format(api_address, algo_name, build_id)
                    response = requests.get(headers=headers, url=url_logs)
                    results = response.json()
                    raise Exception("build failure:\n{}".format(results['logs']))
            else:
                time.sleep(5)


if __name__ == "__main__":
    api_key = os.getenv("INPUT_API_KEY")
    api_address = os.getenv("INPUT_API_ADDRESS")
    algo_name = os.getenv("INPUT_ALGORITHM_NAME")
    algo_hash = os.getenv("INPUT_ALGORITHM_HASH")
    print("--- Finding build in progress ---")
    build_id = get_build_id(api_key, api_address, algo_name, algo_hash)
    print("--- Build ID found, waiting for result ---")
    wait_for_result(api_key, api_address, algo_name, build_id)
    print("--- Build successful ---")
