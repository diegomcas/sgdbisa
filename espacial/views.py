from collections import namedtuple
from parse import parse, search
from django.db import connection
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.gis.geos import Polygon, MultiPoint, Point, GeometryCollection, GEOSGeometry, LineString
from django.contrib.gis.measure import D
# from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ElementoEspacial
from documental.models import Documento, Archivo


def srs_list():
    """
    Consulta la tabla spatial_ref_sys de PostgreSQL y retorna:
        - las proyecciones planas
        - las proyecciones geocéntricas
        - las proyecciones geográficas
    """
    with connection.cursor() as cursor:
        #  WHERE srtext LIKE '%Argentina%'
        cursor.execute("SELECT * FROM public.spatial_ref_sys")
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        columns = [col[0] for col in cursor.description]
        datos = [dict(zip(columns, row)) for row in cursor.fetchall()]

    srss = []
    tipo_srs = ''
    for geogcs in datos:
        srid = geogcs['srid']
        datum = search("DATUM[\"{}\",", geogcs['srtext'])
        definicion = search("PROJCS[\"{}\",", geogcs['srtext'])
        if definicion is not None:
            tipo_srs = 'PROJCS'
        else:
            definicion = search("GEOGCS[\"{}\",", geogcs['srtext'])
            if definicion is not None:
                tipo_srs = 'GEOGCS'
            else:
                definicion = search("GEOCCS[\"{}\",", geogcs['srtext'])
                if definicion is not None:
                    tipo_srs = 'GEOCCS'

        if tipo_srs != '':
            srss.append(
                {
                    'srid': srid,
                    'definicion': definicion.fixed[0],
                    'datum': datum.fixed[0],
                    'tipo_srs': tipo_srs
                }
            )
            tipo_srs = ''

    return srss

def strcoords2list(str):
    """
    Las coordenadas ingresadas en la página
    se parsean a una lista, incluso se traen atributos
    """
    lst_str = str.split('\r\n')
    lst_str = [val for val in lst_str if val != '']

    lst_coords = None
    for line in lst_str:
        if ',' in line:
            parse_str = parse('{:^g},{:^g}', line)
            if parse_str is None:
                parse_str = parse('{:^g},{:^g},{:^}', line)
        else:
            parse_str = parse('{:^g} {:^g}', line)
            if parse_str is None:
                parse_str = parse('{:^g} {:^g} {:^}', line)

        if parse_str is not None:
            if lst_coords is None:
                lst_coords = []
            lst_coords.append(parse_str.fixed)
        else:
            return None

    return lst_coords

def coords2polygon(lst_coords, srid):
    # Elimino atriburos, en caso de que existan
    lst_coords = [(c[0], c[1]) for c in lst_coords]
    # Verificar cierre
    if not lst_coords[0] == lst_coords[-1]:
        lst_coords.append(lst_coords[0])

    geom_obj = Polygon(lst_coords)
    geom_obj.srid = int(srid)

    if srid != 4326:
        geom_obj.transform(4326)

    return geom_obj

def coords2Point(coords, srid):
    geom_obj = Point((coords[0], coords[1]))
    geom_obj.srid = int(srid)

    print(f'geom_obj: {geom_obj}')

    if srid != 4326:
        geom_obj.transform(4326)

    return geom_obj


def coords2line(lst_coords, srid):
    # Elimino atriburos, en caso de que existan
    lst_coords = [(c[0], c[1]) for c in lst_coords]

    geom_obj = LineString(lst_coords)
    geom_obj.srid = int(srid)

    if srid != 4326:
        geom_obj.transform(4326)

    return geom_obj


def prev_definition(ee_exist):
    # Tomo el primero y capturo los valores necesarios
    obj_esp = ee_exist[0]
    t_elemento = obj_esp.tipo_elemento
    str_wkt = ''
    srid = 0
    if t_elemento == 'PT':
        srid = obj_esp.punto.srid
        for obj_esp in ee_exist:
            coords = obj_esp.punto.coords
            atributo = obj_esp.atributo
            str_wkt = str_wkt + f'{coords[0]} {coords[1]} {atributo or ""}\r\n'

    if t_elemento == 'LN':
        srid = obj_esp.poligono.srid
        coords = obj_esp.poligono.coords[0]
        for coord in coords:
            str_wkt = str_wkt + f'{coord[0]} {coord[1]}\r\n'

    if t_elemento == 'PL':
        srid = obj_esp.poligono.srid
        coords = obj_esp.poligono.coords[0]
        for coord in coords:
            str_wkt = str_wkt + f'{coord[0]} {coord[1]}\r\n'

    return [t_elemento, srid, str_wkt]

