from cube_http.types.v1 import V1LoadRequestQuery

TEST_QUERIES: list[V1LoadRequestQuery] = [
    {
        "measures": ["accounts.count"],
    },
    {
        "measures": ["contacts.count"],
        "dimensions": ["contacts.full_name"],
        "limit": 10,
    },
    {
        "measures": ["opportunities.count"],
        "timeDimensions": [
            {
                "dimension": "opportunities.created_at",
                "dateRange": "last 6 months",
                "granularity": "month",
            }
        ],
    },
    {
        "measures": ["products.count"],
        "filters": [
            {"member": "products.price", "operator": "gt", "values": ["100"]}
        ],
    },
    {
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
    },
    {
        "measures": ["campaigns.count"],
        "dimensions": ["campaigns.name"],
        "order": [["campaigns.count", "desc"]],
        "limit": 5,
    },
    {
        "measures": ["accounts.count", "opportunities.count"],
    },
    {
        "measures": ["opportunity_line_items.count"],
        "dimensions": ["products.name"],
        "limit": 10,
        "offset": 10,
    },
    {
        "measures": ["leads.count"],
        "filters": [
            {
                "member": "leads.status",
                "operator": "equals",
                "values": ["New"],
            }
        ],
    },
    {
        "measures": ["cases.count"],
        "timeDimensions": [
            {
                "dimension": "cases.created_at",
                "dateRange": "this month",
            }
        ],
        "timezone": "America/New_York",
    },
    {
        "measures": ["opportunities.count"],
        "filters": [
            {
                "and": [
                    {
                        "member": "opportunities.stage",
                        "operator": "equals",
                        "values": ["Closed Won"],
                    },
                    {
                        "or": [
                            {
                                "member": "opportunities.close_date",
                                "operator": "gte",
                                "values": ["2024-01-01"],
                            },
                            {
                                "member": "opportunities.close_date",
                                "operator": "lte",
                                "values": ["2024-12-31"],
                            },
                        ],
                    },
                ]
            }
        ],
    },
    {
        "measures": ["products.count"],
        "filters": [
            {
                "member": "products.price",
                "operator": "gte",
                "values": ["50"],
            }
        ],
        "timeDimensions": [
            {
                "dimension": "products.created_at",
                "dateRange": ["2024-01-01", "2024-12-31"],
                "granularity": "quarter",
            }
        ],
        "order": [["products.price", "desc"]],
    },
    {
        "dimensions": ["tasks.subject", "tasks.priority"],
        "measures": [],
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
        "timeDimensions": [],
        "order": [["tasks.subject", "asc"]],
        "limit": 100,
    },
]
