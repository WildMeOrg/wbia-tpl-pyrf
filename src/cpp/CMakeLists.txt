# include_directories(${CMAKE_SOURCE_DIR}/include algorithms ext util nn .)

message(STATUS "PYRF_VERSION = ${PYRF_VERSION}")
set(PYRF_VERSION ${PYRF_VERSION})
message(STATUS "PYRF_VERSION = ${PYRF_VERSION}")
add_definitions(-D_PYRF_VERSION=${PYRF_VERSION})
add_definitions(-DPYRF_VERSION_=${PYRF_VERSION})
add_definitions(-DPYRF_VERSION=${PYRF_VERSION})
add_definitions(-D_PYRF_VERSION=${PYRF_VERSION})
add_definitions(-DPYRF_VERSION_=${PYRF_VERSION})
add_definitions(-DPYRF_VERSION=${PYRF_VERSION})

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/pyrf/config.h.in
               ${CMAKE_CURRENT_SOURCE_DIR}/pyrf/config.h)

set(CPP_SOURCES
    ${CMAKE_CURRENT_SOURCE_DIR}/pyrf/CRForestDetector.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/pyrf/CRPatch.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/pyrf/CRTree.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/pyrf/HoG.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/pyrf/pyrf.cpp)

add_library(pyrf_s STATIC ${CPP_SOURCES})
target_link_libraries(pyrf_s ${OpenCV_LIBS})

if(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_CLANG)
  set_target_properties(pyrf_s PROPERTIES COMPILE_FLAGS -fPIC)
endif()

set_property(TARGET pyrf_s PROPERTY COMPILE_DEFINITIONS PYRF_STATIC)

add_library(pyrf SHARED "${CMAKE_CURRENT_SOURCE_DIR}/pyrf/pyrf.h")

if(OS_IS_LINUX)
  set_target_properties(pyrf PROPERTIES LINKER_LANGUAGE CXX)
  set(LINK_FLAG_PREFIX "-Wl,--whole-archive")
  set(LINK_FLAG_POSTFIX "-Wl,--no-whole-archive")
elseif(OS_IS_MACOS)
  set(LINK_FLAG_PREFIX "-Wl,-all_load")
else()
  set_target_properties(pyrf PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS YES)
  set(LINK_FLAG_PREFIX "/WHOLEARCHIVE")
endif()

target_link_libraries(pyrf ${LINK_FLAG_PREFIX} pyrf_s ${LINK_FLAG_POSTFIX})

set_target_properties(
  pyrf PROPERTIES VERSION ${PYRF_VERSION} SOVERSION ${PYRF_SOVERSION}
                  DEFINE_SYMBOL PYRF_EXPORTS)

if(NOT SKBUILD)
  install(
    TARGETS pyrf pyrf_s
    EXPORT ${targets_export_name}
    INCLUDES
    DESTINATION include
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION ${PYRF_LIB_INSTALL_DIR}
    ARCHIVE DESTINATION ${PYRF_LIB_INSTALL_DIR})

  install(
    DIRECTORY pyrf
    DESTINATION include
    FILES_MATCHING
    PATTERN "*.h"
    PATTERN "*.hpp")

else()
  # Only install the library files when building with skbuild
  install(
    TARGETS pyrf pyrf_s
    EXPORT ${targets_export_name}
    LIBRARY DESTINATION ${PYRF_LIB_INSTALL_DIR}
    ARCHIVE DESTINATION ${PYRF_LIB_INSTALL_DIR})
endif()