def espacial(request, pk_object, obj):
    """
    Altas bajas y modificaciones de los elementos espaciales
    """
    if obj == 'archivo':
        objeto = get_object_or_404(Archivo, pk=pk_object)
    else:
        if obj == 'documento':
            objeto = get_object_or_404(Documento, pk=pk_object)
        else:
            # No es correcta la petición, voy a HTTP_REFERER.
            print(f'HTTP_REFERER: {request.META["HTTP_REFERER"]}')

    # Obtengo todos los objetos espaciales referidos por el documento o archivo
    elementos_espaciales_existentes = objeto.espacial.all()

    # Si existen objetos espaciales
    prev_def = [None, None, None]
    if len(elementos_espaciales_existentes) > 0:
        prev_def = prev_definition(elementos_espaciales_existentes)

    error_msg = [None, None, None]
    error = False
    if request.method == "POST":
        srid = request.POST.get('srid_list')
        t_elemento = request.POST.get('tipo_elemento')
        wkt = request.POST.get('wkt_espacial')

        if srid is None:
            error_msg[0] = 'Debe seleccionar un srid de la lista.'
            error = True

        if wkt == '':
            error_msg[1] = 'Debe ingresar las coordenadas del elemento.'
            error = True

        list_geoms = []
        if not error:
            # parsear la entrada de wkt
            lista_coords = strcoords2list(wkt)

            if lista_coords is None or len(lista_coords) < 1:
                error_msg[2] = 'Lista de coordenadas vacía.'
                error = True
            else:
                if t_elemento == 'PT':
                    for coord in lista_coords:
                        geom_point = coords2Point(coord, srid)
                        if not geom_point.valid:
                            error_msg[2] = geom_point.valid_reason
                            error = True
                            break
                        else:
                            if len(coord) == 3:
                                atributo = coord[2]
                            else:
                                atributo = None
                            list_geoms.append(
                                ElementoEspacial(
                                    tipo_elemento='PT',
                                    punto=geom_point,
                                    atributo=atributo,
                                )
                            )

                if t_elemento == 'PL':
                    geom_poly = coords2polygon(lista_coords, srid)
                    if not geom_poly.valid:
                        error_msg[2] = geom_poly.valid_reason
                        error = True
                    else:
                        list_geoms.append(
                            ElementoEspacial(
                                tipo_elemento='PL',
                                poligono=geom_poly,
                                atributo=None,
                            )
                        )

                if t_elemento == 'LN':
                    geom_line = coords2line(lista_coords, srid)
                    if not geom_line.valid:
                        error_msg[2] = geom_line.valid_reason
                        error = True
                    else:
                        list_geoms.append(
                            ElementoEspacial(
                                tipo_elemento='LN',
                                linea=geom_line,
                                atributo=None,
                            )
                        )

            if not error:
                # Borro los elementos espaciales anteriores
                if len(elementos_espaciales_existentes) > 0:
                    for elemento in elementos_espaciales_existentes:
                        elemento.delete()
                # Escribo las nuevas definiciones
                for geom in list_geoms:
                    geom.save()
                    objeto.espacial.add(geom)
                objeto.save()

    return render(
        request,
        'elemento_espacial.html',
        {
            'error': error_msg,
            'objecto': objeto,
            'prev_def': prev_def,
            'tipo_elemento': ElementoEspacial._meta.get_field('tipo_elemento').choices,
            'srids': srs_list(),
        }
    )


def ee2layer(elementos_espaciales, desc, total_geom):
    """
    Convierte objetos de tipo elemento_espacial en diccionarios layer
    que son renderizados en mapping.html
    """
    t_elemento = ''
    lst_layers = []
    children_puntos = []
    layer_nodo_puntos = {
        'label': f'"{desc}"',
        'selectAllCheckbox': 'true',
        'children': children_puntos
    }
    if elementos_espaciales.count() > 0:
        for ee in elementos_espaciales:
            if ee.tipo_elemento == 'PL':
                t_elemento = 'PL'
                esp_data = [[c[0], c[1]] for c in ee.poligono.coords[0]]
                dict_layer = {
                    'label': f'"Poligono {desc}"',
                    'layer': f'L.polygon({esp_data}).bindPopup("{desc}")'
                }
                lst_layers.append(dict_layer)
                total_geom.append(ee.poligono)
            if ee.tipo_elemento == 'LN':
                t_elemento = 'LN'
                esp_data = [[c[0], c[1]] for c in ee.linea.coords]
                dict_layer = {
                    'label': f'"Linea {desc}"',
                    'layer': f'L.polyline({esp_data}).bindPopup("{desc}")'
                }
                lst_layers.append(dict_layer)
                total_geom.append(ee.linea)
            if ee.tipo_elemento == 'PT':
                t_elemento = 'PT'
                atrib = ee.atributo if ee.atributo is not None else f'Punto {desc}'
                esp_data = [ee.punto.coords[0], ee.punto.coords[1]]
                dict_layer = {
                    'label': f'"{atrib}"',
                    'layer': f'L.marker({esp_data}).bindPopup("{atrib}")'
                }
                children_puntos.append(dict_layer)
                total_geom.append(ee.punto)

        if t_elemento == 'PT':
            lst_layers = [layer_nodo_puntos]
    else:
        return None

    return [lst_layers, total_geom]


