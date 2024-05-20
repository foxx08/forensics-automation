import os
import pytsk3
import argparse
from image_analyzer import list_directories


def parse_arguments():
    parser = argparse.ArgumentParser(description="Restore active data from an image's partition")
    parser.add_argument("--image-path", required=True, help="Path to the image file")
    parser.add_argument("--partitions-start", required=True, help="Comma-separated list of partition start sectors")
    parser.add_argument("--output-directory", required=True, help="Directory to save restored data")
    args = parser.parse_args()
    return args.image_path, args.partitions_start, args.output_directory


def save_files(filesystem_object, file_metadata, output_directory):
    for metadata in file_metadata:
        file_path = metadata['Path']
        try:
            file_object = filesystem_object.open(file_path)
            file_data = file_object.read_random(0, file_object.info.meta.size)
            output_path = os.path.join(output_directory, file_path.strip("/"))
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(file_data)
            print(f"File saved to: {output_path}")
        except Exception as e:
            print(f"Error opening or reading file {file_path}: {e}")


def process_partition(imagehandle, partition_start, output_directory):
    filesystem_object = pytsk3.FS_Info(imagehandle, offset=partition_start * 512)
    try:
        file_metadata = list_directories(filesystem_object)
        save_files(filesystem_object, file_metadata, output_directory)
    except Exception as e:
        print(f"Error processing NTFS partition starting at sector {partition_start}: {e}")


if __name__ == "__main__":
    image_path, partitions_start, output_directory = parse_arguments()
    #partition = [int(sector) for sector in partitions_start.split(',')]
    os.makedirs(output_directory, exist_ok=True)
    imagehandle = pytsk3.Img_Info(image_path)

    #for partition_start in partitions_start:
    partition_output_dir = os.path.join(output_directory)
    os.makedirs(partition_output_dir, exist_ok=True)
    process_partition(imagehandle, int(partitions_start), partition_output_dir)
