def FORMAT_ROW(sheet_id, start, end, rgba):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start,
                "endRowIndex": end
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": rgba[0],
                        "green": rgba[1],
                        "blue": rgba[2],
                        'alpha': rgba[3]
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor)"
        }
    }
