import os
import pytsk3
import datetime
import argparse

def process_arguments():
    parser = argparse.ArgumentParser(description="Script to analyze an image file")
    parser.add_argument("--image-path", required=True, help="Path to the image file")
    return parser.parse_args()

def print_partition_info(partition):
    print(f"Partition: {partition.addr}, Type: {partition.desc}, Start: {partition.start}, Size: {partition.len}, Flag: {partition.flags}")

# def list_directories(filesystem_object, directory_path="/"):
#     directory = filesystem_object.open_dir(directory_path)
#     for entry in directory:
#         if entry.info.name.name.decode() not in [".", ".."]:
#             full_path = os.path.join(directory_path, entry.info.name.name.decode())
#             print(full_path)
#             if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
#                 list_directories(filesystem_object, full_path)
#             else:
#                 try:
#                     file_object = filesystem_object.open(full_path)
#                     meta_info = file_object.info.meta
#                     print("File Metadata:")
#                     print("Inode:", meta_info.addr)
#                     print("Name:", file_object.info.name.name.decode())
#                     print("Size:", meta_info.size)
#                     print("Creation Time:", datetime.datetime.fromtimestamp(meta_info.crtime).strftime('%Y-%m-%d %H:%M:%S'))
#                 except Exception as e:
#                     print(f"Error accessing file metadata: {e}")

def process_partition(imagehandle):
    partitionTable = pytsk3.Volume_Info(imagehandle)
    for partition in partitionTable:
        try:
            print_partition_info(partition)
            #filesystemObject = pytsk3.FS_Info(imagehandle, offset=32 * 512)
            #list_directories(filesystemObject)
        except Exception as e:
            print(f"Error processing partition: {e}")

if __name__ == "__main__":
    args = process_arguments()
    imagefile = args.image_path
    imagehandle = pytsk3.Img_Info(imagefile)
    process_partition(imagehandle)
