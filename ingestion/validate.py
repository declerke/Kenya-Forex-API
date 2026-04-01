import pandas as pd
import great_expectations as gx
from great_expectations.core import ExpectationSuite
from great_expectations.expectations import (
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeBetween,
    ExpectColumnValuesToBeInSet,
)

EXPECTED_CURRENCIES = ["USD", "EUR", "GBP", "CNY", "JPY"]


def validate_rates(rates_data: dict) -> bool:
    records = [
        {
            "base_currency": rates_data["base_currency"],
            "target_currency": currency,
            "rate": rate,
            "fetched_at": rates_data["fetched_at"],
        }
        for currency, rate in rates_data["rates"].items()
    ]
    df = pd.DataFrame(records)

    context = gx.get_context(mode="ephemeral")

    data_source = context.data_sources.add_pandas("forex_source")
    data_asset = data_source.add_dataframe_asset("forex_rates")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("forex_batch")

    suite = context.suites.add(ExpectationSuite(name="forex_suite"))
    suite.add_expectation(ExpectColumnValuesToNotBeNull(column="rate"))
    suite.add_expectation(ExpectColumnValuesToNotBeNull(column="target_currency"))
    suite.add_expectation(ExpectColumnValuesToNotBeNull(column="fetched_at"))
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(column="rate", min_value=0.0001, max_value=2.0)
    )
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(column="target_currency", value_set=EXPECTED_CURRENCIES)
    )

    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(name="forex_vd", data=batch_definition, suite=suite)
    )

    result = validation_definition.run(batch_parameters={"dataframe": df})
    return result.success
