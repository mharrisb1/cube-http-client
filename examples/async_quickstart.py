import asyncio

import cube_http


async def main():
    cube = cube_http.AsyncClient(
        {
            "url": "http://localhost:4000/cubejs-api",
            "token": "i9f5e76b519a44b060daa33e78c5de170",
        }
    )

    load_resp = await cube.v1.load(
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


if __name__ == "__main__":
    asyncio.run(main())
