import pandas
import os
import django
import sys

# Add the project root path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Path to djano settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coolboxtest.settings')

# Django initialize
django.setup()

from coolboxtest.settings import COMPANY_INFORMATION_FILE_PATH
from api.models import Company, FinancialData, CompanyDetails
from api.custom_exceptions import ErrorMissingColumns, GenericException
from django.db import transaction


COMPANY_INFORMATION_DATA_MAPPING = {
    'Name': 'name',
    'Country': 'country',
    'Industry': 'industry',
    'Year of foundation': 'founded_year',
    'Year': 'year',
    'Revenue': 'revenue',
    'Net Income': 'net_income',
    'Privacy': 'company_type',
    'Size': 'size',
    'CEO Name': 'ceo_name',
    'Headquarters': 'headquarters',
}


class ParseFile:
    """Custom class for handling the parsing of the .csv files.

    This class includes methods for validating columns, reading the .csv file and creating records.

    Methods
    -------
    _check_columns(columns, mapping_to_use: dict) -> tuple[bool, list]
        Method to verify the data integrity of the .csv file

    read_csv_file_and_create_records(cls, file_path: str, mapping_to_use: dict) -> None
        Method to parse the .csv file into pandas - dataframe, and create records.
    """

    @staticmethod
    def _check_columns(columns, mapping_to_use: dict) -> tuple[bool, list]:
        """Method to verify the data integrity of the .csv file
        :param columns: The read columns.
        :type columns: str.
        :param mapping_to_use: Tells the function which mapping to use.
        :type mapping_to_use: dict
        ...
        :return: True if data integrity is kept. False if there are missing columns or columns,
        that may not be mapped.
        :rtype: bool.
        """
        missing_columns = [column for column in mapping_to_use.keys() if column not in columns]
        if missing_columns:
            formatted_columns = ', '.join(missing_columns)
            return False, formatted_columns
        return True, []
    

    @classmethod
    def read_csv_file_and_create_records(cls, file_path: str, mapping_to_use: dict) -> None:
        """Method to parse the .csv file into pandas - dataframe, and create records.
        :param file_path: The path of the file that is going to be read.
        :type file_path: str.
        :param mapping_to_use: Tells the function which mapping to use.
        :type mapping_to_use: dict
        ...
        :raises ErrorMissingColumns: If there are missing columns - eg the data integrity of the file is breached.
        :raises GenericExceptionError: If unexpected error occurs.
        ...
        :return: None.
        :rtype: NoneType.
        """
        try:
            # Parse the file
            raw_data = pandas.read_csv(file_path, keep_default_na=False, sep=';')
            check_columns, missing_columns = cls._check_columns(raw_data.columns, mapping_to_use)

            if not check_columns:
                raise ErrorMissingColumns(f'Missing columns: {missing_columns}')

            # Reset the db
            Company.objects.all().delete()

            # Data unziping
            # Author note - this could be separated into different function, but because of the struct
            #   of the db, and using atomic function i decided to not separate it!
            for _, row in raw_data.iterrows():
                row_data = {v: row[k] for k, v in mapping_to_use.items()}

                # Verifying that all records will be created.
                with transaction.atomic():
                    # Create company
                    company = Company.objects.create(
                        name=row_data['name'],
                        country=row_data['country'],
                        industry=row_data['industry'],
                        founded_year=row_data['founded_year'],
                    )

                    # Create related FinancialData
                    FinancialData.objects.create(
                        company=company,
                        year=row_data['year'],
                        revenue=row_data['revenue'],
                        net_income=row_data['net_income'],
                    )

                    # Create related CompanyDetails
                    CompanyDetails.objects.create(
                        company=company,
                        company_type=row_data['company_type'],
                        size=row_data['size'],
                        ceo_name=row_data['ceo_name'],
                        headquarters=row_data['headquarters'],
                    )

            print("The records were created successfully!")

        except Exception as error:
            raise GenericException(error)


if __name__ == "__main__":
    ParseFile.read_csv_file_and_create_records(COMPANY_INFORMATION_FILE_PATH, COMPANY_INFORMATION_DATA_MAPPING)
