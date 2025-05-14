from typing import Literal

FilterOperator = Literal[
    "equals",
    "notEquals",
    "contains",
    "notContains",
    "startsWith",
    "notStartsWith",
    "endsWith",
    "notEndsWith",
    "gt",
    "gte",
    "lt",
    "lte",
    "set",
    "notSet",
    "inDateRange",
    "notInDateRange",
    "beforeDate",
    "afterDate",
    "measureFilter",
]
