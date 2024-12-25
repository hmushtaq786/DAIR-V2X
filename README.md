# DAIR-V2X and OpenDAIRV2X: Towards General and Real-World Cooperative Autonomous Driving

<div align="center">
	<h3>
		<a href="https://thudair.baai.ac.cn/index">Project Page</a> |
		<a href="https://arxiv.org/abs/2204.05575">arXiv</a> |
		<a href="https://github.com/AIR-THU/DAIR-V2X/">OpenDAIRV2X</a>
	</h3>
</div>

---

## Dataset Preparation for Conversion to KITTI Format

Follow the steps below to prepare the DAIR-V2X dataset for conversion into the KITTI format.

### 1. Rearrange the Data Content

- Organize the data into the following directory structure:

<pre>
cooperative-vehicle-infrastructure/
	├── infrastructure-side/
		├── image/
			├── {id}.jpg
		├── velodyne/
			├── {id}.pcd
		├── calib/
			├── camera_intrinsic/
				├── {id}.json
			├── virtuallidar_to_camera/
				├── {id}.json
		├── label/
			├── camera/
				├── {id}.json
			├── virtuallidar/
				├── {id}.json
		├── data_info.json
</pre>

- Place the resulted "cooperative-vehicle-infrastructure" folder under data/DAIR-V2X/

### 2. Execute the code

- Once in the repository folder, run the following command:

<pre>
python tools/dataset_converter/dair2kitti.py --source-root ./data/DAIR-V2X/cooperative-vehicle-infrastructure/infrastructure-side --target-root ./data/DAIR-V2X/KITTI --split-path ./data/split_datas/single-infrastructure-split-data.json --label-type lidar --sensor-view infrastructure --no-classmerge
</pre>

### 2. Successful output

- Once the code has finished processing, the resulted data in KITTI format will be available in data/DAIR-V2X/KITTI
