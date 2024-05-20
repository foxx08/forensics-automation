import os
import hashlib
import csv
import argparse
import filetype


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Performs superficial file analysis and generate reports in CSV format.")
    parser.add_argument('--folder-path', required=True, help='Path to the folder to be analyzed')
    parser.add_argument('--subfolder-path', required=True, help='Path to the subfolder')
    args = parser.parse_args()
    return args.folder_path, args.subfolder_path


def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def find_duplicates(folder_path):
    duplicates = {}
    for root, dirs, files in os.walk(folder_path):
        print(f"Analyzing folder: {root}")
        for filename in files:
            file_path = os.path.join(root, filename)
            print(f"Processing file: {file_path}")
            file_hash = calculate_md5(file_path)
            if file_hash in duplicates:
                duplicates[file_hash].append(file_path)
            else:
                duplicates[file_hash] = [file_path]

    duplicates = {key: value for key, value in duplicates.items() if len(value) > 1}

    with open(folder_path + 'detected_duplicates.csv', 'w+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Hash', 'Duplicate Count', 'File Paths'])
        for hash_value, files in duplicates.items():
            csvwriter.writerow([hash_value, len(files), "; ".join(files)])

    print(f"\nDuplicate files have been written to {folder_path}")


def identify_large_files(folder_path, size_threshold=10 * 1024 * 1024):
    large_files = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_size = os.path.getsize(file_path)
            if file_size > size_threshold:
                large_files.append((file_path, file_size))

    # Writing to CSV
    with open(folder_path + 'large_files.csv', 'w+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Path', 'File Size'])
        for file_path, file_size in large_files:
            csvwriter.writerow([file_path, file_size])

    print(f"\nLarge files have been written to {folder_path}")


def identify_file_types(folder_path, subfolder_path):
    directory = folder_path + subfolder_path
    file_types = {}

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_type = filetype.guess(file_path)
            if file_type is not None:
                mime_type = file_type.mime
                if mime_type in file_types:
                    file_types[mime_type].append(file_path)
                else:
                    file_types[mime_type] = [file_path]

    with open(os.path.join(folder_path, 'filetypes_active_files.csv'), 'w+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['MIME Type', 'File Paths'])
        for mime_type, files in file_types.items():
            csvwriter.writerow([mime_type, "; ".join(files)])

    print(f"\nFiletypes of PATH: {subfolder_path} have been written to {folder_path}")


if __name__ == "__main__":
    folder_path, subfolder_path = parse_arguments()
    find_duplicates(folder_path)
    identify_large_files(folder_path)
    identify_file_types(folder_path, subfolder_path)
