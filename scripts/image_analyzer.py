import os
import pytsk3
import datetime

'''
TO-DO:
* use argparse to pass path of image
'''


def print_partition_info(partition):
    print(
        f"Partition: {partition.addr}, Type: {partition.desc}, Start: {partition.start}, Size: {partition.len}, Flag: {partition.flags}")

def list_directories(filesystem_object, directory_path="/"):
    directory = filesystem_object.open_dir(directory_path)
    for entry in directory:
        if entry.info.name.name.decode() not in [".", ".."]:
            full_path = os.path.join(directory_path, entry.info.name.name.decode())
            print(full_path)
            if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                list_directories(filesystem_object, full_path)
            else:
                try:
                    file_object = filesystem_object.open(full_path)
                    meta_info = file_object.info.meta
                    print("File Metadata:")
                    print("Inode:", meta_info.addr)
                    print("Name:", file_object.info.name.name.decode())
                    print("Size:", meta_info.size)
                    print("Creation Time:", datetime.datetime.fromtimestamp(meta_info.crtime).strftime('%Y-%m-%d %H:%M:%S'))
                except Exception as e:
                    print(f"Error accessing file metadata: {e}")


def save_pdf_file(filesystem_object, file_path, output_path):
    try:
        file_object = filesystem_object.open(file_path)
        meta_info = file_object.info.meta
        print("File Metadata:")
        print("Inode:", meta_info.addr)
        print("Name:", file_object.info.name.name.decode())
        print("Size:", meta_info.size)
        print("Creation Time:", datetime.datetime.fromtimestamp(meta_info.crtime).strftime('%Y-%m-%d %H:%M:%S'))

        # Read and save file data
        file_data = file_object.read_random(0, meta_info.size)
        with open(output_path, 'wb') as f:
            f.write(file_data)
        print(f"PDF file saved to: {output_path}")
    except Exception as e:
        print(f"Error opening or reading file: {e}")


def process_partition(imagehandle):
    partitionTable = pytsk3.Volume_Info(imagehandle)
    for partition in partitionTable:
        try:
            print_partition_info(partition)
            filesystemObject = pytsk3.FS_Info(imagehandle, offset=partition.start * 512)
            #print("File System: ", filesystemObject.info.ftype)
            list_directories(filesystemObject)
        except Exception as e:
            #print(f"Error processing partition: {e}")
            continue
    #file_path = "/lost+found"
    #output_path = "/lost+found"
    #save_pdf_file(filesystemObject, file_path, output_path)
    #except Exception as e:
    #   print(f"Error processing NTFS partition: {e}")


if __name__ == "__main__":
    imagefile = "../testObject/forensicstick.dd"
    imagehandle = pytsk3.Img_Info(imagefile)
    #process_ntfs_partition(imagehandle)
    process_partition(imagehandle)
