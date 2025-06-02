import reflex as rx
import reflex_enterprise as rxe
from app.components.feature_display import (
    feature_comparison_dashboard,
)


def index() -> rx.Component:
    return feature_comparison_dashboard()


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="anonymous",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")