def proyecto2layers():
    pass


def documetno2layers(documento, total_geom):
    childrens_doc = []
    layer_nodo_doc = {
        'label': f'"Documento {documento.__str__()}"',
        'selectAllCheckbox': 'true',
        'children': childrens_doc
    }

    elementos_espaciales = documento.espacial.all()
    if elementos_espaciales.count() > 0:
        layer = ee2layer(elementos_espaciales, documento.__str__(), total_geom)
        if layer is not None:
            layer_doc = layer[0]
            total_geom = layer[1]
            childrens_doc.extend(layer_doc)

    layer_nodo_arch = None
    childrens_arch = []
    archivos = documento.compuesto_por.all()
    if archivos.count() > 0:
        layer_nodo_arch = {
            'label': '"Archivos"',
            'selectAllCheckbox': 'true',
            'children': childrens_arch
        }
        for archivo in archivos:
            elementos_espaciales = archivo.espacial.all()
            if elementos_espaciales.count() > 0:
                layer = ee2layer(elementos_espaciales, archivo.__str__(), total_geom)
                if layer is not None:
                    layer_archivo = layer[0]
                    total_geom = layer[1]
                    childrens_arch.extend(layer_archivo)

    if layer_nodo_arch is not None:
        childrens_doc.append(layer_nodo_arch)

    return [layer_nodo_doc, total_geom]


def archivo2layer(archivo):
    layer = None
    elementos_espaciales = archivo.espacial.all()
    if elementos_espaciales.count() > 0:
        layer = ee2layer(
            elementos_espaciales,
            'Archivo ' + archivo.__str__()
        )

    return layer


def cordsminmax(coords):
    x_component = [x[0] for x in coords]
    y_component = [y[1] for y in coords]

    return [[min(x_component), min(y_component)], [max(x_component), max(y_component)]]

def mapping(request, pk_object, obj):
    """
    Presenta en un mapa el el objeto pk_object
    """
    layers = {}

    if obj == 'proyecto':
        # Mostrar todos los documentos y los archivos del proyecto
        pass
    if obj == 'documento':
        # Mostrar el docummento y los archivos contenidos
        objeto = get_object_or_404(Documento, pk=pk_object)
        # Una GeometryCollection para almacenar todas las Geometry y calcular el centroid
        geometry = GeometryCollection()
        layers = documetno2layers(objeto, geometry)
        bounds = f'{cordsminmax(layers[1].envelope.coords[0])}'
        layers = f'{layers[0]}'.replace('\'', '')

    if obj == 'archivo':
        # Mostrar solo el archivo
        pass

    return render(
        request,
        'mapping.html',
        {
            'obj': obj,
            'objeto': objeto,
            'bounds': bounds,
            'layers': layers,
        }
    )


def consulta_espacial(request):
    """
    Gestiona las consultas espaciales y los valores devueltos
    """
    if request.method == "GET":
        if bool(request.GET.dict()):
            srid = request.GET.get('srid_list')
            coordenadas = request.GET.get('coordenadas')
            objeto = request.GET.get('objeto')
            tipo_busqueda = request.GET.get('tipo')
            distancia = request.GET.get('distancia')
            print(request.GET.dict())

            coords = strcoords2list(request.GET.get('coordenadas') + '\r\n')
            print(coords)
            # Armar un punto a partir de coords
            pnt = coords2Point(coords[0], request.GET.get('srid_list'))

            # Distancia de búsqueda
            distance = float(request.GET.get('distancia'))

            # Consulta
            result = ElementoEspacial.objects.filter(
                Q(punto__distance_lte=(pnt, D(km=distance))) |
                Q(poligono__distance_lte=(pnt, D(km=distance))) |
                Q(linea__distance_lte=(pnt, D(km=distance)))
            )

            print(result)

    return render(
        request,
        'spatial_query.html',
        {
            'srids': srs_list(),
        }
    )
