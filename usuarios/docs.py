from usuarios.requeST import PostLoginRequest


from drf_spectacular.utils import extend_schema


iniciarsession = extend_schema(
    description="""
    Esta es la ruta del login
    sirve para iniciar session
    """,
    summary="sirve para iniciar session",
    request=PostLoginRequest,
)