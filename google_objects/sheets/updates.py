def FORMAT_ROW(sheet_id, start, end, red=0, green=0, blue=0):
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
                        "red": red,
                        "green": green,
                        "blue": blue
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor)"
        }
    }
