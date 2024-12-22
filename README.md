<div align="center">   
  
# DAIR-V2X and OpenDAIRV2X: Towards General and Real-World Cooperative Autonomous Driving

</div>

<h3 align="center">
    <a href="https://thudair.baai.ac.cn/index">Project Page</a> |
    <a href="#dataset">Dataset Download</a> |
    <a href="https://arxiv.org/abs/2204.05575">arXiv</a> |
    <a href="https://github.com/AIR-THU/DAIR-V2X/">OpenDAIRV2X</a> 
</h3>

<br><br>

Follow the steps below for preparing the dataset conversion into KITTI format.
1) Rearrange the data content in the given structure:
    ├── cooperative-vehicle-infrastructure
        ├── infrastructure-side
            ├── image		    
                ├── {id}.jpg
            ├── velodyne                
                ├── {id}.pcd           
            ├── calib                 
                ├── camera_intrinsic            
                    ├── {id}.json    
                ├── virtuallidar_to_camera  
                    ├── {id}.json
            ├── label	
                ├── camera       
                    ├── {id}.json
                ├── virtuallidar 
                    ├── {id}.json
            ├── data_info.json   
