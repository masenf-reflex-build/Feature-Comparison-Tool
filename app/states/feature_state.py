import reflex as rx
import pandas as pd
from typing import (
    List,
    Dict,
    Union,
    Optional as TypingOptional,
)
from app.databricks_utils import async_query_df


class FeatureState(rx.State):
    features_list: List[str] = []
    selected_feature_1: TypingOptional[str] = None
    selected_feature_2: TypingOptional[str] = None
    feature_1_chart_data: List[
        Dict[str, Union[str, float]]
    ] = []
    feature_2_chart_data: List[
        Dict[str, Union[str, float]]
    ] = []
    is_loading_features: bool = False
    is_loading_data_1: bool = False
    is_loading_data_2: bool = False
    error_message: str = ""

    @rx.event(background=True)
    async def load_features(self):
        async with self:
            self.is_loading_features = True
            self.error_message = ""
        try:
            df = await async_query_df(
                "SELECT DISTINCT Feature FROM feature_analysis ORDER BY Feature"
            )
            async with self:
                self.features_list = (
                    df["Feature"].tolist()
                    if not df.empty
                    else []
                )
        except Exception as e:
            async with self:
                self.error_message = (
                    f"Error loading features: {str(e)}"
                )
                self.features_list = []
        finally:
            async with self:
                self.is_loading_features = False

    def _format_chart_data(
        self,
        feature_name: TypingOptional[str],
        df: pd.DataFrame,
    ) -> List[Dict[str, Union[str, float]]]:
        if df.empty or feature_name is None:
            return []
        row = df.iloc[0]
        current_value = row.get("Current_Value")
        optimal_value = row.get("Optimal_Value")
        if pd.isna(current_value) or pd.isna(optimal_value):
            print(
                f"Warning: Missing Current_Value or Optimal_Value for feature {feature_name}"
            )
            return []
        return [
            {
                "category": feature_name,
                "Current_Value": float(current_value),
                "Optimal_Value": float(optimal_value),
            }
        ]

    @rx.event
    def select_feature_1(self, feature_name: str):
        self.selected_feature_1 = (
            feature_name if feature_name else None
        )
        self.feature_1_chart_data = []
        if self.selected_feature_1:
            return FeatureState.load_feature_1_data
        return rx.console_log(
            f"Feature 1 selection cleared or invalid: {feature_name}"
        )

    @rx.event(background=True)
    async def load_feature_1_data(self):
        if not self.selected_feature_1:
            async with self:
                self.feature_1_chart_data = []
            return
        async with self:
            self.is_loading_data_1 = True
            self.error_message = ""
        try:
            query = f"SELECT Feature, Current_Value, Optimal_Value FROM feature_analysis WHERE Feature = '{self.selected_feature_1}'"
            df = await async_query_df(query)
            async with self:
                self.feature_1_chart_data = (
                    self._format_chart_data(
                        self.selected_feature_1, df
                    )
                )
        except Exception as e:
            async with self:
                self.error_message = f"Error loading data for {self.selected_feature_1}: {str(e)}"
                self.feature_1_chart_data = []
        finally:
            async with self:
                self.is_loading_data_1 = False

    @rx.event
    def select_feature_2(self, feature_name: str):
        self.selected_feature_2 = (
            feature_name if feature_name else None
        )
        self.feature_2_chart_data = []
        if self.selected_feature_2:
            return FeatureState.load_feature_2_data
        return rx.console_log(
            f"Feature 2 selection cleared or invalid: {feature_name}"
        )

    @rx.event(background=True)
    async def load_feature_2_data(self):
        if not self.selected_feature_2:
            async with self:
                self.feature_2_chart_data = []
            return
        async with self:
            self.is_loading_data_2 = True
            self.error_message = ""
        try:
            query = f"SELECT Feature, Current_Value, Optimal_Value FROM feature_analysis WHERE Feature = '{self.selected_feature_2}'"
            df = await async_query_df(query)
            async with self:
                self.feature_2_chart_data = (
                    self._format_chart_data(
                        self.selected_feature_2, df
                    )
                )
        except Exception as e:
            async with self:
                self.error_message = f"Error loading data for {self.selected_feature_2}: {str(e)}"
                self.feature_2_chart_data = []
        finally:
            async with self:
                self.is_loading_data_2 = False