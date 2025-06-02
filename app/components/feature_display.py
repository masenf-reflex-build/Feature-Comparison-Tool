import reflex as rx
from app.states.feature_state import FeatureState
from typing import (
    List,
    Dict,
    Union,
    Optional as TypingOptional,
)

TOOLTIP_PROPS = {
    "cursor": False,
    "wrapper_style": {"z_index": 1000},
    "content_style": {
        "background_color": "white",
        "border": "1px solid #e0e0e0",
        "border_radius": "0.25rem",
        "box_shadow": "0 1px 3px rgba(0,0,0,0.1)",
    },
    "item_style": {"color": "#333"},
    "label_style": {
        "color": "#003366",
        "font_weight": "bold",
    },
}


def _render_bar_chart(
    chart_data: rx.Var[List[Dict[str, Union[str, float]]]],
    feature_name: rx.Var[TypingOptional[str]],
    is_loading: rx.Var[bool],
) -> rx.Component:
    return rx.el.div(
        rx.cond(
            is_loading,
            rx.el.div(
                rx.spinner(
                    class_name="text-blue-500 h-8 w-8"
                ),
                rx.el.p(
                    "Loading chart data...",
                    class_name="text-gray-600 mt-2",
                ),
                class_name="flex flex-col items-center justify-center h-72",
            ),
            rx.cond(
                chart_data.length() > 0,
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(
                        stroke_dasharray="3 3",
                        horizontal=True,
                        vertical=False,
                        class_name="opacity-30",
                    ),
                    rx.recharts.graphing_tooltip(
                        **TOOLTIP_PROPS
                    ),
                    rx.recharts.x_axis(
                        data_key="category",
                        name="Feature",
                        tick_line=False,
                        axis_line=False,
                        class_name="text-xs text-gray-600",
                    ),
                    rx.recharts.y_axis(
                        tick_line=False,
                        axis_line=False,
                        allow_decimals=True,
                        class_name="text-xs text-gray-600",
                        label={
                            "value": "Value",
                            "angle": -90,
                            "position": "insideLeft",
                            "style": {
                                "text_anchor": "middle",
                                "fill": "#666",
                                "font_size": "12px",
                            },
                        },
                    ),
                    rx.recharts.bar(
                        data_key="Current_Value",
                        name="Current Value",
                        fill="#3b82f6",
                        radius=[4, 4, 0, 0],
                        bar_size=30,
                    ),
                    rx.recharts.bar(
                        data_key="Optimal_Value",
                        name="Optimal Value",
                        fill="#10b981",
                        radius=[4, 4, 0, 0],
                        bar_size=30,
                    ),
                    data=chart_data,
                    height=300,
                    width="100%",
                    margin={
                        "top": 20,
                        "right": 20,
                        "left": 10,
                        "bottom": 5,
                    },
                    class_name="bg-white rounded-lg",
                ),
                rx.el.div(
                    rx.cond(
                        feature_name.is_not_none(),
                        rx.el.p(
                            "No data to display for ",
                            rx.el.span(
                                feature_name,
                                class_name="font-semibold",
                            ),
                            ". This might be due to missing values or a data processing error.",
                        ),
                        rx.el.p(
                            "Select a feature to display its graph."
                        ),
                    ),
                    class_name="flex items-center justify-center h-72 text-gray-500 text-sm p-4 text-center",
                ),
            ),
        ),
        class_name="w-full p-1 border border-gray-200 rounded-lg shadow-sm bg-white min-h-[350px]",
    )


def feature_comparison_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Feature Experimentation Dashboard",
            class_name="text-3xl font-bold text-gray-800 mb-8 text-center",
        ),
        rx.cond(
            FeatureState.error_message != "",
            rx.el.div(
                rx.el.strong(
                    "Error: ", class_name="font-bold"
                ),
                FeatureState.error_message,
                class_name="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6 shadow",
                role="alert",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Select Feature 1:",
                    class_name="block text-md font-semibold text-gray-700 mb-2",
                ),
                rx.el.select(
                    rx.el.option(
                        "Select Feature...",
                        value="",
                        disabled=FeatureState.is_loading_features,
                    ),
                    rx.foreach(
                        FeatureState.features_list,
                        lambda feature: rx.el.option(
                            feature, value=feature
                        ),
                    ),
                    default_value=FeatureState.selected_feature_1.to(
                        str
                    ),
                    on_change=FeatureState.select_feature_1,
                    placeholder="Select Feature 1",
                    disabled=FeatureState.is_loading_features,
                    class_name="mt-1 block w-full pl-3 pr-10 py-2.5 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md shadow-sm",
                ),
                rx.cond(
                    FeatureState.selected_feature_1.is_not_none(),
                    _render_bar_chart(
                        FeatureState.feature_1_chart_data,
                        FeatureState.selected_feature_1,
                        FeatureState.is_loading_data_1,
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Please select a feature for column 1.",
                            class_name="text-gray-500",
                        ),
                        class_name="mt-4 p-4 border border-dashed border-gray-300 rounded-lg bg-gray-50 min-h-[350px] flex items-center justify-center text-sm",
                    ),
                ),
                class_name="flex-1 p-4 space-y-4 bg-slate-50 rounded-xl shadow-md",
            ),
            rx.el.div(
                rx.el.label(
                    "Select Feature 2:",
                    class_name="block text-md font-semibold text-gray-700 mb-2",
                ),
                rx.el.select(
                    rx.el.option(
                        "Select Feature...",
                        value="",
                        disabled=FeatureState.is_loading_features,
                    ),
                    rx.foreach(
                        FeatureState.features_list,
                        lambda feature: rx.el.option(
                            feature, value=feature
                        ),
                    ),
                    default_value=FeatureState.selected_feature_2.to(
                        str
                    ),
                    on_change=FeatureState.select_feature_2,
                    placeholder="Select Feature 2",
                    disabled=FeatureState.is_loading_features,
                    class_name="mt-1 block w-full pl-3 pr-10 py-2.5 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md shadow-sm",
                ),
                rx.cond(
                    FeatureState.selected_feature_2.is_not_none(),
                    _render_bar_chart(
                        FeatureState.feature_2_chart_data,
                        FeatureState.selected_feature_2,
                        FeatureState.is_loading_data_2,
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Please select a feature for column 2.",
                            class_name="text-gray-500",
                        ),
                        class_name="mt-4 p-4 border border-dashed border-gray-300 rounded-lg bg-gray-50 min-h-[350px] flex items-center justify-center text-sm",
                    ),
                ),
                class_name="flex-1 p-4 space-y-4 bg-slate-50 rounded-xl shadow-md",
            ),
            class_name="flex flex-col md:flex-row gap-8",
        ),
        on_mount=FeatureState.load_features,
        class_name="p-6 md:p-10 bg-gradient-to-br from-slate-100 to-sky-100 min-h-screen font-['Inter']",
    )