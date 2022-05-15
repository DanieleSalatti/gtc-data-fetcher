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

queryVotes = """
query getVotes {
  votes(orderBy: id, orderDirection: asc, first: 100) {
    id
    voteId
    voter {
      id
    }
    amount
    grantId
    createdAt
  }
}
"""

votesResult = run_query(queryVotes)

queryReleases = """
query getReleases {
  releases(orderBy: id orderDirection: asc first: 100) {
    id
    voter {
      id
    }
    voteId
    amount
    createdAt
  }
}
"""

releasesResult = run_query(queryReleases)

print('Vote Results')
print('#############')
pprint(votesResult)
print('Releases Results')
print('#############')
pprint(releasesResult)