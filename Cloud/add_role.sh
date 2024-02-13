curl --location '34.250.205.215:30007/api/v1/roles' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--user "airflow:airflow" \
--data '{
    "actions": [
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "Audit Logs"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "DAG Dependencies"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "DAG Code"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "DAG Runs"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "Datasets"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "Cluster Activity"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "ImportError"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "DAG Warnings"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "Jobs"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "My Password"
            }
        },
        {
            "action": {
                "name": "can_edit"
            },
            "resource": {
                "name": "My Password"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "My Profile"
            }
        },
        {
            "action": {
                "name": "can_edit"
            },
            "resource": {
                "name": "My Profile"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "Plugins"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "SLA Misses"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "Task Instances"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "Task Logs"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "XComs"
            }
        },
        {
            "action": {
                "name": "can_read"
            },
            "resource": {
                "name": "Website"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "Browse"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "DAGs"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "DAG Dependencies"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "DAG Runs"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "Datasets"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "Cluster Activity"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "Documentation"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "Docs"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "Jobs"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "Audit Logs"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "Plugins"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "SLA Misses"
            }
        },
        {
            "action": {
                "name": "menu_access"
            },
            "resource": {
                "name": "Task Instances"
            }
        },
        {
            "action": {
                "name": "can_create"
            },
            "resource": {
                "name": "Task Instances"
            }
        },
        {
            "action": {
                "name": "can_edit"
            },
            "resource": {
                "name": "Task Instances"
            }
        },
        {
            "action": {
                "name": "can_delete"
            },
            "resource": {
                "name": "Task Instances"
            }
        },
        {
            "action": {
                "name": "can_create"
            },
            "resource": {
                "name": "DAG Runs"
            }
        },
        {
            "action": {
                "name": "can_edit"
            },
            "resource": {
                "name": "DAG Runs"
            }
        },
        {
            "action": {
                "name": "can_delete"
            },
            "resource": {
                "name": "DAG Runs"
            }
        }
    ],
    "name": "RestrictedUser"
}'