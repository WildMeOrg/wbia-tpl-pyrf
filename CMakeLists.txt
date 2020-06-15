cmake_minimum_required(VERSION 2.13.0)

include(cmake/VersionDiscovery.cmake)
discover_version()
# CMP0048 is used to enable `project()` to manage `VERSION` & `VERSION*` variables
cmake_policy(SET CMP0048 NEW)

#######################################

project(pydarknet VERSION "${DISCOVERED_VERSION}" LANGUAGES C CXX)
set(CMAKE_BUILD_TYPE "Release")

option(CUDA "build with cuda" Off)
set(CFLAGS -Wall -O2)


#######################################
# Find required packages

if (APPLE)
  # Include Homebrew installed libraries
  message("USING Homebrew")
  include_directories(/usr/local/include)
  link_directories(/usr/local/lib)
endif()

message(STATUS "Checking OpenCV")
find_package( OpenCV REQUIRED )
add_definitions(-DOPENCV)
include_directories(${OpenCV_INCLUDE_DIRS})



# #######################################
# # Clang2 = Clang + OpenMP built for OSX Mavericks
# # http://goo.gl/1Tg0Zj
# if (APPLE)
#     set(CMAKE_MACOSX_RPATH 1)
#     message("Detected APPLE system")
#     SET(CLANG2 Off)
# endif()

# if (APPLE AND CLANG2)
# 	message("Using clang2")
#     set(CMAKE_C_COMPILER "clang2")
#     set(CMAKE_CXX_COMPILER "clang2++")
# endif()
# #######################################
# #######################################
# if(APPLE AND CLANG2)
#     # Add flags to support clang2
#     message("APPLE + CLANG2: Adding stdlib flags for clang")
#     set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -stdlib=libc++")
#     set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++")
#     set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -lc++")
#     set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -lc++")
# endif()
# #######################################

message(STATUS "Checking OpenMP")
find_package(OpenMP)
IF(OPENMP_FOUND)
    message("Found OpenMP! ^_^")
    # add flags for OpenMP
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS} -fopenmp")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS} -fopenmp")
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} ${OpenMP_C_FLAGS} ${OpenMP_SHARED_LINKER_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_C_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
ELSE()
    message(FATAL_ERROR "Missed OpenMP! x_x")
ENDIF()

#######################################

set(
  SOURCE_FILES
  src/CRForestDetector.cpp
  src/CRPatch.cpp
  src/CRTree.cpp
  src/HoG.cpp
)


#######################################


#######################################
# Define library targets

file(GLOB SOURCE_FILES "src/*.cpp")
file(GLOB HEADER_FILES "src/*.h")

add_library(pyrf SHARED src/pyrf.cpp ${SOURCE_FILES})
target_link_libraries(pyrf ${OpenCV_LIBS})

if (SKBUILD)
  install(TARGETS pyrf DESTINATION pyrf/lib)
  install(FILES ${HEADER_FILES} DESTINATION pyrf/include)
else ()
  install(TARGETS ${install_target} DESTINATION lib)
  install(FILES ${HEADER_FILES} DESTINATION include)
endif()
