import cube_http
from cube_http.exc import V1LoadError

if __name__ == "__main__":
    cube = cube_http.Client(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
        }
    )

    try:
        load_resp = cube.v1.load(
            {
                "query": {
                    "measures": ["tasks.count"],
                    "filters": [
                        {
                            "or": [
                                {
                                    "member": "tasks.status",
                                    "operator": "equals",
                                    "values": ["Completed"],
                                },
                                {
                                    "member": "tasks.priority",
                                    "operator": "equals",
                                    "values": ["High"],
                                },
                            ]
                        }
                    ],
                }
            }
        )

        print(load_resp.model_dump())
    except V1LoadError as e:
        print("Error:", e)
