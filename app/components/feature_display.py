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
        "border": "2px solid black",
        "padding": "8px",
        "box_shadow": "2px 2px 0px #000000",
    },
    "item_style": {"color": "#1f2937"},
    "label_style": {
        "color": "#059669",
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
                    class_name="text-emerald-600 h-8 w-8"
                ),
                rx.el.p(
                    "Loading chart data...",
                    class_name="text-neutral-600 mt-2 font-medium",
                ),
                class_name="flex flex-col items-center justify-center h-full",
            ),
            rx.cond(
                chart_data.length() > 0,
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(
                        stroke_dasharray="3 3",
                        horizontal=True,
                        vertical=False,
                        class_name="stroke-neutral-300 opacity-75",
                    ),
                    rx.recharts.graphing_tooltip(
                        **TOOLTIP_PROPS
                    ),
                    rx.recharts.x_axis(
                        data_key="category",
                        name="Feature",
                        tick_line=False,
                        axis_line=False,
                        class_name="text-xs text-neutral-700 fill-neutral-700 font-medium",
                    ),
                    rx.recharts.y_axis(
                        tick_line=False,
                        axis_line=False,
                        allow_decimals=True,
                        class_name="text-xs text-neutral-700 fill-neutral-700 font-medium",
                        label={
                            "value": "Value",
                            "angle": -90,
                            "position": "insideLeft",
                            "style": {
                                "text_anchor": "middle",
                                "fill": "#404040",
                                "font_size": "12px",
                                "font_weight": "500",
                            },
                        },
                    ),
                    rx.recharts.bar(
                        data_key="Current_Value",
                        name="Current Value",
                        fill="#059669",
                        bar_size=30,
                    ),
                    rx.recharts.bar(
                        data_key="Optimal_Value",
                        name="Optimal Value",
                        fill="#0ea5e9",
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
                    class_name="bg-white",
                ),
                rx.el.div(
                    rx.cond(
                        feature_name.is_not_none(),
                        rx.el.p(
                            "No data to display for ",
                            rx.el.span(
                                feature_name,
                                class_name="font-semibold text-emerald-700",
                            ),
                            ".",
                        ),
                        rx.el.p(
                            "Select a feature to display its graph."
                        ),
                    ),
                    class_name="flex items-center justify-center h-full text-neutral-500 text-sm p-4 text-center font-medium",
                ),
            ),
        ),
        class_name="w-full p-1 border-2 border-black bg-white min-h-[350px] shadow-[4px_4px_0px_#000000]",
    )


def feature_comparison_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Feature Experiment Dashboard",
            class_name="text-4xl font-bold text-black mb-12 text-center tracking-tight font-['Archivo_Black']",
        ),
        rx.cond(
            FeatureState.error_message != "",
            rx.el.div(
                rx.el.strong(
                    "Error: ",
                    class_name="font-bold text-red-700",
                ),
                FeatureState.error_message,
                class_name="bg-red-100 border-2 border-red-600 text-red-700 px-4 py-3 mb-8 font-medium shadow-[4px_4px_0px_#ef4444]",
                role="alert",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Feature A",
                    class_name="block text-xl font-bold text-black mb-3 font-['Archivo_Black']",
                ),
                rx.el.select(
                    rx.el.option(
                        "Select Feature...",
                        value="",
                        disabled=FeatureState.is_loading_features,
                        class_name="text-neutral-500",
                    ),
                    rx.foreach(
                        FeatureState.features_list,
                        lambda feature: rx.el.option(
                            feature,
                            value=feature,
                            class_name="text-black font-medium",
                        ),
                    ),
                    default_value=FeatureState.selected_feature_1.to(
                        str
                    ),
                    on_change=FeatureState.select_feature_1,
                    disabled=FeatureState.is_loading_features,
                    class_name="mt-1 block w-full pl-3 pr-10 py-3 text-base bg-white border-2 border-black text-black focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm font-medium shadow-[2px_2px_0px_#000000]",
                ),
                rx.el.div(
                    rx.cond(
                        FeatureState.selected_feature_1.is_not_none(),
                        _render_bar_chart(
                            FeatureState.feature_1_chart_data,
                            FeatureState.selected_feature_1,
                            FeatureState.is_loading_data_1,
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Select Feature A to view graph.",
                                class_name="text-neutral-600 font-medium",
                            ),
                            class_name="mt-4 p-4 border-2 border-dashed border-neutral-400 bg-neutral-100 min-h-[350px] flex items-center justify-center text-sm",
                        ),
                    ),
                    class_name="mt-6",
                ),
                class_name="flex-1 p-6 space-y-4 bg-white border-2 border-black shadow-[6px_6px_0px_#000000]",
            ),
            rx.el.div(
                rx.el.label(
                    "Feature B",
                    class_name="block text-xl font-bold text-black mb-3 font-['Archivo_Black']",
                ),
                rx.el.select(
                    rx.el.option(
                        "Select Feature...",
                        value="",
                        disabled=FeatureState.is_loading_features,
                        class_name="text-neutral-500",
                    ),
                    rx.foreach(
                        FeatureState.features_list,
                        lambda feature: rx.el.option(
                            feature,
                            value=feature,
                            class_name="text-black font-medium",
                        ),
                    ),
                    default_value=FeatureState.selected_feature_2.to(
                        str
                    ),
                    on_change=FeatureState.select_feature_2,
                    disabled=FeatureState.is_loading_features,
                    class_name="mt-1 block w-full pl-3 pr-10 py-3 text-base bg-white border-2 border-black text-black focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm font-medium shadow-[2px_2px_0px_#000000]",
                ),
                rx.el.div(
                    rx.cond(
                        FeatureState.selected_feature_2.is_not_none(),
                        _render_bar_chart(
                            FeatureState.feature_2_chart_data,
                            FeatureState.selected_feature_2,
                            FeatureState.is_loading_data_2,
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Select Feature B to view graph.",
                                class_name="text-neutral-600 font-medium",
                            ),
                            class_name="mt-4 p-4 border-2 border-dashed border-neutral-400 bg-neutral-100 min-h-[350px] flex items-center justify-center text-sm",
                        ),
                    ),
                    class_name="mt-6",
                ),
                class_name="flex-1 p-6 space-y-4 bg-white border-2 border-black shadow-[6px_6px_0px_#000000]",
            ),
            class_name="flex flex-col md:flex-row gap-10",
        ),
        on_mount=FeatureState.load_features,
        class_name="p-6 md:p-10 bg-yellow-200 min-h-screen font-['Inter']",
    )