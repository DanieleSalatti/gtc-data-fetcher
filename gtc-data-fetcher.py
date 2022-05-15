import requests
from pprint import pprint


def run_query(q):
    request = requests.post('https://api.thegraph.com/subgraphs/name/danielesalatti/gtc-conviction-voting-rinkeby'
                            '',
                            json={'query': q})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

queryGrants = """
query getGrants {
  grants(orderBy: id, orderDirection: asc, first: 100) {
    id
    votes {
      id
      amount
      createdAt
    }
    releases {
      id
      amount
      createdAt
    }
  }
}
"""

grantsResult = run_query(queryGrants)

## TODO: calculation of voting power per grant

print('Grant Results')
print('#############')
pprint(grantsResult)
