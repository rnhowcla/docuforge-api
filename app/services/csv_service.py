import io
import csv
import pandas as pd


def csv_to_excel(file_bytes: bytes, delimiter: str = ",") -> bytes:
    df = pd.read_csv(io.BytesIO(file_bytes), sep=delimiter, engine="python")
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output.read()


def csv_clean(file_bytes: bytes, delimiter: str = ",") -> bytes:
    content = file_bytes.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(content), delimiter=delimiter)
    rows = [[cell.strip() for cell in row] for row in reader]
    # Remove fully empty rows
    rows = [r for r in rows if any(c != "" for c in r)]
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")
