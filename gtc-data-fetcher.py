from decimal import *
import time
import requests
from pprint import pprint

from web3 import Web3

# export const GRAPH_URI_RINKEBY = "https://api.thegraph.com/subgraphs/name/danielesalatti/gtc-conviction-voting-rinkeby";
# Temporary Mainnet query URL:
# export const GRAPH_URI_MAINNET = "https://api.studio.thegraph.com/query/20308/gtc-conviction-voting-mainnet/v0.0.2";


def run_query(q):
    request = requests.post('https://api.studio.thegraph.com/query/20308/gtc-conviction-voting-mainnet/v0.0.2'
    # request = requests.post('https://api.thegraph.com/subgraphs/name/danielesalatti/gtc-conviction-voting-rinkeby'
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
      voteId
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

grants = grantsResult['data']['grants']

maxMultiplier = 50

secondsInSixMonths = 60 * 60 * 24 * 30 * 6
alphaDecay = 0.8
beta = pow(maxMultiplier, 1 / secondsInSixMonths) - 1

def mapReleasesToVoteId(grant):
    releases = grant['releases']
    releaseByVoteId = {}
    for release in releases:
        releaseByVoteId[int(release['voteId'])] = release
    return releaseByVoteId

def calculate_voting_power(grant):
    totalVotingPower = 0

    releaseByVoteId = mapReleasesToVoteId(grant)

    for vote in grant['votes']:
        secondsSinceVote = (time. time() - int(vote['createdAt']))

        secondsSinceRelease = 0

        voteIdInt = int(vote['id'], 16)

        if (voteIdInt in releaseByVoteId):
            print("release found")
            secondsSinceRelease = (time. time() - int(releaseByVoteId[voteIdInt]['createdAt']))
            secondsSinceVote = secondsSinceVote - secondsSinceRelease

        
        secondsSinceVote = min(secondsSinceVote, secondsInSixMonths)

        votingPower = Web3.fromWei(int(vote['amount']), 'ether') * Decimal(pow(1 + beta, secondsSinceVote))

        for i in range(0, int(secondsSinceRelease)):
            votingPower = votingPower - Decimal(((1 - alphaDecay) / (24 * 60 * 60))) * votingPower
        
        totalVotingPower = totalVotingPower + votingPower
    
    return totalVotingPower



for grant in grants:
    print('Grant: {}'.format(int(grant['id'], 16)))
    print('Voting Power: {}'.format(calculate_voting_power(grant)))

