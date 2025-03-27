"""Global point for collected routers."""

from app.internal.pkg.models import Routes
from app.internal.routes import controller, data_generator

__all__ = ["__routes__"]


__routes__ = Routes(
    routers=(
        controller.router,
        data_generator.router,
    ),
)
