from django.test import TestCase
from django.conf import settings
from django.utils import simplejson
from django.contrib.gis.geos import Point, LineString

from caminae.common.utils import dbnow, almostequal
from caminae.core.factories import (PathFactory, PathAggregationFactory, 
                                    TopologyFactory)
from caminae.core.models import Path, Topology, PathAggregation


class TopologyTest(TestCase):
    def test_dates(self):
        t1 = dbnow()
        e = TopologyFactory.build(no_path=True)
        e.save()
        t2 = dbnow()
        self.assertTrue(t1 < e.date_insert < t2)

        e.delete()
        t3 = dbnow()
        self.assertTrue(t2 < e.date_update < t3)

    def test_length(self):
        e = TopologyFactory.build(no_path=True)
        self.assertEqual(e.length, 0)
        e.save()
        self.assertEqual(e.length, 0)
        PathAggregationFactory.create(topo_object=e)
        e.save()
        self.assertNotEqual(e.length, 0)

    def test_kind(self):
        from caminae.land.models import LandEdge
        from caminae.land.factories import LandEdgeFactory

        # Test with a concrete inheritance of Topology : LandEdge
        self.assertEqual('TOPOLOGY', Topology.KIND)
        self.assertEqual(0, len(Topology.objects.filter(kind='LANDEDGE')))
        self.assertEqual('LANDEDGE', LandEdge.KIND)
        # Kind of instances
        e = LandEdgeFactory.create()
        self.assertEqual(e.kind, LandEdge.KIND)
        self.assertEqual(1, len(Topology.objects.filter(kind='LANDEDGE')))

    def test_delete(self):
        topology = TopologyFactory.create(offset=1)
        path = topology.paths.get()
        self.assertEqual(len(PathAggregation.objects.filter(topo_object=topology)), 1)
        self.assertEqual(len(path.topology_set.all()), 1)
        topology.delete()
        # Make sure object remains in database with deleted status
        self.assertEqual(len(PathAggregation.objects.filter(topo_object=topology)), 1)
        # Make sure object has deleted status
        self.assertTrue(topology.deleted)
        # Make sure object still exists
        self.assertEqual(len(path.topology_set.all()), 1)
        self.assertIn(topology, Topology.objects.all())
        # Make sure object can be hidden from managers
        self.assertNotIn(topology, Topology.objects.existing())
        self.assertEqual(len(path.topology_set.existing()), 0)

    def test_mutate(self):
        topology1 = TopologyFactory.create(no_path=True)
        self.assertEqual(len(topology1.paths.all()), 0)
        topology2 = TopologyFactory.create(offset=14.5)
        self.assertEqual(len(topology2.paths.all()), 1)
        # Normal usecase
        topology1.mutate(topology2)
        self.assertEqual(topology1.offset, 14.5)
        self.assertEqual(len(topology1.paths.all()), 1)
        # topology2 does not exist anymore
        self.assertEqual(len(Topology.objects.filter(pk=topology2.pk)), 0)
        # Without deletion
        topology3 = TopologyFactory.create()
        topology1.mutate(topology3, delete=False)
        # topology3 still exists
        self.assertEqual(len(Topology.objects.filter(pk=topology3.pk)), 1)

    def test_mutate_intersection(self):
        # Mutate a Point topology at an intersection, and make sure its aggregations
        # are not duplicated (c.f. SQL triggers)
        
        # Create a 3 paths intersection
        p1 = PathFactory.create(geom=LineString((0,0,0), (1,0,0)))
        p2 = PathFactory.create(geom=LineString((1,0,0), (2,0,0)))
        p3 = PathFactory.create(geom=LineString((1,0,0), (1,1,0)))
        # Create a topology point at this intersection
        topology = TopologyFactory.create(no_path=True)
        topology.add_path(p2, start=0.0, end=0.0)
        self.assertTrue(topology.ispoint())
        # Make sure, the trigger worked, and linked to 3 paths
        self.assertEqual(len(topology.paths.all()), 3)
        # Mutate it to another one !
        topology2 = TopologyFactory.create(no_path=True)
        self.assertEqual(len(topology2.paths.all()), 0)
        self.assertTrue(topology2.ispoint())
        topology2.mutate(topology)

        for a in topology2.aggregations.all():
            print a
        self.assertEqual(len(topology2.paths.all()), 3)

    def test_serialize(self):
        # At least two path are required
        t = TopologyFactory.create(offset=1)
        self.assertEqual(len(t.paths.all()), 1)

        # This path as been created automatically
        # as we will check only basic json serialization property
        path = t.paths.all()[0]

        # Reload as the geom of the topology will be build by trigger
        t.reload()

        test_objdict = dict(kind=t.kind,
                           offset=1,
                           # 0 referencing the index in paths of the only created path
                           positions={'0':[0.0, 1.0]},
                           paths=[ path.pk ]
                       )

        objdict = simplejson.loads(t.serialize())
        self.assertDictEqual(objdict[0], test_objdict)

    def test_serialize_point(self):
        path = PathFactory.create()
        topology = TopologyFactory.create(offset=1, no_path=True)
        topology.add_path(path, start=0.5, end=0.5)
        fieldvalue = topology.serialize()
        # fieldvalue is like '{"lat": -5.983842291017086, "lng": -1.3630770374505987, "kind": "TOPOLOGYMIXIN"}'
        field = simplejson.loads(fieldvalue)
        self.assertTrue(almostequal(field['lat'],  -5.983))
        self.assertTrue(almostequal(field['lng'],  -1.363))
        self.assertEqual(field['kind'],  "TOPOLOGY")

    def test_deserialize(self):
        path = PathFactory.create()
        topology = Topology.deserialize('[{"paths": [%s], "positions": {"0": [0.0, 1.0]}, "offset": 1}]' % (path.pk))
        self.assertEqual(topology.offset, 1)
        self.assertEqual(topology.kind, Topology.KIND)
        self.assertEqual(len(topology.paths.all()), 1)
        self.assertEqual(topology.aggregations.all()[0].path, path)
        self.assertEqual(topology.aggregations.all()[0].start_position, 0.0)
        self.assertEqual(topology.aggregations.all()[0].end_position, 1.0)
        
        # Multiple paths
        p1 = PathFactory.create(geom=LineString((0,0,0), (2,2,2)))
        p2 = PathFactory.create(geom=LineString((2,2,2), (2,0,0)))
        p3 = PathFactory.create(geom=LineString((2,0,0), (4,0,0)))
        pks = [p.pk for p in [p1,p2,p3]]
        topology = Topology.deserialize('{"paths": %s, "positions": {"0": [0.0, 1.0], "2": [0.0, 1.0]}, "offset": 1}' % (pks))
        for i in range(3):
            self.assertEqual(topology.aggregations.all()[i].start_position, 0.0)
            self.assertEqual(topology.aggregations.all()[i].end_position, 1.0)

        topology = Topology.deserialize('{"paths": %s, "positions": {"0": [0.3, 1.0], "2": [0.0, 0.7]}, "offset": 1}' % (pks))
        self.assertEqual(topology.aggregations.all()[0].start_position, 0.3)
        self.assertEqual(topology.aggregations.all()[0].end_position, 1.0)
        self.assertEqual(topology.aggregations.all()[1].start_position, 0.0)
        self.assertEqual(topology.aggregations.all()[1].end_position, 1.0)
        self.assertEqual(topology.aggregations.all()[2].start_position, 0.0)
        self.assertEqual(topology.aggregations.all()[2].end_position, 0.7)

    def test_deserialize_point(self):
        PathFactory.create()
        # Take a point
        p = Point(2, 1, 0, srid=settings.SRID)
        p.transform(settings.API_SRID)
        closest = Path.closest(p)
        # Check closest path
        self.assertEqual(closest.geom.coords, ((1.0, 1.0, 0.0), (2.0, 2.0, 0.0)))
        # The point has same x as first point of path, and y to 0 :
        topology = Topology.deserialize('{"lng": %s, "lat": %s}' % (p.x, p.y))
        self.assertAlmostEqual(topology.offset, -0.7071, 3)
        self.assertEqual(len(topology.paths.all()), 1)
        pagg = topology.aggregations.get()
        self.assertTrue(almostequal(pagg.start_position, 0.5))
        self.assertTrue(almostequal(pagg.end_position, 0.5))

    def test_deserialize_serialize(self):
        path = PathFactory.create(geom=LineString((1,1,1), (2,2,2), (2,0,0)))
        before = TopologyFactory.create(offset=1, no_path=True)
        before.add_path(path, start=0.5, end=0.5)
        # Reload from DB
        before = Topology.objects.get(pk=before.pk)
        
        # Deserialize its serialized version !
        after = Topology.deserialize(before.serialize())
        # Reload from DB
        after = Topology.objects.get(pk=after.pk)
        

        self.assertEqual(len(before.paths.all()), len(after.paths.all()))
        self.assertTrue(almostequal(before.aggregations.all()[0].start_position,
                                    after.aggregations.all()[0].start_position))
        self.assertTrue(almostequal(before.aggregations.all()[0].end_position,
                                    after.aggregations.all()[0].end_position))

    def test_point_geom_3d(self):
        """
           + 
          / \ 
         / X \
        +     + 
        """
        p1 = PathFactory.create(geom=LineString((0,0,1000), (4,4,2000)))
        p2 = PathFactory.create(geom=LineString((4,4,2000), (8,0,0)))
        
        poi = Point(3, 1, srid=settings.SRID)
        position, distance = Path.interpolate(p1, poi)
        self.assertTrue(almostequal(0.5, position))
        self.assertTrue(almostequal(-1.414, distance))
        # Verify that deserializing this, we obtain the same original coordinates
        # (use lat/lng as in forms)
        poi.transform(settings.API_SRID)
        poitopo = Topology.deserialize({'lat': poi.y, 'lng': poi.x})
        # Computed topology properties match original interpolation
        self.assertTrue(almostequal(0.5, poitopo.aggregations.all()[0].start_position))
        self.assertTrue(almostequal(-1.414, poitopo.offset))
        # Resulting geometry
        self.assertTrue(almostequal(3, poitopo.geom.x))
        self.assertTrue(almostequal(1, poitopo.geom.y))
        self.assertTrue(almostequal(0, poitopo.geom.z))

    def test_point_geom_not_moving(self):
        """
        Modify path, point not moving
        +                  +
        |                  |
         \     X          /        X
         /                \
        |                  |
        +                  +
        """
        p1 = PathFactory.create(geom=LineString((0,0,0),
                                                (0,5,0),
                                                (5,10,0),
                                                (0,15,0),
                                                (0,20,0)))
        poi = Point(10, 10, srid=settings.SRID)
        poi.transform(settings.API_SRID)
        poitopo = Topology.deserialize({'lat': poi.y, 'lng': poi.x})
        self.assertEqual(0.5, poitopo.aggregations.all()[0].start_position)
        self.assertTrue(almostequal(-5, poitopo.offset))
        # It should have kept its position !
        self.assertTrue(almostequal(10, poitopo.geom.x))
        self.assertTrue(almostequal(10, poitopo.geom.y))
        # Change path, it should still be in the same position
        p1.geom = LineString((0,0,0),
                             (0,5,0),
                             (-5,10,0),
                             (0,15,0),
                             (0,20,0))
        p1.save()
        poitopo.reload()
        self.assertTrue(almostequal(10, poitopo.geom.x))
        self.assertTrue(almostequal(10, poitopo.geom.y))

    def test_point_geom_moving(self):
        p1 = PathFactory.create(geom=LineString((0,0,0),
                                                (0,5,0)))
        poi = Point(0, 2.5, srid=settings.SRID)
        poi.transform(settings.API_SRID)
        poitopo = Topology.deserialize({'lat': poi.y, 'lng': poi.x})
        self.assertTrue(almostequal(0.5, poitopo.aggregations.all()[0].start_position))
        self.assertTrue(almostequal(0, poitopo.offset))
        self.assertTrue(almostequal(0, poitopo.geom.x))
        self.assertTrue(almostequal(2.5, poitopo.geom.y))
        p1.geom = LineString((10,0,0),
                             (10,5,0))
        p1.save()
        poitopo.reload()
        self.assertTrue(almostequal(10, poitopo.geom.x))
        self.assertTrue(almostequal(2.5, poitopo.geom.y))


    def test_junction_point(self):
        p1 = PathFactory.create(geom=LineString((0,0,0), (2,2,2)))
        p2 = PathFactory.create(geom=LineString((0,0,0), (2,0,0)))
        p3 = PathFactory.create(geom=LineString((0,2,2), (0,0,0)))

        # Create a junction point topology
        t = TopologyFactory.create(no_path=True)
        self.assertEqual(len(t.paths.all()), 0)

        pa = PathAggregationFactory.create(topo_object=t, path=p1,
                                      start_position=0.0, end_position=0.0)

        self.assertItemsEqual(t.paths.all(), [p1, p2, p3])

        # Update to a non junction point topology
        pa.end_position = 0.4
        pa.save()

        self.assertItemsEqual(t.paths.all(), [p1])

        # Update to a junction point topology
        pa.end_position = 0.0
        pa.save()

        self.assertItemsEqual(t.paths.all(), [p1, p2, p3])

    def test_topology_geom(self):
        p1 = PathFactory.create(geom=LineString((0,0,0), (2,2,2)))
        p2 = PathFactory.create(geom=LineString((2,2,2), (2,0,0)))
        p3 = PathFactory.create(geom=LineString((2,0,0), (4,0,0)))

        # Type Point
        t = TopologyFactory.create(no_path=True)
        PathAggregationFactory.create(topo_object=t, path=p1,
                                      start_position=0.5, end_position=0.5)
        t = Topology.objects.get(pk=t.pk)
        self.assertEqual(t.geom, Point((1,1,1)))

        # 50% of path p1, 100% of path p2
        t = TopologyFactory.create(no_path=True)
        PathAggregationFactory.create(topo_object=t, path=p1,
                                      start_position=0.5)
        PathAggregationFactory.create(topo_object=t, path=p2)
        t = Topology.objects.get(pk=t.pk)
        self.assertEqual(t.geom, LineString((1,1,1), (2,2,2), (2,0,0)))

        # 100% of path p2 and p3, with offset of 1
        t = TopologyFactory.create(no_path=True, offset=1)
        PathAggregationFactory.create(topo_object=t, path=p2)
        PathAggregationFactory.create(topo_object=t, path=p3)
        t.save()
        self.assertEqual(t.geom, LineString((3,2,2), (3,1,0), (4,1,0)))

        # Change offset, geometry is computed again
        t.offset = 0.5
        t.save()
        self.assertEqual(t.geom, LineString((2.5,2,2), (2.5,0.5,0), (4,0.5,0)))

    def test_topology_geom_with_intermediate_markers(self):
        # Intermediate (forced passage) markers for topologies
        # Use a bifurcation, make sure computed geometry is correct
        #       +--p2---+
        #   +---+-------+---+
        #     p1   p3     p4
        p1 = PathFactory.create(geom=LineString((0,0,0), (2,0,0)))
        p2 = PathFactory.create(geom=LineString((2,0,0), (2,1,0), (4,1,0), (4,0,0)))
        p3 = PathFactory.create(geom=LineString((2,0,0), (4,0,0)))
        p4 = PathFactory.create(geom=LineString((4,0,0), (6,0,0)))
        """
        From p1 to p4, with point in the middle of p3
        """
        t = TopologyFactory.create(no_path=True)
        PathAggregationFactory.create(topo_object=t, path=p1)
        PathAggregationFactory.create(topo_object=t, path=p3)
        PathAggregationFactory.create(topo_object=t, path=p3, 
                                      start_position=0.5, end_position=0.5)
        PathAggregationFactory.create(topo_object=t, path=p4)
        t.save()
        self.assertEqual(t.geom, LineString((0,0,0), (2,0,0), (4,0,0), (6,0,0)))
        """
        From p1 to p4, through p2
        """
        t = TopologyFactory.create(no_path=True)
        PathAggregationFactory.create(topo_object=t, path=p1)
        PathAggregationFactory.create(topo_object=t, path=p2)
        # There will a forced passage in database...
        PathAggregationFactory.create(topo_object=t, path=p2, 
                                      start_position=0.5, end_position=0.5)
        PathAggregationFactory.create(topo_object=t, path=p4)
        t.save()
        self.assertEqual(t.geom, LineString((0,0,0), (2,0,0), (2,1,0), (4,1,0), (4,0,0), (6,0,0)))

        """
        From p1 to p4, though p2, but **with start/end at 0.0**
        """
        t2 = TopologyFactory.create(no_path=True)
        PathAggregationFactory.create(topo_object=t2, path=p1)
        PathAggregationFactory.create(topo_object=t2, path=p2)
        PathAggregationFactory.create(topo_object=t2, path=p2, 
                                      start_position=0.0, end_position=0.0)
        PathAggregationFactory.create(topo_object=t2, path=p4)
        t2.save()
        self.assertEqual(t2.geom, t.geom)

    def test_troncon_geom_update(self):
        # Create a path
        p = PathFactory.create(geom=LineString((0,0,0),(4,0,0)))

        # Create a linear topology
        t1 = TopologyFactory.create(offset=1, no_path=True)
        t1.add_path(p, start=0.0, end=0.5)
        t1_agg = t1.aggregations.get()

        # Create a point topology
        t2 = TopologyFactory.create(offset=-1, no_path=True)
        t2.add_path(p, start=0.5, end=0.5)
        t2_agg = t2.aggregations.get()

        # Ensure linear topology is correct before path modification
        self.assertEqual(t1.offset, 1)
        self.assertEqual(t1.geom.coords, ((0,1,0),(2,1,0)))
        self.assertEqual(t1_agg.start_position, 0.0)
        self.assertEqual(t1_agg.end_position, 0.5)

        # Ensure point topology is correct before path modification
        self.assertEqual(t2.offset, -1)
        self.assertEqual(t2.geom.coords, (2,-1,0))
        self.assertEqual(t2_agg.start_position, 0.5)
        self.assertEqual(t2_agg.end_position, 0.5)

        # Modify path geometry and refresh computed data
        p.geom = LineString((0,2,0),(8,2,0))
        p.save()
        t1.reload()
        t1_agg = t1.aggregations.get()
        t2.reload()
        t2_agg = t2.aggregations.get()

        # Ensure linear topology is correct after path modification
        self.assertEqual(t1.offset, 1)
        self.assertEqual(t1.geom.coords, ((0,3,0),(4,3,0)))
        self.assertEqual(t1_agg.start_position, 0.0)
        self.assertEqual(t1_agg.end_position, 0.5)

        # Ensure point topology is correct before path modification
        self.assertEqual(t2.offset, -3)
        self.assertEqual(t2.geom.coords, (2,-1,0))
        self.assertEqual(t2_agg.start_position, 0.25)
        self.assertEqual(t2_agg.end_position, 0.25)



