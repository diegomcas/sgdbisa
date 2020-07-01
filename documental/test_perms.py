def list_proyectos(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para listar los proyectos.
    """
    if 'documental.list_proyectos' in user.get_all_permissions():
        return True

    return False


def finalize_proyecto(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para listar los proyectos.
    """
    if 'documental.finalize_proyecto' in user.get_all_permissions():
        return True

    return False


def view_proyecto(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para ver los detalles del proyecto y los documentos.
    """
    if 'documental.view_proyecto' in user.get_all_permissions():
        return True

    return False


def add_proyecto(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para crear un proyecto.
    """
    if 'documental.add_proyecto' in user.get_all_permissions():
        return True

    return False


def update_proyecto(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para editar un proyecto.
    """
    if 'documental.change_proyecto' in user.get_all_permissions():
        return True

    return False


def list_documentos(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para listar los documentos.
    """
    if 'documental.list_documentos' in user.get_all_permissions():
        return True

    return False


def view_documento(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para listar los documentos.
    """
    if 'documental.view_documento' in user.get_all_permissions():
        return True

    return False


def add_documento(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para listar los documentos.
    """
    if 'documental.add_documento' in user.get_all_permissions():
        return True

    return False


def update_documento(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para listar los documentos.
    """
    if 'documental.change_documento' in user.get_all_permissions():
        return True

    return False


def delete_documento(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para eliminar documentos.
    """
    if 'documental.delete_documento' in user.get_all_permissions():
        return True

    return False


def revision_documento(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para revisionar documentos.
    """
    if 'documental.revision_archivo' in user.get_all_permissions():
        return True

    return False


def list_archivos(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para listar los archivos.
    """
    if 'documental.list_archivos' in user.get_all_permissions():
        return True

    return False


def view_archivo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para ver archivos.
    """
    if 'documental.view_archivo' in user.get_all_permissions():
        return True

    return False


def add_archivo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para agreagar archivos.
    """
    if 'documental.add_archivo' in user.get_all_permissions():
        return True

    return False


def update_archivo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para editar archivos.
    """
    if 'documental.change_archivo' in user.get_all_permissions():
        return True

    return False


def delete_archivo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para eliminar archivos.
    """
    if 'documental.delete_archivo' in user.get_all_permissions():
        return True

    return False


def revision_archivo(user):
    """
    Verifica si el usuario, por el grupo al que pertence,
    tiene permisos para revisionar archivos.
    """
    if 'documental.revision_archivo' in user.get_all_permissions():
        return True

    return False
