# The Hazard Library
# Copyright (C) 2012-2015, GEM Foundation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Module :mod:`openquake.hazardlib.geo.surface.gridded` defines
:class:`GriddedSurface`.
"""
import numpy as np

from openquake.hazardlib.geo.geodetic import min_geodetic_distance
from openquake.hazardlib.geo import utils
from openquake.hazardlib.geo.point import Point
from openquake.hazardlib.geo.surface.base import BaseSurface
from openquake.hazardlib.geo.mesh import Mesh


class GriddedSurface(BaseSurface):
    """
    Gridded surface defined by an unstructured cloud of points. This surface
    type is required for a proper implementation of some subduction interface
    surfaces included int the Japan 2012 model.

    Note that currently we support only one rupture-site typology i.e. since
    this the only one that can be unambiguosly computed.

    :param mesh:
        An unstructured mesh of points ideally representing a rupture surface.
        Must be an instance of :class:`~openquake.hazardlib.geo.mesh.Mesh`
    """
    def __init__(self, mesh):
        self.mesh = mesh

    @classmethod
    def from_points_list(cls, points):
        """
        Create a gridded surface from a list of points.

        :parameter points:
            A list of :class:`~openquake.hazardlib.geo.Point`
        :returns:
            An instance of
            :class:`~openquake.hazardlib.geo.surface.gridded.GriddedSurface`
        """

        return cls(Mesh.from_points_list(points))

    def get_bounding_box(self):
        """
        Compute surface geographical bounding box.

        :return:
            A tuple of four items. These items represent western, eastern,
            northern and southern borders of the bounding box respectively.
            Values are floats in decimal degrees.
        """
        return utils.get_spherical_bounding_box(self.mesh.lons, self.mesh.lats)

    def get_min_distance(self, mesh):
        """
        Compute and return the minimum distance from the surface to each point
        of ``mesh``. This distance is sometimes called ``Rrup``.

        :param mesh:
            :class:`~openquake.hazardlib.geo.mesh.Mesh` of points to calculate
            minimum distance to.
        :returns:
            A numpy array of distances in km.
        """
        # return (self.mesh.get_min_distance(mesh))
        dists = min_geodetic_distance(mesh.lons, mesh.lats, self.mesh.lons,
                                      self.mesh.lats)
        return min(dists)

    def get_closest_points(self, mesh):
        """
        For each point from ``mesh`` find a closest point belonging to surface.

        :param mesh:
            :class:`~openquake.hazardlib.geo.mesh.Mesh` of points to find
            closest points to.
        :returns:
            :class:`~openquake.hazardlib.geo.mesh.Mesh` of the same shape as
            ``mesh`` with closest surface's points on respective indices.
        """
        raise NotImplementedError

    def get_joyner_boore_distance(self, mesh):
        """
        Compute and return Joyner-Boore (also known as ``Rjb``) distance
        to each point of ``mesh``.

        :param mesh:
            :class:`~openquake.hazardlib.geo.mesh.Mesh` of points to calculate
            Joyner-Boore distance to.
        :returns:
            Numpy array of closest distances between the projections of surface
            and each point of the ``mesh`` to the earth surface.
        """
        return self.mesh.get_joyner_boore_distance(mesh)

    def get_rx_distance(self, mesh):
        """
        Compute distance between each point of mesh and surface's great circle
        arc.

        Distance is measured perpendicular to the rupture strike, from
        the surface projection of the updip edge of the rupture, with
        the down dip direction being positive (this distance is usually
        called ``Rx``).

        In other words, is the horizontal distance to top edge of rupture
        measured perpendicular to the strike. Values on the hanging wall
        are positive, values on the footwall are negative.

        :param mesh:
            :class:`~openquake.hazardlib.geo.mesh.Mesh` of points to calculate
            Rx-distance to.
        :returns:
            Numpy array of distances in km.
        """
        raise NotImplementedError

    def get_top_edge_depth(self):
        """
        Compute minimum depth of surface's top edge.

        :returns:
            Float value, the vertical distance between the earth surface
            and the shallowest point in surface's top edge in km.
        """
        raise NotImplementedError

    def get_strike(self):
        """
        Compute surface's strike as decimal degrees in a range ``[0, 360)``.

        The actual definition of the strike might depend on surface geometry.

        :returns:
            Float value, the azimuth (in degrees) of the surface top edge
        """
        raise NotImplementedError

    def get_dip(self):
        """
        Compute surface's dip as decimal degrees in a range ``(0, 90]``.

        The actual definition of the dip might depend on surface geometry.

        :returns:
            Float value, the inclination (in degrees) of the surface with
            respect to the Earth surface
        """
        raise NotImplementedError

    def get_width(self):
        """
        Compute surface's width (that is surface extension along the
        dip direction) in km.

        The actual definition depends on the type of surface geometry.

        :returns:
            Float value, the surface width
        """
        raise NotImplementedError

    def get_area(self):
        """
        Compute surface's area in squared km.

        :returns:
            Float value, the surface area
        """
        raise NotImplementedError

    def get_middle_point(self):
        """
        Compute coordinates of surface middle point.

        The actual definition of ``middle point`` depends on the type of
        surface geometry.

        :return:
            instance of :class:`openquake.hazardlib.geo.point.Point`
            representing surface middle point.
        """
        lon_bar = np.mean(self.mesh.lons)
        lat_bar = np.mean(self.mesh.lats)
        idx = np.argmin((self.mesh.lons - lon_bar)**2 +
                        (self.mesh.lats - lat_bar)**2)
        return Point(self.mesh.lons[idx], self.mesh.lats[idx],
                     self.mesh.depths[idx])

    def get_ry0_distance(self, mesh):
        """
        :param mesh:
            :class:`~openquake.hazardlib.geo.mesh.Mesh` of points
        """
        raise NotImplementedError
