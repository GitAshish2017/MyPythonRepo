import pandas as pd
import csv

def safe_read_csv(filepath):
    rows = []
    with open(filepath, 'r', encoding='latin1') as f:
        reader = csv.reader(f)
        header = next(reader)  # first line as header
        num_cols = len(header)

        for line_number, row in enumerate(reader, start=2):  # start=2 because header is line 1
            if len(row) == num_cols:
                rows.append(row)
            else:
                print(f"⚠ Skipped line {line_number}: {row}")  # optional: log skipped rows

    df = pd.DataFrame(rows, columns=header)
    return df

def compare_datasets(file1_path, file2_path):
    # Read CSV files
    df1 = safe_read_csv('C:/Users/Admin/Desktop/app2/csv1.csv')
    df2 = safe_read_csv('C:/Users/Admin/Desktop/app2/csv2.csv')

    # Check if dataframes are None or empty
    if df1 is None or df2 is None:
        print("Error: One of the dataframes is None.")
        return None, None, None
    
    # Strip any extra spaces from column names
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Check the columns in each DataFrame
    print(f"Columns in df1: {df1.columns.tolist()}")
    print(f"Columns in df2: {df2.columns.tolist()}")

    name = 'name'  # Replace with your actual column name

    # Check if the column exists in both DataFrames
    if name not in df1.columns or name not in df2.columns:
        print(f"Error: Column '{name}' not found in both files.")
        return None, None, None

    # Check uniqueness of the column values
    print(f"Unique check for df1: {df1[name].is_unique}")
    print(f"Unique check for df2: {df2[name].is_unique}")

    # Drop duplicates if necessary
    df1 = df1.drop_duplicates(subset=[name])
    df2 = df2.drop_duplicates(subset=[name])

    # Perform the merge
    common_rows = pd.merge(df1, df2)

    # Find rows unique to each file
    unique_to_file1 = df1.merge(df2, how='outer', indicator=True).query('_merge == "left_only"').drop('_merge', axis=1)
    unique_to_file2 = df2.merge(df1, how='outer', indicator=True).query('_merge == "left_only"').drop('_merge', axis=1)

    return common_rows, unique_to_file1, unique_to_file2

# Function to convert DataFrames to HTML
def convert_to_html(common_rows, unique_to_file1, unique_to_file2):
    # Check if any DataFrame is None or empty before calling to_html
    if common_rows is None or unique_to_file1 is None or unique_to_file2 is None:
        print("One or more of the dataframes is None. Cannot convert to HTML.")
        return None, None, None
    
    # Check if DataFrames are empty
    if common_rows.empty:
        print("common_rows is empty!")
        common_rows_html = None
    else:
        common_rows_html = common_rows.to_html()

    if unique_to_file1.empty:
        print("unique_to_file1 is empty!")
        unique_to_file1_html = None
    else:
        unique_to_file1_html = unique_to_file1.to_html()

    if unique_to_file2.empty:
        print("unique_to_file2 is empty!")
        unique_to_file2_html = None
    else:
        unique_to_file2_html = unique_to_file2.to_html()

    return common_rows_html, unique_to_file1_html, unique_to_file2_html


# Main Code: Example of usage
file1_path = r'C:/Users/Admin/Desktop/app2'  # Update with your file paths

file2_path = r'C:/Users/Admin/Desktop/app2'  # Update with your file paths

common_rows, unique_to_file1, unique_to_file2 = compare_datasets(file1_path, file2_path)

# Convert to HTML only if the DataFrames are valid
common_rows_html, unique_to_file1_html, unique_to_file2_html = convert_to_html(common_rows, unique_to_file1, unique_to_file2)

# If HTML is successfully generated, you can use it
if common_rows_html:
    print(common_rows_html)
if unique_to_file1_html:
    print(unique_to_file1_html)
if unique_to_file2_html:
    print(unique_to_file2_html)
