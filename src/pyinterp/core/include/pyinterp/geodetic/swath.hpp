// Copyright (c) 2022 CNES
//
// All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.
#pragma once
#include <pybind11/eigen.h>

#include <Eigen/Core>
#include <tuple>

#include "pyinterp/detail/broadcast.hpp"
#include "pyinterp/detail/math/orbit.hpp"

namespace pyinterp::geodetic {

/// Calculate the swath coordinates from the swath center coordinates.
template <typename T>
[[nodiscard]] auto calculate_swath(
    const T& delta_ac, const T& half_gap, const int half_swath, const T& radius,
    const pybind11::EigenDRef<const Eigen::Matrix<T, Eigen::Dynamic, 3>>&
        location,
    const pybind11::EigenDRef<const Eigen::Matrix<T, Eigen::Dynamic, 3>>&
        direction)
    -> std::tuple<Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic>,
                  Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic>> {
  detail::check_eigen_shape("location", location, "direction", direction);
  auto lon = Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic>(location.rows(),
                                                              2 * half_swath);
  auto lat = Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic>(location.rows(),
                                                              2 * half_swath);
  auto loc = Eigen::Matrix<T, 3, 1>();

  for (auto ix = 0; ix < location.rows(); ++ix) {
    const auto loc_row = location.row(ix).transpose();
    const auto& dir_row = direction.row(ix);

    for (auto jx = 0; jx < half_swath; ++jx) {
      auto rotation = detail::math::rotation_3d_matrix<T>(
          (-(jx * delta_ac + half_gap) / radius), dir_row);
      auto kx = half_swath + jx;

      loc = rotation * loc_row;
      std::tie(lon(ix, kx), lat(ix, kx)) =
          detail::math::cartesian2spherical<T>(loc[0], loc[1], loc[2]);

      loc = rotation.transpose() * loc_row;
      kx = half_swath - jx - 1;
      std::tie(lon(ix, kx), lat(ix, kx)) =
          detail::math::cartesian2spherical(loc[0], loc[1], loc[2]);
    }
  }
  return std::make_tuple(lon, lat);
}

}  // namespace pyinterp::geodetic
