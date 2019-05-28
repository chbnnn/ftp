# ftp
python command line ftp

- 支持的命令：
  - 服务器端:
    - **ls [-l]**
    - **cd**
    - **upload** file_or_directory [name]: 不区分单个文件或文件夹；如果提供第二个参数，则以该名字上传文件；
    - **download** file_or_directory [name]: 同upload
    - **rm**
    - **mkdir**
    - **rmdir**
    - **debuglevel**: 可选参数0，1，2
  - 本地：
    - **pwd** (服务器当前目录显示在Chinbing 远程目录>)
    - **lcd**: local cd
    - **lls [-l]**: local ls
  - 退出：
    - **exit**


![运行结果](/result.png)

(meicuo, jiushi baozhuang yixia ftplib de jiekou eryi)
(gongxian jiushi zengjia le yiliangge mingling, kanqilai haoyong yidiandian)
