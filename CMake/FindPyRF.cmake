# ##############################################################################
# Find PyRF
#
# This sets the following variables: PYRF_FOUND - True if pyrf was found.
# PYRF_INCLUDE_DIRS - Directories containing the pyrf include files.
# PYRF_LIBRARIES - Libraries needed to use pyrf. PYRF_DEFINITIONS - Compiler
# flags for pyrf.

find_package(PkgConfig)
pkg_check_modules(PC_PYRF pyrf)
set(PYRF_DEFINITIONS ${PC_PYRF_CFLAGS_OTHER})

find_path(PYRF_INCLUDE_DIR pyrf/pyrf.hpp HINTS ${PC_PYRF_INCLUDEDIR}
                                               ${PC_PYRF_INCLUDE_DIRS})

find_library(PYRF_LIBRARY pyrf HINTS ${PC_PYRF_LIBDIR} ${PC_PYRF_LIBRARY_DIRS})

set(PYRF_INCLUDE_DIRS ${PYRF_INCLUDE_DIR})
set(PYRF_LIBRARIES ${PYRF_LIBRARY})

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(PyRF DEFAULT_MSG PYRF_LIBRARY
                                  PYRF_INCLUDE_DIR)

mark_as_advanced(PYRF_LIBRARY PYRF_INCLUDE_DIR)
