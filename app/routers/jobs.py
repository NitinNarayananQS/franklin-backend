from fastapi import APIRouter
import requests

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)


query1 = """
    query RunsQuery {
        runsOrError {
            ... on Runs {
                results {
                    runId
                    jobName
                    status
                    runConfigYaml
                    stats {
                        ... on RunStatsSnapshot {
                            id
                            startTime
                            endTime
                            stepsFailed
                        }
                    }
                }
            }
        }
    }
"""

# for usage when run inside of a container
# url = 'http://host.docker.internal:3000/graphql'

# for local development 
url = 'http://localhost:3000/graphql'

# variables  = {"repositoryLocationName": "eliaapifetcher", "repositoryName": "elia_api_repo"}

# r1 = requests.post(url, json={'query': query1, 'variables': variables})

# print(json.dumps(r1.json(), indent=4))

@router.get('/getAllRuns')
def get_runs():
    r1 = requests.post(url, json={'query': query1 })
    return r1.json()