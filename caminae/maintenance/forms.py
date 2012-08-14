from django.contrib.gis.geos import Point, LineString

import floppyforms as forms
from crispy_forms.layout import Field

from caminae.mapentity.forms import MapEntityForm
from caminae.core.widgets import PointOrMultipathWidget

from .models import Intervention, Project


class InterventionForm(MapEntityForm):
    geom = forms.gis.GeometryField(widget=PointOrMultipathWidget)

    modelfields = (
            'name',
            'structure',
            'date',
            'status',
            'typology',
            'disorders',
            Field('comments', css_class='input-xlarge'),
            'in_maintenance',
            'length',
            'height',
            'width',
            'area',
            'slope',
            'material_cost',
            'heliport_cost',
            'subcontract_cost',
            'stake',
            'project',)
    geomfields = ('geom',)

    def save(self, commit=True):
        intervention = super(InterventionForm, self).save(commit)
        if not commit:
            return intervention
        
        geom = self.cleaned_data.get('geom')
        if not geom:
            pass  # raise ValueError !

        if isinstance(geom, Point):
            intervention.initFromPoint(geom)
        elif isinstance(geom, LineString):
            # TODO: later it should be list of Path objects (from list of pks in form)
            intervention.initFromPathsList(geom)
        return intervention

    class Meta:
        model = Intervention
        exclude = ('deleted', 'topology', 'jobs')  # TODO


class ProjectForm(MapEntityForm):
    modelfields = (
            'name',
            'structure',
            'begin_year',
            'end_year',
            'constraint',
            'cost',
            Field('comments', css_class='input-xlarge'),
            'contractors',
            'project_owner',
            'project_manager',
            'founders',)
    geomfields = tuple()  # no geom field in project

    class Meta:
        model = Project
        exclude = ('deleted',)