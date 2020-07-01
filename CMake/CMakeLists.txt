set(PKG_DESC "Random Forest / Hough Voting Detection Algorithm")
set(pkg_conf_file ${CMAKE_CURRENT_BINARY_DIR}/pyrf.pc)
configure_file(pyrf.pc.in ${pkg_conf_file} @ONLY)
install(
  FILES ${pkg_conf_file}
  DESTINATION ${PYRF_LIB_INSTALL_DIR}/pkgconfig/
  COMPONENT pkgconfig)
