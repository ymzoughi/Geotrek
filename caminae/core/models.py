from django.contrib.gis.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from caminae.authent.models import StructureRelated
from caminae.utils import distance3D


# Used to create the matching url name
ENTITY_LAYER = "layer"
ENTITY_LIST = "list"
ENTITY_JSON_LIST = "json_list"
ENTITY_DETAIL = "detail"
ENTITY_CREATE = "add"
ENTITY_UPDATE = "update"
ENTITY_DELETE = "delete"

ENTITY_KINDS = (
    ENTITY_LAYER, ENTITY_LIST, ENTITY_JSON_LIST,
    ENTITY_DETAIL, ENTITY_CREATE,
    ENTITY_UPDATE, ENTITY_DELETE,
)

class MapEntityMixin(object):

    @classmethod
    def latest_updated(cls):
        try:
            return cls.objects.latest("date_update").date_update
        except cls.DoesNotExist:
            return None

    # List all different kind of views
    @classmethod
    def get_url_name(cls, kind):
        if not kind in ENTITY_KINDS:
            return None
        return '%s:%s_%s' % (cls._meta.app_label, cls._meta.module_name, kind)

    @classmethod
    def get_url_name_for_registration(cls, kind):
        if not kind in ENTITY_KINDS:
            return None
        return '%s_%s' % (cls._meta.module_name, kind)

    @classmethod
    @models.permalink
    def get_layer_url(cls):
        return (cls.get_url_name(ENTITY_LAYER), )

    @classmethod
    @models.permalink
    def get_list_url(cls):
        return (cls.get_url_name(ENTITY_LIST), )

    @classmethod
    @models.permalink
    def get_jsonlist_url(cls):
        return (cls.get_url_name(ENTITY_JSON_LIST), )

    @classmethod
    @models.permalink
    def get_add_url(cls):
        return (cls.get_url_name(ENTITY_CREATE), )

    def get_absolute_url(self):
        return self.get_detail_url()

    @classmethod
    @models.permalink
    def get_generic_detail_url(self):
        return (self.get_url_name(ENTITY_DETAIL), [str(0)])

    @models.permalink
    def get_detail_url(self):
        return (self.get_url_name(ENTITY_DETAIL), [str(self.pk)])

    @models.permalink
    def get_update_url(self):
        return (self.get_url_name(ENTITY_UPDATE), [str(self.pk)])

    @models.permalink
    def get_delete_url(self):
        return (self.get_url_name(ENTITY_DELETE), [str(self.pk)])




# GeoDjango note:
# Django automatically creates indexes on geometry fields but it uses a
# syntax which is not compatible with PostGIS 2.0. That's why index creation
# is explicitly disbaled here (see manual index creation in custom SQL files).

class Path(MapEntityMixin, StructureRelated):
    geom = models.LineStringField(srid=settings.SRID, spatial_index=False,
                                  dim=3)
    geom_cadastre = models.LineStringField(null=True, srid=settings.SRID,
                                           spatial_index=False, dim=3)
    valid = models.BooleanField(db_column='troncon_valide', default=True, verbose_name=_(u"Validity"))
    name = models.CharField(null=True, blank=True, max_length=20, db_column='nom_troncon', verbose_name=_(u"Name"))
    comments = models.TextField(null=True, blank=True, db_column='remarques', verbose_name=_(u"Comments"))

    # Override default manager
    objects = models.GeoManager()

    # Computed values (managed at DB-level with triggers)
    date_insert = models.DateTimeField(editable=False, verbose_name=_(u"Insertion date"))
    date_update = models.DateTimeField(editable=False, verbose_name=_(u"Update date"))
    length = models.FloatField(editable=False, default=0, db_column='longueur', verbose_name=_(u"Length"))
    ascent = models.IntegerField(
            editable=False, default=0, db_column='denivelee_positive', verbose_name=_(u"Ascent"))
    descent = models.IntegerField(
            editable=False, default=0, db_column='denivelee_negative', verbose_name=_(u"Descent"))
    min_elevation = models.IntegerField(
            editable=False, default=0, db_column='altitude_minimum', verbose_name=_(u"Minimum elevation"))
    max_elevation = models.IntegerField(
            editable=False, default=0, db_column='altitude_maximum', verbose_name=_(u"Maximum elevation"))


    trail = models.ForeignKey('Trail',
            null=True, blank=True, related_name='paths',
            verbose_name=_("Trail"))
    datasource = models.ForeignKey('Datasource',
            null=True, blank=True, related_name='paths',
            verbose_name=_("Datasource"))
    stake = models.ForeignKey('Stake',
            null=True, blank=True, related_name='paths',
            verbose_name=_("Stake"))
    usages = models.ManyToManyField('Usage',
            blank=True, null=True, related_name="paths",
            verbose_name=_(u"Usages"))
    networks = models.ManyToManyField('Network',
            blank=True, null=True, related_name="paths",
            verbose_name=_(u"Networks"))

    def __unicode__(self):
        return self.name or 'path %d' % self.pk

    class Meta:
        db_table = 'troncons'
        verbose_name = _(u"Path")
        verbose_name_plural = _(u"Paths")

    def save(self, *args, **kwargs):
        super(Path, self).save(*args, **kwargs)

        # Update object's computed values (reload from database)
        tmp = self.__class__.objects.get(pk=self.pk)
        self.date_insert = tmp.date_insert
        self.date_update = tmp.date_update
        self.length = tmp.length
        self.ascent = tmp.ascent
        self.descent = tmp.descent
        self.min_elevation = tmp.min_elevation
        self.max_elevation = tmp.max_elevation
        self.geom = tmp.geom

    def get_elevation_profile(self):
        """
        Extract elevation profile from path.
        """
        coords = self.geom.coords
        profile = [(0.0, coords[0][2])]
        distance = 0
        for i in range(1, len(coords)):
            a = coords[i - 1]
            b = coords[i]
            distance += distance3D(a, b)
            profile.append((distance, b[2],))
        return profile

    @property
    def name_display(self):
        return u'<a data-pk="%s" href="%s" >%s</a>' % (self.pk, self.get_detail_url(), self)

    @property
    def trail_display(self):
        return self.trail.name if self.trail else _("None")


