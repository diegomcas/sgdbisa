def list_listas_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para listar listas de chequeo.
    """
    if 'calidad.list_listaschequeo' in user.get_all_permissions():
        return True

    return False


def view_lista_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para ver listas de chequeo.
    """
    if 'calidad.view_listachequeo' in user.get_all_permissions():
        return True

    return False


def add_lista_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para crear listas de chequeo.
    """
    if 'calidad.add_listachequeo' in user.get_all_permissions():
        return True

    return False


def update_lista_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para editar listas de chequeo.
    """
    if 'calidad.change_listachequeo' in user.get_all_permissions():
        return True

    return False


def delete_lista_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para eliminar listas de chequeo.
    """
    if 'calidad.delete_listachequeo' in user.get_all_permissions():
        return True

    return False


def list_tipos_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para listar tipos de chequeo.
    """
    if 'calidad.list_tiposchequeo' in user.get_all_permissions():
        return True

    return False


def view_tipo_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para listar tipos de chequeo.
    """
    if 'calidad.view_tipochequeo' in user.get_all_permissions():
        return True

    return False


def add_tipo_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para agregar tipos de chequeo.
    """
    if 'calidad.add_tipochequeo' in user.get_all_permissions():
        return True

    return False


def update_tipo_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para modificar tipos de chequeo.
    """
    if 'calidad.change_tipochequeo' in user.get_all_permissions():
        return True

    return False


def delete_tipo_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para eliminar tipos de chequeo.
    """
    if 'calidad.delete_tipochequeo' in user.get_all_permissions():
        return True

    return False


def add_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para agregar chequeos a documentos.
    """
    if 'calidad.add_chequeo' in user.get_all_permissions():
        return True

    return False


def change_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para hacer el control de calidad a documentos.
    """
    if 'calidad.change_chequeo' in user.get_all_permissions():
        return True

    return False


def delete_chequeo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para eliminar un chequeo a un documentos.
    """
    if 'calidad.delete_chequeo' in user.get_all_permissions():
        return True

    return False
