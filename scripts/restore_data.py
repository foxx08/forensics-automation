import os
import pytsk3


def save_files(filesystem_object, file_path, output_directory):
    try:
        file_object = filesystem_object.open(file_path)
        file_data = file_object.read_random(0, file_object.info.meta.size)
        output_path = os.path.join(output_directory, file_path.strip("/"))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(file_data)
        print(f"File saved to: {output_path}")
    except Exception as e:
        print(f"Error opening or reading file: {e}")


def list_directory_recursive(filesystem_object, directory_path, output_directory):
    directory = filesystem_object.open_dir(directory_path)
    for entry in directory:
        if entry.info.name.name.decode() not in [".", ".."]:
            full_path = os.path.join(directory_path, entry.info.name.name.decode())
            if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                list_directory_recursive(filesystem_object, full_path, output_directory)
            else:
                save_files(filesystem_object, full_path, output_directory)


def process_ntfs_partition(imagehandle, output_directory):
    filesystem_object = pytsk3.FS_Info(imagehandle, offset=32 * 512)
    try:
        list_directory_recursive(filesystem_object, "/", output_directory)
    except Exception as e:
        print(f"Error processing NTFS partition: {e}")


if __name__ == "__main__":
    imagefile = "../testObject/forensicstick.dd"
    output_directory = "../testObject/partition_extraction"
    os.makedirs(output_directory, exist_ok=True)
    imagehandle = pytsk3.Img_Info(imagefile)
    process_ntfs_partition(imagehandle, output_directory)