class TopologyMixin(models.Model):
    troncons = models.ManyToManyField(Path, through='PathAggregation', verbose_name=_(u"Path"))
    offset = models.IntegerField(default=0, db_column='decallage', verbose_name=_(u"Offset"))
    deleted = models.BooleanField(default=False, db_column='supprime', verbose_name=_(u"Deleted"))
    kind = models.ForeignKey('TopologyMixinKind', verbose_name=_(u"Kind"))

    # Override default manager
    objects = models.GeoManager()

    # Computed values (managed at DB-level with triggers)
    date_insert = models.DateTimeField(editable=False, verbose_name=_(u"Insertion date"))
    date_update = models.DateTimeField(editable=False, verbose_name=_(u"Update date"))
    length = models.FloatField(editable=False, default=0, db_column='longueur', verbose_name=_(u"Length"))
    geom = models.LineStringField(editable=False, srid=settings.SRID,
                                  spatial_index=False, dim=3)

    def __unicode__(self):
        return u"%s (%s)" % (_(u"Topology"), self.pk)

    class Meta:
        db_table = 'evenements'
        verbose_name = _(u"Topology")
        verbose_name_plural = _(u"Topologies")

    def save(self, *args, **kwargs):
        super(TopologyMixin, self).save(*args, **kwargs)

        # Update computed values
        tmp = self.__class__.objects.get(pk=self.pk)
        self.date_insert = tmp.date_insert
        self.date_update = tmp.date_update
        self.length = tmp.length
        self.geom = tmp.geom


class TopologyMixinKind(models.Model):

    kind = models.CharField(max_length=128, verbose_name=_(u"Topology's kind"))

    def __unicode__(self):
        return self.kind

    class Meta:
        db_table = 'type_evenements'
        verbose_name = _(u"Topology's kind")
        verbose_name_plural = _(u"Topology's kinds")


class PathAggregation(models.Model):
    path = models.ForeignKey(Path, null=False, db_column='troncon', verbose_name=_(u"Path"), related_name="aggregations")
    topo_object = models.ForeignKey(TopologyMixin, null=False, related_name="aggregations",
                                    db_column='evenement', verbose_name=_(u"Topology"))
    start_position = models.FloatField(db_column='pk_debut', verbose_name=_(u"Start position"))
    end_position = models.FloatField(db_column='pk_fin', verbose_name=_(u"End position"))

    # Override default manager
    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s (%s - %s)" % (_("Path aggregation"), self.start_position, self.end_position)

    class Meta:
        db_table = 'evenements_troncons'
        verbose_name = _(u"Path aggregation")
        verbose_name_plural = _(u"Path aggregations")


class Datasource(StructureRelated):

    source = models.CharField(verbose_name=_(u"Source"), max_length=50)

    class Meta:
        db_table = 'source_donnees'
        verbose_name = _(u"Datasource")
        verbose_name_plural = _(u"Datasources")

    def __unicode__(self):
        return self.source


class Stake(StructureRelated):

    stake = models.CharField(verbose_name=_(u"Stake"), max_length=50)

    class Meta:
        db_table = 'enjeu'
        verbose_name = _(u"Stake")
        verbose_name_plural = _(u"Stakes")

    def __unicode__(self):
        return self.stake


class Usage(StructureRelated):

    usage = models.CharField(verbose_name=_(u"Usage"), max_length=50)

    class Meta:
        db_table = 'usage'
        verbose_name = _(u"Usage")
        verbose_name_plural = _(u"Usages")

    def __unicode__(self):
        return self.usage


class Network(StructureRelated):

    network = models.CharField(verbose_name=_(u"Network"), max_length=50)

    class Meta:
        db_table = 'reseau_troncon'
        verbose_name = _(u"Network")
        verbose_name_plural = _(u"Networks")

    def __unicode__(self):
        return self.network


class Trail(StructureRelated):

    name = models.CharField(verbose_name=_(u"Name"), max_length=64)
    departure = models.CharField(verbose_name=_(u"Name"), max_length=64)
    arrival = models.CharField(verbose_name=_(u"Arrival"), max_length=64)
    comments = models.TextField(default="", verbose_name=_(u"Comments"))

    class Meta:
        db_table = 'sentier'
        verbose_name = _(u"Trails")
        verbose_name_plural = _(u"Trails")

    def __unicode__(self):
        return u"%s (%s -> %s)" % (self.name, self.departure, self.arrival)