class TopologyCornerCases(TestCase):
    def test_opposite_paths(self):
        """
                A  C
        B +-------+-------+ D

        """
        ab = PathFactory.create(geom=LineString((5,0,0), (0,0,0)))
        cd = PathFactory.create(geom=LineString((5,0,0), (10,0,0)))
        topo = TopologyFactory.create(no_path=True)
        topo.add_path(ab, start=0.2, end=0)
        topo.add_path(cd, start=0, end=0.2)
        topo.save()
        expected = LineString((4,0,0),(5,0,0),(6,0,0))
        self.assertEqual(topo.geom, expected)
        # Now let's have some fun, reverse BA :)
        ab.reverse()
        ab.save()
        topo.reload()
        self.assertEqual(topo.geom, expected)


    def test_opposite_paths_with_middle(self):
        """
                A            C
        B +-------+--------+-------+ D

        """
        ab = PathFactory.create(geom=LineString((5,0,0), (0,0,0)))
        ac = PathFactory.create(geom=LineString((5,0,0), (10,0,0)))
        cd = PathFactory.create(geom=LineString((10,0,0), (15,0,0)))
        topo = TopologyFactory.create(no_path=True)
        topo.add_path(ab, start=0.2, end=0)
        topo.add_path(ac)
        topo.add_path(cd, start=0, end=0.2)
        topo.save()
        expected = LineString((4,0,0),(5,0,0),(10,0,0),(11,0,0))
        self.assertEqual(topo.geom, expected)
        # Reverse AC ! OMG this is hell !
        ac.reverse()
        ac.save()
        topo.reload()
        self.assertEqual(topo.geom, expected)

    def test_return_path(self):
        """
                     A
                 ----+
                 |
        B +------+------+ C
        """
        p1 = PathFactory.create(geom=LineString((0,0,0), (10,0,0)))
        p2 = PathFactory.create(geom=LineString((5,0,0), (5,10,0), (10,10,0)))
        p3 = Path.objects.filter(name=p1.name).exclude(pk=p1.pk)[0]  # Was splitted :)
        # Now create a topology B-A-C
        topo = TopologyFactory.create(no_path=True)
        topo.add_path(p1, start=0.5, end=1)
        topo.add_path(p2, start=0, end=0.8)
        topo.add_path(p2, start=0.8, end=0.8)
        topo.add_path(p2, start=0.8, end=0)
        topo.add_path(p3, start=0, end=0.5)
        topo.save()
        self.assertEqual(topo.geom, LineString((2.5,0,0),(5,0,0),(5,10,0),
                                               (7,10,0),(5,10,0),(5,0,0),
                                               (7.5,0,0)))

    def test_return_path_serialized(self):
        """
        Same as test_return_path() but from deserialization.
        """
        p1 = PathFactory.create(geom=LineString((0,0,0), (10,0,0)))
        p2 = PathFactory.create(geom=LineString((5,0,0), (5,10,0), (10,10,0)))
        p3 = Path.objects.filter(name=p1.name).exclude(pk=p1.pk)[0]  # Was splitted :)
        topo = Topology.deserialize("""
           [{"offset":0,
             "positions":{"0":[0.5,1],
                          "1":[0.0, 0.8]},
             "paths":[%(p1)s,%(p2)s]
            },
            {"offset":0,
             "positions":{"0":[0.8,0.0],
                          "1":[0.0, 0.5]},
             "paths":[%(p2)s,%(p3)s]
            }
           ]
        """ % {'p1': p1.pk, 'p2': p2.pk, 'p3': p3.pk})
        topo.save()
        self.assertEqual(topo.geom, LineString((2.5,0,0),(5,0,0),(5,10,0),
                                               (7,10,0),(5,10,0),(5,0,0),
                                               (7.5,0,0)))

    def test_simple_loop(self):
        """
           ==========
          ||        ||
        A +==------==+ B
        """
        p1 = PathFactory.create(geom=LineString((10,0,0), (0,0,0)))
        p2 = PathFactory.create(geom=LineString((0,0,0), (0,5,0),(10,5,0), (10,0,0)))
        # Full loop
        topo = TopologyFactory.create(no_path=True)
        topo.add_path(p1)
        topo.add_path(p2)
        topo.save()
        self.assertEqual(topo.geom, LineString((10,0,0),(0,0,0),(0,5,0),(10,5,0),(10,0,0)))
        # Subpart, like in diagram
        topo = TopologyFactory.create(no_path=True)
        topo.add_path(p1, start=0.8, end=1)
        topo.add_path(p2)
        topo.add_path(p1, start=0, end=0.2)
        topo.save()
        self.assertEqual(topo.geom, LineString((2,0,0),(0,0,0),(0,5,0),
                                               (10,5,0),(10,0,0),(8,0,0)))


    def test_trek_loop(self):
        """
                            =========
                           ||       ||
        +-------===========+=========+----------+
        """
        p1 = PathFactory.create(geom=LineString((0,0,0), (10,0,0)))
        p2 = PathFactory.create(geom=LineString((10,0,0), (30,0,0)))
        p3 = PathFactory.create(geom=LineString((10,0,0), (10,5,0),
                                                (20,5,0), (20,0,0)))
        topo = TopologyFactory.create(no_path=True)
        topo.add_path(p1, start=0.3, end=1)
        topo.add_path(p3)
        topo.add_path(p2, start=1, end=0)
        topo.add_path(p1, start=1, end=0.3)
        topo.save()
        self.assertEqual(topo.geom, LineString((3,0,0),(10,0,0),(10,5,0),(20,5,0),(20,0,0),
                                               (10,0,0),(3,0,0)))