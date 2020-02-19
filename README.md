# AWS Lambda BOE DataSet
Lambda function to query the Bank Of England database for exchange rates,
and upload the dataset to S3 as a parquet file, so that it can be queried in Athena.

## Series Codes
```
    XUDLADS   # Australian Dollar
    XUDLCDS   # Canadian Dollar
    XUDLBK89  # Chinese Yuan
    XUDLBK25  # Czech Koruna
    XUDLDKS   # Danish Krone
    XUDLERS   # Euro
    XUDLHDS   # Hong Kong Dollar
    XUDLBK33  # Hungarian Forint
    XUDLBK97  # Indian Rupee
    XUDLBK78  # Israeli Shekel
    XUDLJYS   # Japanese Yen
    XUDLBK83  # Malaysian ringgit
    XUDLNDS   # New Zealand Dollar
    XUDLNKS   # Norwegian Krone
    XUDLBK47  # Polish Zloty
    XUDLBK85  # Russian Ruble
    XUDLSRS   # Saudi Riyal
    XUDLSGS   # Singapore Dollar
    XUDLZRS   # South African Rand
    XUDLBK93  # South Korean Won
    XUDLSKS   # Swedish Krona
    XUDLSFS   # Swiss Franc
    XUDLTWS   # Taiwan Dollar
    XUDLBK87  # Thai Baht
    XUDLBK95  # Turkish Lira
    XUDLUSS   # US Dollar
```