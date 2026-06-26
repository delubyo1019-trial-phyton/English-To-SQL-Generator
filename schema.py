SCHEMA = {
    "FACT_WS_SESSIONS": {
        "description": "Fact table storing periodic session/stat captures for WS (Workspace) product users. Each row represents one session snapshot captured by the WS application.",
        "columns": {
            "STAT_ID": {"type": "NUMBER", "description": "Surrogate primary key for each session record"},
            "CALENDAR_D_KEY": {"type": "NUMBER", "description": "Foreign key to DIM_CALENDAR"},
            "CUSTOMER_D_KEY": {"type": "NUMBER", "description": "Foreign key to DIM_CUSTOMER"},
            "USER_D_KEY": {"type": "NUMBER", "description": "Foreign key to DIM_USER"},
            "STAT_COLLECTED_DATE": {"type": "TIMESTAMP", "description": "Exact timestamp when the session/stat was captured by the WS application"},
            "EVENT_DATA": {"type": "VARIANT", "description": "JSON object containing session details. Keys: windows_credential (DOMAIN\\\\username of the Windows account that ran WS), computer_name (machine hostname), ip_address (machine IP, used by other teams), machine_id (hardware ID, used by other teams). Access using Snowflake colon notation e.g. EVENT_DATA:windows_credential::VARCHAR"}
        },
        "notes": "Primary table for license-sharing analysis. Join to DIM_USER via USER_D_KEY, DIM_CUSTOMER via CUSTOMER_D_KEY. Use STAT_COLLECTED_DATE for date filtering — typically last 3 months for monthly sharing reviews. EVENT_DATA is VARIANT — always cast extracted values e.g. EVENT_DATA:windows_credential::VARCHAR"
    },
    "DIM_USER": {
        "description": "User dimension table containing information about WS licensed users.",
        "columns": {
            "USER_D_KEY": {"type": "NUMBER", "description": "Surrogate primary key, joins to FACT_WS_SESSIONS.USER_D_KEY"},
            "UUID": {"type": "VARCHAR", "description": "Unique identifier for each user across systems"},
            "LOGIN_ID": {"type": "VARCHAR", "description": "The WS login credential used to access the product. This is the key field for license-sharing detection — multiple WINDOWS_CREDENTIALs for one LOGIN_ID indicates potential sharing"},
            "FIRSTNAME": {"type": "VARCHAR", "description": "User first name"},
            "LASTNAME": {"type": "VARCHAR", "description": "User last name"},
            "FULL_NAME": {"type": "VARCHAR", "description": "Pre-concatenated as LASTNAME || ', ' || FIRSTNAME"},
            "EMAIL": {"type": "VARCHAR", "description": "User email address"},
            "USER_PERMISSIONED": {"type": "VARCHAR", "description": "License status. Filter to USER_PERMISSIONED = 'Yes' to include only currently active/licensed users. 'No' means license cancelled or inactive."},
            "ENTITLEMENT_TYPE": {"type": "VARCHAR", "description": "Type of license entitlement e.g. NAMED_USER, CONCURRENT"}
        },
        "notes": "Always filter USER_PERMISSIONED = 'Yes' unless the question specifically asks about inactive users. LOGIN_ID is the main sharing-detection identifier."
    },
    "DIM_CUSTOMER": {
        "description": "Customer/account dimension table containing company-level information for WS license holders.",
        "columns": {
            "CUSTOMER_D_KEY": {"type": "NUMBER", "description": "Surrogate primary key, joins to FACT_WS_SESSIONS.CUSTOMER_D_KEY"},
            "A_NUMBER": {"type": "VARCHAR", "description": "Account identifier e.g. A-12345"},
            "ACCOUNT": {"type": "VARCHAR", "description": "Company/account name"},
            "COUNTRY": {"type": "VARCHAR", "description": "Country of the account"},
            "REGION": {"type": "VARCHAR", "description": "Geographic region e.g. APAC, EMEA, AMER"},
            "ORGANISATION_TYPE": {"type": "VARCHAR", "description": "Type of organisation e.g. SELL-SIDE, BUY-SIDE, CORPORATE"},
            "CUSTOMER_CHANNEL": {"type": "VARCHAR", "description": "Sales channel e.g. DIRECT, INDIRECT"}
        },
        "notes": "Use for filtering by account, region, or organisation type."
    },
    "DIM_CALENDAR": {
        "description": "Calendar dimension. Rarely needed since STAT_COLLECTED_DATE on the fact table can be used directly for date filtering.",
        "columns": {
            "CALENDAR_D_KEY": {"type": "NUMBER", "description": "Surrogate primary key, joins to FACT_WS_SESSIONS.CALENDAR_D_KEY"},
            "CALENDAR_DATE": {"type": "DATE", "description": "The calendar date"},
            "YEAR": {"type": "NUMBER", "description": "Year number"},
            "MONTH": {"type": "NUMBER", "description": "Month number 1-12"},
            "MONTH_NAME": {"type": "VARCHAR", "description": "Month name e.g. January"},
            "QUARTER": {"type": "NUMBER", "description": "Quarter number 1-4"}
        },
        "notes": "Use STAT_COLLECTED_DATE directly on the fact table for most date filtering. Only join DIM_CALENDAR if the question specifically needs calendar attributes like month name or quarter."
    }
}


def build_schema_context():
    """
    Converts the SCHEMA dictionary into a formatted string
    that can be injected into a prompt as context.
    Returns a human-readable schema description Gemini can reason over.
    """
    lines = []
    lines.append("DATABASE SCHEMA FOR WS LICENSE-SHARING DETECTION SYSTEM")
    lines.append("=" * 60)

    for table_name, table_info in SCHEMA.items():
        lines.append(f"\nTABLE: {table_name}")
        lines.append(f"Description: {table_info['description']}")
        lines.append("Columns:")
        for col_name, col_info in table_info["columns"].items():
            lines.append(f"  - {col_name} ({col_info['type']}): {col_info['description']}")
        lines.append(f"Notes: {table_info['notes']}")

    lines.append("\n" + "=" * 60)
    lines.append("SNOWFLAKE-SPECIFIC RULES:")
    lines.append("- EVENT_DATA is VARIANT type. Extract fields using colon notation: EVENT_DATA:windows_credential::VARCHAR")
    lines.append("- Always cast extracted JSON values with :: e.g. ::VARCHAR, ::NUMBER, ::TIMESTAMP")
    lines.append("- Use LATERAL FLATTEN(INPUT => EVENT_DATA) to expand JSON into separate columns when needed")
    lines.append("- Standard join pattern: FROM FACT_WS_SESSIONS F LEFT JOIN DIM_USER U ON F.USER_D_KEY = U.USER_D_KEY LEFT JOIN DIM_CUSTOMER C ON F.CUSTOMER_D_KEY = C.CUSTOMER_D_KEY")
    lines.append("- Always filter USER_PERMISSIONED = 'Yes' unless specifically asked about inactive users")
    lines.append("- Use STAT_COLLECTED_DATE directly for date filtering — prefer DATEADD/DATEDIFF over joining DIM_CALENDAR")
    lines.append("- Monthly sharing reviews look at last 3 months: WHERE STAT_COLLECTED_DATE >= DATEADD('month', -3, CURRENT_DATE())")

    return "\n".join(lines)