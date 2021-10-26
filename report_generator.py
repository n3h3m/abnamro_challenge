import logging

import pandas as pd

from configs.processed_future_movement import future_movement_config


class ReportGenerator:
    def __init__(self, input_filename, output_filename, field_configs):
        self.output_filename = output_filename
        self.field_configs = field_configs
        self.input_filename = input_filename

        try:
            self.input_df = pd.read_fwf(
                self.input_filename,
                colspecs=self.get_colspecs(self.field_configs),
                names=self.get_colnames(self.field_configs),
            )
            logging.debug("loading input from {} to the dataframe is successful".format(self.input_filename))
        except FileNotFoundError:
            logging.exception("Check if the file exists or the filename is correct".format(self.input_filename))
            raise

        # For testability reason the output_df is maintained as the class attribute
        # Otherwise can be a local variable before writing the CSV into the disk
        self.output_df = None

    @staticmethod
    def get_colspecs(field_configs):
        """
        Receives a fields configuration object which contains list of column name names and the tuples of their starting and ending positions.

        Returns a list of tuples with offset off by 1 so that it can be used by Pandas to extract fixed-width data.
        """
        global f
        logging.debug("extracting colspecs from field_configs")
        try:
            # return [(f[1] - 1, f[2]) for f in field_configs]
            colspecs = []
            for f in field_configs:
                assert len(f) == 3
                assert isinstance(f[0], str)
                assert isinstance(f[1], int)
                assert isinstance(f[2], int)
                assert f[1] <= f[2]
                colspecs.append((f[1] - 1, f[2]))  # Offset by since Pandas' index starts with 0
            return colspecs

        except (TypeError, IndexError, AssertionError):
            logging.exception("Error in parsing the configuration at ine {}".format(f))
            raise

    @staticmethod
    def get_colnames(field_configs):
        global f
        logging.debug("extracting column names from field_configs")
        # return [f[0] for f in field_configs]

        try:
            colnames = []
            for f in field_configs:
                assert len(f) == 3
                assert isinstance(f[0], str)
                assert f[0]  # Column name cannot be empty
                colnames.append(f[0])  # Offset by 1 since Pandas' index starts with 0
            return colnames

        except (TypeError, IndexError, AssertionError):
            logging.exception("Error in parsing the configuration at ine {}".format(f))
            raise

    def generate_summary_report(self):
        """
        This method is responsible for,
            For each executed trade entries
            Group by clients and product info
            Calculate sum of the total transaction amount
            Update the self.output_df
            Write the .csv file to the output filepath

        """

        # client_info and product_info can be list of columns, used by Pandas while doing groupby
        client_info = [
            "client_type",
            "client_number",
            "account_number",
            "subaccount_number",
        ]
        product_info = [
            "exchange_code",
            "product_group_code",
            "symbol",
            "transaction_date",
        ]

        # Calculate the total_transaction_amount using quantity_long - quantity_short
        self.input_df["total_transaction_amount"] = self.input_df["quantity_long"] - self.input_df["quantity_short"]

        # The actual logic that does the groupby magic and calculate the sum
        self.output_df = self.input_df.groupby(client_info + product_info, as_index=False)["total_transaction_amount"].sum()

        # Write the .csv output to the desired output filepath.
        self.output_df.to_csv(self.output_filename, index=False)

        logging.debug("Output file {} is saved to the disk".format(self.output_filename))


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        filename="logs/challenge.log",
        format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d FUNC:%(funcName)s() %(message)s",
    )

    logging.debug("Program started")

    # Create a ReportGenerator() object
    # To create ReportGenerator object we need input file, and an output filepath and a configuration object
    rg = ReportGenerator("data/input.txt", "data/output.csv", future_movement_config)

    # Generate the summary report
    rg.generate_summary_report()

    logging.debug("Program ended")


if __name__ == "__main__":
    main()
