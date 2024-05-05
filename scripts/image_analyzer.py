#!/usr/bin/python
# Sample program or step 2 in becoming a DFIR Wizard!
# No license as this code is simple and free!
import sys
import pytsk3
import datetime


def print_partition_info(partition):
    print(
        f"Partition: {partition.addr}, Type: {partition.desc}, Start: {partition.start}, Size: {partition.len}, Flag: {partition.flags}")


'''
TO-DO:
* handle try catch when iterating over partitions with their .start and 512 offset value
* 
'''


def process_partitions(imagehandle):
    partitionTable = pytsk3.Volume_Info(imagehandle)
    for partition in partitionTable:
        print_partition_info(partition)
        #if partition.desc.decode() != "Unallocated":
        #offset_bytes = partition.start + partition.len  # Calculate offset in bytes
        filesystemObject = pytsk3.FS_Info(imagehandle, offset=32 * 512)
        print("FS: ", filesystemObject.info.ftype)
        try:
            fileobject = filesystemObject.open("/$MFT")
            print("File Inode:", fileobject.info.meta.addr)
            print("File Name:", fileobject.info.name.name)
            print("File Creation Time:",
                  datetime.datetime.fromtimestamp(fileobject.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            print("Error opening $MFT:", e)


if __name__ == "__main__":
    imagefile = "../testObject/forensicstick.dd"
    imagehandle = pytsk3.Img_Info(imagefile)
    process_partitions(imagehandle)
