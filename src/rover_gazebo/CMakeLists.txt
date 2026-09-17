cmake_minimum_required(VERSION 3.20)
project(rover_gazebo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)

  # Skip copyright check for now
  set(ament_cmake_copyright_FOUND TRUE)

  # Skip cpplint check for now
  set(ament_cmake_cpplint_FOUND TRUE)

  ament_lint_auto_find_test_dependencies()
endif()

install(
  DIRECTORY launch worlds config models scripts
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
