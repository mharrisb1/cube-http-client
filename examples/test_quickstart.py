import os

import cube_http
from cube_http.types.v1.load import V1LoadRequestQueryDict


def test_quickstart_example():
    cube = cube_http.Client(
        {
            "url": os.getenv("CUBEJS_API_URL", "NOT FOUND"),
            "token": os.getenv("CUBEJS_API_TOKEN", "NOT FOUND"),
        }
    )

    cube.v1.meta()
    query: V1LoadRequestQueryDict = {
        "measures": ["teams.count"],
        "dimensions": ["teams.is_business_domain"],
        "limit": 10,
        "timeDimensions": [
            {
                "dimension": "teams.team_created_at",
                "dateRange": "last 3 month",
                "granularity": "week",
            }
        ],
        "order": [["teams.team_id", "asc"]],
    }
    cube.v1.load(query)
    cube.v1.sql(query)
