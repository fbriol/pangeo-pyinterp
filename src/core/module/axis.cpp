#include "pyinterp/axis.hpp"
#include "pyinterp/detail/broadcast.hpp"
#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pyinterp {

template <typename T>
inline std::vector<T> vector_from_numpy(
    const std::string& name,
    const py::array_t<T, py::array::c_style>& ndarray) {
  detail::check_array_ndim(name, 1, ndarray);
  return std::vector<T>(ndarray.data(), ndarray.data() + ndarray.size());
}

Axis::Axis(const py::array_t<double, py::array::c_style>& points,
           const bool is_circle, const bool is_radian)
    : Axis(vector_from_numpy<double>("points", points), is_circle, is_radian) {}

py::array_t<double> Axis::coordinate_values(const py::slice& slice) const {
  size_t start, stop, step, slicelength;
  if (!slice.compute(size(), &start, &stop, &step, &slicelength)) {
    throw py::error_already_set();
  }

  auto result = py::array_t<double>(slicelength);
  auto _result = result.mutable_unchecked<1>();

  {
    pybind11::gil_scoped_release release;
    for (size_t ix = 0; ix < slicelength; ++ix) {
      _result(ix) = (*this)(ix);
    }
  }
  return result;
}

pybind11::array_t<int64_t> Axis::find_index(
    const pybind11::array_t<double>& coordinates, bool bounded) const {
  detail::check_array_ndim("coordinates", 1, coordinates);

  auto size = coordinates.size();
  auto result = pybind11::array_t<int64_t>(size);
  auto _result = result.mutable_unchecked<1>();
  auto _coordinates = coordinates.unchecked<1>();

  {
    pybind11::gil_scoped_release release;
    for (auto ix = 0; ix < size; ++ix) {
      _result(ix) = detail::Axis::find_index(_coordinates(ix), bounded);
    }
  }
  return result;
}

}  // namespace pyinterp

void init_axis(py::module& m) {
  py::class_<pyinterp::Axis>(m, "Axis", R"__doc__(
A coordinate axis is a Variable that specifies one of the coordinates
of a variable's values.
)__doc__")
      .def(py::init<const py::array_t<double>&, const bool, const bool>(),
           py::arg("values"), py::arg("is_circle") = false,
           py::arg("is_radian") = false, R"__doc__(
Create a coordinate axis from values.
Args:
    values (numpy.ndarray): Axis values.
    is_circle (bool, optional): True, if the axis can represent a
        circle. Defaults to ``false``.
    is_radian (bool, optional): True, if the coordinate system is radian.
        Defaults to ``false``.
)__doc__")
      .def(py::init<double, double, double, bool, bool>(), py::arg("start"),
           py::arg("stop"), py::arg("step"), py::arg("is_circle") = false,
           py::arg("is_radian") = false,
           R"__doc__(
Create a coordinate axis from evenly spaced numbers over a specified
interval.
Args:
    start (float): The first value of the axis.
    stop (float): The last value of the axis.
    num (int): Number of samples in the axis.
    is_circle (bool, optional): True, if the axis can represent a circle.
        Defaults to ``false``.
    is_radian (bool, optional): True, if the coordinate system is radian.
        Defaults to ``false``.
)__doc__")
      .def("__len__",
           [](const pyinterp::Axis& self) -> size_t { return self.size(); })
      .def("__getitem__",
           [](const pyinterp::Axis& self, size_t index) -> double {
             return self.coordinate_value(index);
           })
      .def("__getitem__", &pyinterp::Axis::coordinate_values)
      .def("min_value", &pyinterp::Axis::min_value, R"__doc__(
Get the minimum coordinate value.
Return:
    float: The minimum coordinate value.
)__doc__")
      .def("max_value", &pyinterp::Axis::max_value, R"__doc__(
Get the maximum coordinate value.
Return:
    float: The maximum coordinate value.
)__doc__")
      .def("is_regular", &pyinterp::Axis::is_regular,
           R"__doc__(
Check if this axis values are spaced regularly
Return:
  bool: True if this axis values are spaced regularly
)__doc__")
      .def(
          "find_index",
          [](const pyinterp::Axis& self, const py::array_t<double>& coordinates,
             const bool bounded) -> py::array_t<int64_t> {
            return self.find_index(coordinates, bounded);
          },
          py::arg("coordinates"), py::arg("bounded") = false, R"__doc__(
Given coordinate positions, find what grid elements contains them, or is
closest to them.
Args:
    coordinates (numpy.ndarray): Positions in this coordinate system
    bounded (bool, optional): True if you want to obtain the closest value to
        a coordinate outside the axis definition range.
Return:
    numpy.ndarray: index of the grid points containing them or -1 if the
    ``bounded`` parameter is set to false and if one of the searched indexes
    is out of the definition range of the axis, otherwise the index of the
    closest value of the coordinate is returned.
)__doc__")
      .def("front", &pyinterp::Axis::front, R"__doc__(
Get the first value of this axis
Return:
    float: The first value
)__doc__")
      .def("back", &pyinterp::Axis::back, R"__doc__(
Get the last value of this axis
Return:
    float: The last value
)__doc__")
      .def("is_ascending", &pyinterp::Axis::is_ascending, R"__doc__(
Test if the data is sorted in ascending order.
Return:
    bool: True if the data is sorted in ascending order.
)__doc__")
      .def("increment", &pyinterp::Axis::increment, R"__doc__(
Get increment value if is_regular()
Raises:
    RuntimeError: if this instance does not represent a regular axis
Return:
    float: Increment value
)__doc__")
      .def_property_readonly("is_circle", &pyinterp::Axis::is_circle, R"__doc__(
Test if this axis represents a circle.
Return:
    bool: True if this axis represents a circle
)__doc__")
      .def("__eq__",
           [](const pyinterp::Axis& self, const pyinterp::Axis& rhs) -> bool {
             return self == rhs;
           })
      .def("__ne__",
           [](const pyinterp::Axis& self, const pyinterp::Axis& rhs) -> bool {
             return self != rhs;
           })
      .def("__repr__",
           [](const pyinterp::Axis& self) -> std::string {
             return static_cast<std::string>(self);
           })
      .def(
          py::pickle([](const pyinterp::Axis& self) { return self.getstate(); },
                     [](const py::tuple& state) {
                       return pyinterp::Axis::setstate(state);
                     }));
}
