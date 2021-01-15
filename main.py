import requests
import json

url = "https://mainnet.infura.io/v3/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
start_block = 10943752
end_block = 11659280

print("diff", end_block - start_block)


def get_transfer(_from, _to):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getLogs",
        "params": [
            {
                "address": "0xa1faa113cbe53436df28ff0aee54275c13b40975",
                "fromBlock": hex(_from),
                "toBlock": hex(_to),
                "topics": ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"],
            },
            "latest",
        ],
        "id": 1,
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    return response.json()["result"]


m = {}

i = start_block
while i < end_block:
    j = i + 10000
    if j > end_block:
        j = end_block

    x = get_transfer(i, j)
    print(len(x), f"({i},{j})")

    for xx in x:
        [a, b, c] = xx["topics"]
        if b in m:
            m[b] -= int(xx["data"], 16)
        else:
            m[b] = 0

        if c in m:
            m[c] += int(xx["data"], 16)
        else:
            m[c] = int(xx["data"], 16)

    i = j

print(m)
