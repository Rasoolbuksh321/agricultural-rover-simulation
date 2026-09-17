# Agricultural Rover Simulation – ROS 2 & Gazebo

This repository contains the ROS 2 and Gazebo simulation environment developed for an agricultural mobile rover.

The project includes the rover model, agricultural Gazebo environment, rover meshes, ROS 2 packages, launch files, keyboard control scripts, and the current simulation configuration.

## Current Features

- Agricultural field simulation in Gazebo
- Four-wheel mobile rover model
- Rover model based on Fusion 360 exported meshes
- Agricultural environment with crop rows, soil, trees, and obstacles
- Differential-drive based rover movement
- Keyboard control
- ROS 2 workspace structure
- Automatic Gazebo world launch and rover spawning
- LiDAR model included in the rover design

## System Used for Development

The current simulation was developed and tested using:

- Ubuntu 24.04
- ROS 2 Rolling
- Gazebo Harmonic
- Gazebo Sim 8
- Python 3
- colcon
- ament_cmake

The simulation was developed inside an Ubuntu virtual machine.

> Note: ROS 2 Rolling is a continuously updated ROS distribution. Package availability may change over time.

## Repository Structure

```text
rover_ws/
├── README.md
└── src/
    ├── rover_description/
    │   ├── CMakeLists.txt
    │   ├── package.xml
    │   ├── launch/
    │   ├── meshes/
    │   └── urdf/
    │
    └── rover_gazebo/
        ├── CMakeLists.txt
        ├── package.xml
        ├── launch/
        │   └── agri_sim.launch.py
        ├── models/
        │   └── wave_rover/
        │       ├── model.config
        │       └── model.sdf
        ├── scripts/
        └── worlds/
            ├── agri_world.sdf
            └── empty_world.sdf
```

## Rover Description

The `rover_description` package contains the rover description files and the original rover meshes exported from Fusion 360.

The meshes include:

- Chassis
- Front-left wheel
- Front-right wheel
- Rear-left wheel
- Rear-right wheel
- LiDAR sensor model

The rover URDF/Xacro description is located in:

```bash
src/rover_description/urdf/
```

## Gazebo Simulation

The `rover_gazebo` package contains the Gazebo simulation files.

The main agricultural environment is:

```bash
src/rover_gazebo/worlds/agri_world.sdf
```

The Gazebo rover model is:

```bash
src/rover_gazebo/models/wave_rover/model.sdf
```

The agricultural environment currently contains crop rows, soil areas, trees, posts, and obstacles for rover testing.

## Building the Workspace

Open a terminal and go to the workspace:

```bash
cd ~/rover_ws
```

Source ROS 2:

```bash
source /opt/ros/rolling/setup.bash
```

Build the workspace:

```bash
colcon build --symlink-install
```

After the build completes, source the workspace:

```bash
source install/setup.bash
```

## Running the Complete Simulation

The recommended method is to use the ROS 2 launch file.

First source ROS 2 and the workspace:

```bash
cd ~/rover_ws
source /opt/ros/rolling/setup.bash
source install/setup.bash
```

Then launch the simulation:

```bash
ros2 launch rover_gazebo agri_sim.launch.py
```

This launch file:

1. Starts Gazebo Sim.
2. Loads the agricultural field.
3. Spawns the rover automatically in the environment.

The rover is currently spawned near:

```text
x = -8
y = -8
z = 0.10
```

## Running Gazebo Manually

The agricultural world can also be started directly using:

```bash
gz sim ~/rover_ws/src/rover_gazebo/worlds/agri_world.sdf
```

After Gazebo opens, make sure the simulation is running and is not paused.

## Keyboard Control

Keyboard control scripts are located in:

```bash
src/rover_gazebo/scripts/
```

The main shell controller can be started using:

```bash
cd ~/rover_ws
./src/rover_gazebo/scripts/rover_keys.sh
```

The current controls are:

```text
w = Forward
s = Backward
a = Left
d = Right
x = Stop
q = Quit
```

The rover receives movement commands through the Gazebo `/cmd_vel` topic.

## Gazebo Resource Path

Gazebo must be able to locate the rover model.

If required, set the model resource path with:

```bash
export GZ_SIM_RESOURCE_PATH=$HOME/rover_ws/src/rover_gazebo/models:$GZ_SIM_RESOURCE_PATH
```

## Dependencies

The main software required for the project is:

- Ubuntu
- ROS 2 Rolling
- Gazebo Harmonic / Gazebo Sim 8
- Python 3
- colcon
- ament_cmake

ROS 2 must be installed and available at:

```bash
/opt/ros/rolling/
```

Gazebo installation can be checked with:

```bash
gz sim --versions
```

ROS 2 installation can be checked with:

```bash
ros2 --help
```

## Current Project Status

The following parts of the project are currently operational:

- ROS 2 workspace builds successfully
- Agricultural Gazebo world loads successfully
- Rover model loads in Gazebo
- Rover can be spawned automatically using the launch file
- Rover can move inside the agricultural environment
- Basic keyboard control is available
- Rover physics and stability have been improved
- Fusion 360 rover geometry has been integrated into the simulation

## Planned Development

The next development stages include:

- Further rover control refinement
- LiDAR sensor integration and validation
- Gazebo-to-ROS 2 sensor communication
- ROS 2 topic verification
- RViz visualization
- SLAM and mapping
- Agricultural autonomous navigation experiments

## Troubleshooting

### Gazebo graphics warnings

When Gazebo is running inside a virtual machine, warnings such as:

```text
VMware: No 3D enabled
libEGL warning
```

may appear.

If the Gazebo graphical interface opens and the simulation runs correctly, these warnings do not necessarily prevent the simulation from operating.

### ROS Rolling warning

On Ubuntu 24.04, ROS Rolling may display a warning indicating that Rolling has migrated to a newer Ubuntu release.

The current development environment was nevertheless created and tested with the installed ROS 2 Rolling setup on Ubuntu 24.04.

## Author

Rasool Buksh

Agricultural Rover Simulation Project
