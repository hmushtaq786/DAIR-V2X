import argparse
import os
import shutil
from gen_kitti.label_lidarcoord_to_cameracoord import gen_lidar2cam
from gen_kitti.label_json2kitti import json2kitti, rewrite_label, label_filter
from gen_kitti.gen_calib2kitti import gen_calib2kitti
from gen_kitti.gen_ImageSets_from_split_data import gen_ImageSet_from_split_data
from utils import pcd2bin

parser = argparse.ArgumentParser("Generate the Kitti Format Data")
parser.add_argument("--source-root", type=str, required=True, help="Raw data root about DAIR-V2X.")
parser.add_argument("--target-root", type=str, required=True, help="Target root for generated KITTI format data.")
parser.add_argument("--split-path", type=str, required=True, help="Path to the split data JSON.")
parser.add_argument("--label-type", type=str, default="lidar", help="Label type ('lidar' or 'camera').")
parser.add_argument("--sensor-view", type=str, default="vehicle", help="Sensor view ('infrastructure' or 'vehicle').")
parser.add_argument("--no-classmerge", action="store_true", help="Skip class merging.")
parser.add_argument("--temp-root", type=str, default="./tmp_file", help="Temporary intermediate file root.")

def mdkir_kitti(target_root):
    os.makedirs(os.path.join(target_root, "training/calib"), exist_ok=True)
    os.makedirs(os.path.join(target_root, "training/label_2"), exist_ok=True)
    os.makedirs(os.path.join(target_root, "training/image_2"), exist_ok=True)
    os.makedirs(os.path.join(target_root, "training/velodyne"), exist_ok=True)
    os.makedirs(os.path.join(target_root, "ImageSets"), exist_ok=True)

def rawdata_copy(source_root, target_root):
    src_image = os.path.join(source_root, "image")
    dest_image = os.path.join(target_root, "training/image_2")
    src_velodyne = os.path.join(source_root, "velodyne")
    dest_velodyne = os.path.join(target_root, "training/velodyne")

    if os.path.exists(src_image):
        shutil.copytree(src_image, dest_image, dirs_exist_ok=True)
    if os.path.exists(src_velodyne):
        shutil.copytree(src_velodyne, dest_velodyne, dirs_exist_ok=True)

def kitti_pcd2bin(target_root):
    pcd_dir = os.path.join(target_root, "training/velodyne")
    if not os.path.exists(pcd_dir):
        print(f"Directory {pcd_dir} does not exist. Please verify the source data.")
        return

    for fileName in os.listdir(pcd_dir):
        if ".pcd" in fileName:
            print(fileName)
            pcd_file_path = os.path.join(pcd_dir, fileName)
            bin_file_path = os.path.join(pcd_dir, fileName.replace(".pcd", ".bin"))
            pcd2bin(pcd_file_path, bin_file_path)


if __name__ == "__main__":
    print("================ Start to Convert ================")
    args = parser.parse_args()
    source_root = args.source_root
    target_root = args.target_root

    print("================ Start to Copy Raw Data ================")
    mdkir_kitti(target_root)
    rawdata_copy(source_root, target_root)
    kitti_pcd2bin(target_root)

    print("================ Start to Generate Label ================")
    temp_root = args.temp_root
    os.makedirs(temp_root, exist_ok=True)
    gen_lidar2cam(source_root, temp_root, label_type=args.label_type)

    json_root = os.path.join(temp_root, "label", args.label_type)
    kitti_label_root = os.path.join(target_root, "training/label_2")
    json2kitti(json_root, kitti_label_root)
    if not args.no_classmerge:
        rewrite_label(kitti_label_root)
    label_filter(kitti_label_root)

    shutil.rmtree(temp_root)

    print("================ Start to Generate Calibration Files ================")
    path_camera_intrinsic = os.path.join(source_root, "calib/camera_intrinsic")
    path_lidar_to_camera = os.path.join(source_root, "calib/virtuallidar_to_camera")
    path_calib = os.path.join(target_root, "training/calib")
    gen_calib2kitti(path_camera_intrinsic, path_lidar_to_camera, path_calib)

    print("================ Start to Generate ImageSet Files ================")
    ImageSets_path = os.path.join(target_root, "ImageSets")
    gen_ImageSet_from_split_data(ImageSets_path, args.split_path, args.sensor_view)
