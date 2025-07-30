"""
Apache Beam pipeline for calculating temperature variance and statistics for different sensors.
This module demonstrates windowing, CombineFn usage, and integration with SciPy in Apache Beam.
"""

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms.trigger import AfterWatermark, AccumulationMode
import numpy as np
from scipy import stats


class SensorStatisticsCombineFn(beam.CombineFn):
    """
    Calculates statistics (variance, standard deviation) for temperature values
    using SciPy and CombineFn.
    """

    def create_accumulator(self):
        """Creates an accumulator to store values for statistical processing."""
        # Store all values in a list for later processing with SciPy
        return []

    def add_input(self, accumulator, element, *args, **kwargs):
        """Adds an input value to the accumulator."""
        accumulator.append(element)
        return accumulator

    def merge_accumulators(self, accumulators, *args, **kwargs):
        """Merges multiple accumulators into a single one."""
        merged = []
        for acc in accumulators:
            merged.extend(acc)
        return merged

    def extract_output(self, accumulator, *args, **kwargs):
        """
        Calculates statistics from the accumulated values using SciPy.
        Returns a dictionary of statistical measures.
        """
        if not accumulator:
            return {
                "count": 0,
                "mean": float("nan"),
                "std_dev": float("nan"),
                "variance": float("nan"),
            }

        # Convert to numpy array for SciPy processing
        values = np.array(accumulator)

        # Calculate statistics using SciPy
        return {
            "count": len(values),
            "mean": np.mean(values),
            "std_dev": stats.tstd(values),  # SciPy's t-distribution standard deviation
            "variance": stats.variation(values)
            ** 2,  # Square of coefficient of variation
        }


def run_pipeline():
    """
    Creates and runs the Apache Beam pipeline to calculate temperature statistics.
    Uses fixed windows of 60 seconds to group temperature readings by sensor.
    """
    options = PipelineOptions()

    with beam.Pipeline(options=options) as p:
        data = [
            ("sensor_A", 20.0, 1678886400),  # March 15, 2023 00:00:00 GMT
            ("sensor_B", 25.0, 1678886410),
            ("sensor_A", 20.5, 1678886430),
            ("sensor_A", 21.0, 1678886460),
            ("sensor_B", 24.5, 1678886470),
            ("sensor_A", 20.3, 1678886490),
            (
                "sensor_A",
                22.0,
                1678886520,
            ),  # March 15, 2023 00:02:00 GMT (ends first window for A)
            ("sensor_B", 26.0, 1678886530),
            ("sensor_A", 23.0, 1678886580),  # March 15, 2023 00:03:00 GMT
            ("sensor_A", 20.0, 1678886640),  # Next window for sensor_A
            ("sensor_A", 21.0, 1678886650),
            ("sensor_A", 22.0, 1678886660),
        ]

        # This chaining structure is correct in Beam
        timed_data = (
            p
            | "Create Data" >> beam.Create(data)
            | "Add Timestamps"
            >> beam.Map(lambda x: beam.window.TimestampedValue((x[0], x[1]), x[2]))
            | "To KV" >> beam.Map(lambda x: (x[0], x[1]))
        )  # Key is sensor_id, Value is temperature

        windowed_data = timed_data | "Window" >> beam.WindowInto(
            beam.window.FixedWindows(60),
            trigger=AfterWatermark(),
            accumulation_mode=AccumulationMode.DISCARDING,
        )

        statistics_results = (
            windowed_data
            | "Group and Calculate Statistics"
            >> beam.CombinePerKey(SensorStatisticsCombineFn())
            | "Add Window Info"
            >> beam.MapTuple(
                lambda k, v, window=beam.DoFn.WindowParam: {
                    "sensor": k,
                    "window_start": window.start.to_utc_datetime(),
                    "statistics": v,
                }
            )
        )

        # Print the results in a formatted way
        statistics_results | "Print Results" >> beam.Map(
            lambda result: f"Sensor: {result['sensor']}, "
            f"Window: {result['window_start']}, "
            f"Stats: Count={result['statistics']['count']}, "
            f"Mean={result['statistics']['mean']:.2f}, "
            f"StdDev={result['statistics']['std_dev']:.4f}, "
            f"Variance={result['statistics']['variance']:.4f}"
        ) | "Output" >> beam.Map(print)


if __name__ == "__main__":
    print("Running pipeline with SciPy Statistics:")
    run_pipeline()
