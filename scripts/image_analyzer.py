import os
import pytsk3
import argparse
import csv
import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(description="Analyze a forensic image and generate a report in CSV format.")
    parser.add_argument("--image-path", required=True, help="Path to the image file")
    parser.add_argument("--output-csv", required=True, help="Path to save the report (CSV file)")
    args = parser.parse_args()
    return args.image_path, args.output_csv


def list_directories(filesystem_object, directory_path="/"):
    file_metadata_list = []
    directory = filesystem_object.open_dir(directory_path)
    for entry in directory:
        if entry.info.name.name.decode() not in [".", ".."]:
            full_path = os.path.join(directory_path, entry.info.name.name.decode())
            if entry.info.meta and entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                file_metadata_list.extend(list_directories(filesystem_object, full_path))
            else:
                try:
                    if entry.info.meta:
                        file_object = filesystem_object.open(full_path)
                        meta_info = file_object.info.meta
                        file_metadata = {
                            'Path': full_path,
                            'Inode': meta_info.addr,
                            'Name': file_object.info.name.name.decode(),
                            'Size': meta_info.size,
                            'Creation Time': datetime.datetime.fromtimestamp(meta_info.crtime).strftime('%Y-%m-%d %H:%M:%S')
                        }
                        file_metadata_list.append(file_metadata)
                except Exception as e:
                    print(f"Error accessing file metadata: {e}")
    return file_metadata_list



def get_partition_info(imagehandle):
    partition_info_list = []
    partitionTable = pytsk3.Volume_Info(imagehandle)
    for partition in partitionTable:
        try:
            partition_info = {
                'Partition': partition.addr,
                'Type': partition.desc.decode(),
                'Start': partition.start,
                'Size': partition.len,
                'Flag': partition.flags
            }
            partition_info_list.append(partition_info)
            partition_start = partition.start
            #print("Hello",partition_start)
            #filesystemObject = pytsk3.FS_Info(imagehandle, offset=partition_start * 512)
            #list_directories(filesystemObject)
        except Exception as e:
            print(f"Error processing partition: {e}")
    return partition_info_list


########################################################################################################################
def save_partition_info_to_csv(partition_info, output_csv):
    file_exists = os.path.isfile(output_csv)
    with open(output_csv + 'partitionInfo.csv', 'w+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(['Partition', 'Type', 'Start', 'Size', 'Flag'])
        for info in partition_info:
            writer.writerow([info['Partition'], info['Type'], info['Start'], info['Size'], info['Flag']])
    print(f"Partition info saved to {output_csv}")


def save_file_metadata_to_csv(file_metadata, output_csv):
    file_exists = os.path.isfile(output_csv)
    with open(output_csv + 'fileMetadata.csv', 'w+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(['Path', 'Inode', 'Name', 'Size', 'Creation Time'])
        for metadata in file_metadata:
            writer.writerow([metadata['Path'], metadata['Inode'], metadata['Name'], metadata['Size'], metadata['Creation Time']])
    print(f"File metadata saved to {output_csv}")


'''
TO-DO:
* create meta data csv file for each partition and name those files accordingly
 
'''

if __name__ == "__main__":
    image_path, output_csv = parse_arguments()
    imagehandle = pytsk3.Img_Info(image_path)

    partition_info = get_partition_info(imagehandle)
    save_partition_info_to_csv(partition_info, output_csv)

    file_metadata = list_directories(pytsk3.FS_Info(imagehandle, offset=32 * 512))
    save_file_metadata_to_csv(file_metadata, output_csv)
