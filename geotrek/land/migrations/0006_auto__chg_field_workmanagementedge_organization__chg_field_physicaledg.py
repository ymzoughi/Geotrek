# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'WorkManagementEdge.organization' to match new field type.
        db.rename_column('f_t_gestion_travaux', 'organization_id', 'organisme')
        # Changing field 'WorkManagementEdge.organization'
        db.alter_column('f_t_gestion_travaux', 'organisme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organism'], db_column='organisme'))

        # Renaming column for 'PhysicalEdge.physical_type' to match new field type.
        db.rename_column('f_t_nature', 'physical_type_id', 'type')
        # Changing field 'PhysicalEdge.physical_type'
        db.alter_column('f_t_nature', 'type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['land.PhysicalType'], db_column='type'))

        # Renaming column for 'RestrictedAreaEdge.restricted_area' to match new field type.
        db.rename_column('f_t_zonage', 'restricted_area_id', 'zone')
        # Changing field 'RestrictedAreaEdge.restricted_area'
        db.alter_column('f_t_zonage', 'zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['land.RestrictedArea'], db_column='zone'))

        # Renaming column for 'CityEdge.city' to match new field type.
        db.rename_column('f_t_commune', 'city_id', 'commune')
        # Changing field 'CityEdge.city'
        db.alter_column('f_t_commune', 'commune', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['land.City'], db_column='commune'))

        # Renaming column for 'RestrictedAreaType.name' to match new field type.
        db.rename_column('f_b_zonage', 'name', 'nom')
        # Changing field 'RestrictedAreaType.name'
        db.alter_column('f_b_zonage', 'nom', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='nom'))

        # Renaming column for 'DistrictEdge.district' to match new field type.
        db.rename_column('f_t_secteur', 'district_id', 'secteur')
        # Changing field 'DistrictEdge.district'
        db.alter_column('f_t_secteur', 'secteur', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['land.District'], db_column='secteur'))

        # Renaming column for 'SignageManagementEdge.organization' to match new field type.
        db.rename_column('f_t_gestion_signaletique', 'organization_id', 'organisme')
        # Changing field 'SignageManagementEdge.organization'
        db.alter_column('f_t_gestion_signaletique', 'organisme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organism'], db_column='organisme'))

        # Renaming column for 'CompetenceEdge.organization' to match new field type.
        db.rename_column('f_t_competence', 'organization_id', 'organisme')
        # Changing field 'CompetenceEdge.organization'
        db.alter_column('f_t_competence', 'organisme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organism'], db_column='organisme'))

        # Renaming column for 'LandEdge.land_type' to match new field type.
        db.rename_column('f_t_foncier', 'land_type_id', 'type')
        # Changing field 'LandEdge.land_type'
        db.alter_column('f_t_foncier', 'type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['land.LandType'], db_column='type'))

        # Renaming column for 'PhysicalType.name_en' to match new field type.
        db.rename_column('f_b_nature', 'name_en', 'nom_en')
        # Changing field 'PhysicalType.name_en'
        db.alter_column('f_b_nature', 'nom_en', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, db_column='nom'))

        # Renaming column for 'PhysicalType.name_fr' to match new field type.
        db.rename_column('f_b_nature', 'name_fr', 'nom_fr')
        # Changing field 'PhysicalType.name_fr'
        db.alter_column('f_b_nature', 'nom_fr', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, db_column='nom'))

        # Renaming column for 'PhysicalType.name_it' to match new field type.
        db.rename_column('f_b_nature', 'name_it', 'nom_it')
        # Changing field 'PhysicalType.name_it'
        db.alter_column('f_b_nature', 'nom_it', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, db_column='nom'))

        # Renaming column for 'PhysicalType.name' to match new field type.
        db.rename_column('f_b_nature', 'name', 'nom')
        # Changing field 'PhysicalType.name'
        db.alter_column('f_b_nature', 'nom', self.gf('django.db.models.fields.CharField')(max_length=128, db_column='nom'))

    def backwards(self, orm):

        # Renaming column for 'WorkManagementEdge.organization' to match new field type.
        db.rename_column('f_t_gestion_travaux', 'organisme', 'organization_id')
        # Changing field 'WorkManagementEdge.organization'
        db.alter_column('f_t_gestion_travaux', 'organization_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organism']))

        # Renaming column for 'PhysicalEdge.physical_type' to match new field type.
        db.rename_column('f_t_nature', 'type', 'physical_type_id')
        # Changing field 'PhysicalEdge.physical_type'
        db.alter_column('f_t_nature', 'physical_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['land.PhysicalType']))

        # Renaming column for 'RestrictedAreaEdge.restricted_area' to match new field type.
        db.rename_column('f_t_zonage', 'zone', 'restricted_area_id')
        # Changing field 'RestrictedAreaEdge.restricted_area'
        db.alter_column('f_t_zonage', 'restricted_area_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['land.RestrictedArea']))

        # Renaming column for 'CityEdge.city' to match new field type.
        db.rename_column('f_t_commune', 'commune', 'city_id')
        # Changing field 'CityEdge.city'
        db.alter_column('f_t_commune', 'city_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['land.City']))

        # Renaming column for 'RestrictedAreaType.name' to match new field type.
        db.rename_column('f_b_zonage', 'nom', 'name')
        # Changing field 'RestrictedAreaType.name'
        db.alter_column('f_b_zonage', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Renaming column for 'DistrictEdge.district' to match new field type.
        db.rename_column('f_t_secteur', 'secteur', 'district_id')
        # Changing field 'DistrictEdge.district'
        db.alter_column('f_t_secteur', 'district_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['land.District']))

        # Renaming column for 'SignageManagementEdge.organization' to match new field type.
        db.rename_column('f_t_gestion_signaletique', 'organisme', 'organization_id')
        # Changing field 'SignageManagementEdge.organization'
        db.alter_column('f_t_gestion_signaletique', 'organization_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organism']))

        # Renaming column for 'CompetenceEdge.organization' to match new field type.
        db.rename_column('f_t_competence', 'organisme', 'organization_id')
        # Changing field 'CompetenceEdge.organization'
        db.alter_column('f_t_competence', 'organization_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organism']))

        # Renaming column for 'LandEdge.land_type' to match new field type.
        db.rename_column('f_t_foncier', 'type', 'land_type_id')
        # Changing field 'LandEdge.land_type'
        db.alter_column('f_t_foncier', 'land_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['land.LandType']))

        # Renaming column for 'PhysicalType.name_en' to match new field type.
        db.rename_column('f_b_nature', 'nom_en', 'name_en')
        # Changing field 'PhysicalType.name_en'
        db.alter_column('f_b_nature', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=128, null=True))

        # Renaming column for 'PhysicalType.name_fr' to match new field type.
        db.rename_column('f_b_nature', 'nom_fr', 'name_fr')
        # Changing field 'PhysicalType.name_fr'
        db.alter_column('f_b_nature', 'name_fr', self.gf('django.db.models.fields.CharField')(max_length=128, null=True))

        # Renaming column for 'PhysicalType.name_it' to match new field type.
        db.rename_column('f_b_nature', 'nom_it', 'name_it')
        # Changing field 'PhysicalType.name_it'
        db.alter_column('f_b_nature', 'name_it', self.gf('django.db.models.fields.CharField')(max_length=128, null=True))

        # Renaming column for 'PhysicalType.name' to match new field type.
        db.rename_column('f_b_nature', 'nom', 'name')
        # Changing field 'PhysicalType.name'
        db.alter_column('f_b_nature', 'name', self.gf('django.db.models.fields.CharField')(max_length=128))

    models = {
        'authent.structure': {
            'Meta': {'object_name': 'Structure'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'common.organism': {
            'Meta': {'object_name': 'Organism', 'db_table': "'m_b_organisme'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organism': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'organisme'"})
        },
        'core.comfort': {
            'Meta': {'object_name': 'Comfort', 'db_table': "'l_b_confort'"},
            'comfort': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'confort'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']", 'db_column': "'structure'"})
        },
        'core.datasource': {
            'Meta': {'object_name': 'Datasource', 'db_table': "'l_b_source'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']", 'db_column': "'structure'"})
        },
        'core.network': {
            'Meta': {'object_name': 'Network', 'db_table': "'l_b_reseau'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'reseau'"}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']", 'db_column': "'structure'"})
        },
        'core.path': {
            'Meta': {'object_name': 'Path', 'db_table': "'l_t_troncon'"},
            'arrival': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_column': "'arrivee'", 'blank': 'True'}),
            'ascent': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'denivelee_positive'"}),
            'comfort': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paths'", 'null': 'True', 'db_column': "'confort'", 'to': "orm['core.Comfort']"}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'remarques'", 'blank': 'True'}),
            'datasource': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paths'", 'null': 'True', 'db_column': "'source'", 'to': "orm['core.Datasource']"}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'db_column': "'date_insert'"}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'db_column': "'date_update'"}),
            'departure': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_column': "'depart'", 'blank': 'True'}),
            'descent': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'denivelee_negative'"}),
            'geom': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '%s' % settings.SRID, 'dim': '3', 'spatial_index': 'False'}),
            'geom_cadastre': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '%s' % settings.SRID, 'dim': '3', 'null': 'True', 'spatial_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_column': "'longueur'"}),
            'max_elevation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'altitude_maximum'"}),
            'min_elevation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'altitude_minimum'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'nom'", 'blank': 'True'}),
            'networks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'paths'", 'to': "orm['core.Network']", 'db_table': "'l_r_troncon_reseau'", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'stake': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paths'", 'null': 'True', 'db_column': "'enjeu'", 'to': "orm['core.Stake']"}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']", 'db_column': "'structure'"}),
            'trail': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paths'", 'null': 'True', 'db_column': "'sentier'", 'to': "orm['core.Trail']"}),
            'usages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'paths'", 'to': "orm['core.Usage']", 'db_table': "'l_r_troncon_usage'", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'valide'"})
        },
        'core.pathaggregation': {
            'Meta': {'ordering': "['id']", 'object_name': 'PathAggregation', 'db_table': "'e_r_evenement_troncon'"},
            'end_position': ('django.db.models.fields.FloatField', [], {'db_column': "'pk_fin'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aggregations'", 'on_delete': 'models.DO_NOTHING', 'db_column': "'troncon'", 'to': "orm['core.Path']"}),
            'start_position': ('django.db.models.fields.FloatField', [], {'db_column': "'pk_debut'"}),
            'topo_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aggregations'", 'db_column': "'evenement'", 'to': "orm['core.Topology']"})
        },
        'core.stake': {
            'Meta': {'object_name': 'Stake', 'db_table': "'l_b_enjeu'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stake': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'enjeu'"}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']", 'db_column': "'structure'"})
        },
        'core.topology': {
            'Meta': {'object_name': 'Topology', 'db_table': "'e_t_evenement'"},
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'db_column': "'date_insert'"}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'db_column': "'date_update'"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'supprime'"}),
            'geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'srid': '%s' % settings.SRID, 'dim': '3', 'null': 'True', 'spatial_index': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_column': "'longueur'"}),
            'offset': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_column': "'decallage'"}),
            'paths': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Path']", 'through': "orm['core.PathAggregation']", 'db_column': "'troncons'", 'symmetrical': 'False'})
        },
        'core.trail': {
            'Meta': {'object_name': 'Trail', 'db_table': "'l_t_sentier'"},
            'arrival': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_column': "'arrivee'"}),
            'comments': ('django.db.models.fields.TextField', [], {'default': "''", 'db_column': "'commentaire'"}),
            'departure': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_column': "'depart'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_column': "'nom'"}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']", 'db_column': "'structure'"})
        },
        'core.usage': {
            'Meta': {'object_name': 'Usage', 'db_table': "'l_b_usage'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']", 'db_column': "'structure'"}),
            'usage': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'usage'"})
        },
        'land.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City', 'db_table': "'l_commune'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True', 'db_column': "'insee'"}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '%s' % settings.SRID, 'spatial_index': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'commune'"})
        },
        'land.cityedge': {
            'Meta': {'object_name': 'CityEdge', 'db_table': "'f_t_commune'", '_ormbases': ['core.Topology']},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['land.City']", 'db_column': "'commune'"}),
            'topo_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Topology']", 'unique': 'True', 'primary_key': 'True', 'db_column': "'evenement'"})
        },
        'land.competenceedge': {
            'Meta': {'object_name': 'CompetenceEdge', 'db_table': "'f_t_competence'", '_ormbases': ['core.Topology']},
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Organism']", 'db_column': "'organisme'"}),
            'topo_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Topology']", 'unique': 'True', 'primary_key': 'True', 'db_column': "'evenement'"})
        },
        'land.district': {
            'Meta': {'ordering': "['name']", 'object_name': 'District', 'db_table': "'l_secteur'"},
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '%s' % settings.SRID, 'spatial_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'secteur'"})
        },
        'land.districtedge': {
            'Meta': {'object_name': 'DistrictEdge', 'db_table': "'f_t_secteur'", '_ormbases': ['core.Topology']},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['land.District']", 'db_column': "'secteur'"}),
            'topo_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Topology']", 'unique': 'True', 'primary_key': 'True', 'db_column': "'evenement'"})
        },
        'land.landedge': {
            'Meta': {'object_name': 'LandEdge', 'db_table': "'f_t_foncier'", '_ormbases': ['core.Topology']},
            'land_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['land.LandType']", 'db_column': "'type'"}),
            'topo_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Topology']", 'unique': 'True', 'primary_key': 'True', 'db_column': "'evenement'"})
        },
        'land.landtype': {
            'Meta': {'object_name': 'LandType', 'db_table': "'f_b_foncier'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'foncier'"}),
            'right_of_way': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'droit_de_passage'"}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']", 'db_column': "'structure'"})
        },
        'land.physicaledge': {
            'Meta': {'object_name': 'PhysicalEdge', 'db_table': "'f_t_nature'", '_ormbases': ['core.Topology']},
            'physical_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['land.PhysicalType']", 'db_column': "'type'"}),
            'topo_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Topology']", 'unique': 'True', 'primary_key': 'True', 'db_column': "'evenement'"})
        },
        'land.physicaltype': {
            'Meta': {'object_name': 'PhysicalType', 'db_table': "'f_b_nature'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'nom'"}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_column': "'nom'", 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_column': "'nom'", 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_column': "'nom'", 'blank': 'True'})
        },
        'land.restrictedarea': {
            'Meta': {'ordering': "['area_type', 'name']", 'object_name': 'RestrictedArea', 'db_table': "'l_zonage_reglementaire'"},
            'area_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['land.RestrictedAreaType']"}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '%s' % settings.SRID, 'spatial_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_column': "'zonage'"})
        },
        'land.restrictedareaedge': {
            'Meta': {'object_name': 'RestrictedAreaEdge', 'db_table': "'f_t_zonage'", '_ormbases': ['core.Topology']},
            'restricted_area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['land.RestrictedArea']", 'db_column': "'zone'"}),
            'topo_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Topology']", 'unique': 'True', 'primary_key': 'True', 'db_column': "'evenement'"})
        },
        'land.restrictedareatype': {
            'Meta': {'object_name': 'RestrictedAreaType', 'db_table': "'f_b_zonage'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'nom'"})
        },
        'land.signagemanagementedge': {
            'Meta': {'object_name': 'SignageManagementEdge', 'db_table': "'f_t_gestion_signaletique'", '_ormbases': ['core.Topology']},
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Organism']", 'db_column': "'organisme'"}),
            'topo_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Topology']", 'unique': 'True', 'primary_key': 'True', 'db_column': "'evenement'"})
        },
        'land.workmanagementedge': {
            'Meta': {'object_name': 'WorkManagementEdge', 'db_table': "'f_t_gestion_travaux'", '_ormbases': ['core.Topology']},
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Organism']", 'db_column': "'organisme'"}),
            'topo_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Topology']", 'unique': 'True', 'primary_key': 'True', 'db_column': "'evenement'"})
        }
    }

    complete_apps = ['land']