# robot_sim_mujoco

a separate repo for robot sim

## Installation

### UnitreeSDK2Python

To install UnitreeSDK2Python with custom configuration, follow these steps:

```bash
project_path=$(pwd) && \
rm -rf third_party && mkdir third_party && \
git clone https://github.com/eclipse-cyclonedds/cyclonedds -b releases/0.10.x $project_path/third_party/cyclonedds  && \
cd cyclonedds && mkdir build install && cd build  && \
cmake .. -DCMAKE_INSTALL_PREFIX=../install  && \
cmake --build . --target install  && \
cd $project_path && \
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git $project_path/third_party/unitree_sdk2_python
```

```bash
project_path=$(pwd) && \
CYCLONEDDS_HOME="$project_path/third_party/cyclonedds/install" && \
cd $project_path/third_party/unitree_sdk2_python && \
pip install -e .
```
