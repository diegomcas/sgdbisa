from django.contrib.gis.geos import GeometryCollection
from documental.models import Proyecto, Documento, Archivo

class JsLayer:
    """
    Genera las capas de Leaflet a partir de objetos:
    - Proyecto
    - Documento
    - Archivo
    """
    def __init__(self, objects):
        self.objects = objects
        self.total_geom = GeometryCollection()
        self.leaflet_dict = {}

    def leaflet_str(self):
        dict2str = str(self.leaflet_dict)
        return dict2str.replace('\'', '')

    def make_layers(self):
        layers_docs = None
        layers_files = None

        if type(self.objects) == Proyecto:
            # Childrens son Documentos y Archivos pero Documentos sin Archivos referidos
            docs = self.objects.documentos_proyecto.all()
            for doc in docs:
                layer_doc = self.document2layers(doc)
                if layer_doc is not None:
                    if layers_docs is not None:
                        layers_docs.append(layer_doc)
                    else:
                        layers_docs = []
                        layers_docs.append(layer_doc)

            files = self.objects.archivos_proyecto.all()
            for file in files:
                layer_file = self.archivo2layer(file)
                if layer_file is not None:
                    if layers_files is not None:
                        layers_files.append(layer_file)
                    else:
                        layers_files = []
                        layers_files.append(layer_file)

            if (layers_docs is not None) or (layers_files is not None):
                self.leaflet_dict = self.object_node(self.objects)
                if layers_docs is not None:
                    doc_node = self.generic_node('Documentos')
                    doc_node['children'] = layers_docs
                    self.leaflet_dict['children'].append(doc_node)
                if layers_files is not None:
                    file_node = self.generic_node('Archivos')
                    file_node['children'] = layers_files
                    self.leaflet_dict['children'].append(file_node)

        if type(self.objects) == Documento:
            layer_doc = self.document2layers(self.objects, True)
            if layer_doc is not None:
                proyecto = self.objects.proyecto
                self.leaflet_dict = self.object_node(proyecto)
                self.leaflet_dict['children'] = [layer_doc]

        if type(self.objects) == Archivo:
            layer_file = self.archivo2layer(self.objects)
            if layer_file is not None:
                proyecto = self.objects.proyecto
                self.leaflet_dict = self.object_node(proyecto)
                self.leaflet_dict['children'] = [layer_file]

        if '.QuerySet' in str(type(self.objects)):
            # recorrer objetos espaciales
            # crear un nodo por proyecto (OJO!!!)
            # crear un nodo por tipo de objeto (Archivo o Documento)
            pass

    def object_node(self, object):
        obj_name = str(type(object)).split('.').pop().replace('\'>', '')
        object_node = {
            'label': f'"{obj_name}: {object}"',
            'selectAllCheckbox': 'true',
            'children': []
        }

        return object_node

    def generic_node(self, title):
        generic_node = {
            'label': f'"{title}"',
            'selectAllCheckbox': 'true',
            'children': []
        }

        return generic_node

    def ee2layer(self, ee, title, file=False):
        if len(ee) > 1:  # Puntos
            desc = f'{title} (Puntos)'
            return self.points2layer(ee, desc, file)
        elif len(ee) == 1:
            if ee[0].tipo_elemento == 'PL':
                desc = f'{title} (Polígono)'
                self.total_geom.append(ee[0].poligono)
                return self.polygon2layer(ee[0], desc, file)
            if ee[0].tipo_elemento == 'LN':
                desc = f'{title} (Línea)'
                self.total_geom.append(ee[0].linea)
                return self.line2layer(ee[0], desc, file)
        else:
            return None

    def points2layer(self, ees, desc, file=False):
        layer_nodo_puntos = self.generic_node(f'Puntos: {desc}')
        children_puntos = layer_nodo_puntos['children']
        for ee in ees:
            atrib = ee.atributo if ee.atributo is not None else 'Punto'
            esp_data = [ee.punto.coords[0], ee.punto.coords[1]]
            if file:
                layer_str = f'L.marker({esp_data}, {{icon: greenIcon}}).bindPopup("{desc}")'
            else:
                layer_str = f'L.marker({esp_data}).bindPopup("{desc}")'

            dict_layer = {
                'label': f'"{atrib}"',
                'layer': layer_str
            }
            children_puntos.append(dict_layer)
            self.total_geom.append(ee.punto)

        return layer_nodo_puntos

    def line2layer(self, ee, desc, file=False):
        esp_data = [[c[0], c[1]] for c in ee.linea.coords]
        if file:
            layer_str = f'L.polyline({esp_data}, {{color: "green"}}).bindPopup("{desc}")'
        else:
            layer_str = f'L.polyline({esp_data}).bindPopup("{desc}")'

        dict_layer = {
            'label': f'"{desc}"',
            'layer': layer_str
        }

        return dict_layer

    def polygon2layer(self, ee, desc, file=False):
        esp_data = [[c[0], c[1]] for c in ee.poligono.coords[0]]
        if file:
            layer_str = f'L.polygon({esp_data}, {{color: "green"}}).bindPopup("{desc}")'
        else:
            layer_str = f'L.polygon({esp_data}).bindPopup("{desc}")'

        dict_layer = {
            'label': f'"{desc}"',
            'layer': layer_str
        }

        return dict_layer

    def document2layers(self, documento, childrens=False):
        layer_doc = None
        layer_files = None
        layer_file_title = None
        layer_doc_title = None
        ees = documento.espacial.all()
        if len(ees) > 0:
            layer_doc = self.ee2layer(ees, documento.__str__())

        if childrens:  # Armar capas de archivos referenciados
            files = documento.compuesto_por.all()
            for file in files:
                layer_file = self.archivo2layer(file)
                if layer_file is not None:
                    if layer_files is not None:
                        layer_files.append(layer_file)
                    else:
                        layer_files = []
                        layer_files.append(layer_file)

            if layer_files is not None:
                # Agregar Childrens a diccionario layer_title
                layer_file_title = self.generic_node('Archivos')
                layer_file_title['children'] = layer_files

        if (layer_doc is not None) or (layer_file_title is not None):
            layer_doc_title = self.object_node(documento)
            if layer_doc is not None:
                layer_doc_title['children'] = [layer_doc]
                if layer_file_title is not None:
                    layer_doc_title['children'].append(layer_file_title)
            else:
                layer_doc_title['children'] = [layer_file_title]

        return layer_doc_title

    def archivo2layer(self, archivo):
        layer_file = None
        ees = archivo.espacial.all()
        if len(ees) > 0:
            layer_file = self.ee2layer(ees, archivo.__str__(), True)

        return layer_file

    def cordsminmax(self):
        if not self.total_geom.empty:
            coords = self.total_geom.envelope.coords[0]
            x_component = [x[0] for x in coords]
            y_component = [y[1] for y in coords]
            return [[min(x_component), min(y_component)], [max(x_component), max(y_component)]]
        else:
            return [[-56.757721, -74.160839], [-21.357144, -53.366386]]
