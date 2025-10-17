import pytest
from api.models import Company, FinancialData, CompanyDetails
from api.custom_exceptions import ErrorMissingColumns, GenericException
from api.csv_parser import ParseFile, COMPANY_INFORMATION_DATA_MAPPING


@pytest.fixture
def mock_csv_ok(tmp_path):
    """A valid CSV file with all required columns."""
    csv_data = (
        "Name;Country;Industry;Year of foundation;Year;Revenue;Net Income;Privacy;Size;CEO Name;Headquarters\n"
        "Acme;USA;Tech;2000;2024;1000;200;Public;100-500;Jane Doe;New York\n"
        "Beta;UK;Finance;1995;2023;500;100;Private;50-100;John Smith;London\n"
    )
    file_path = tmp_path / "ok.csv"
    file_path.write_text(csv_data)
    return file_path


@pytest.fixture
def mock_csv_missing_column(tmp_path):
    """CSV missing required columns."""
    csv_data = (
        "Name;Country;Industry;Year of foundation;Year;Revenue;Net Income;Privacy;Size;CEO Name\n"  # missing Headquarters
        "Acme;USA;Tech;2000;2024;1000;200;Public;100-500;Jane Doe\n"
    )
    file_path = tmp_path / "missing.csv"
    file_path.write_text(csv_data)
    return file_path


@pytest.mark.django_db(transaction=True)
class TestParseFile:
    """Integration-style tests for ParseFile using the Django test DB."""

    def test_check_columns_passes_when_all_present(self):
        cols = COMPANY_INFORMATION_DATA_MAPPING.keys()
        ok, missing = ParseFile._check_columns(cols, COMPANY_INFORMATION_DATA_MAPPING)
        assert ok is True
        assert missing == []

    def test_check_columns_fails_when_missing(self):
        cols = ["Name", "Country"]
        ok, missing = ParseFile._check_columns(cols, COMPANY_INFORMATION_DATA_MAPPING)
        assert ok is False
        assert "Industry" in missing

    def test_read_csv_creates_records(self, mock_csv_ok):
        """Should parse CSV and create Company + related objects."""
        ParseFile.read_csv_file_and_create_records(mock_csv_ok, COMPANY_INFORMATION_DATA_MAPPING)

        # Validate created records
        companies = Company.objects.all()
        assert companies.count() == 2

        for company in companies:
            assert FinancialData.objects.filter(company=company).exists()
            assert CompanyDetails.objects.filter(company=company).exists()

    def test_read_csv_missing_column_raises(self, mock_csv_missing_column):
        """Should raise an exception that includes 'Missing columns: Headquarters'."""
        with pytest.raises((GenericException, ErrorMissingColumns)) as exc_info:
            ParseFile.read_csv_file_and_create_records(
                mock_csv_missing_column,
                COMPANY_INFORMATION_DATA_MAPPING,
            )

        assert "Missing columns:" in str(exc_info.value)

    def test_generic_exception_on_invalid_file(self):
        """Invalid path should raise GenericException."""
        with pytest.raises(GenericException):
            ParseFile.read_csv_file_and_create_records("nonexistent.csv", COMPANY_INFORMATION_DATA_MAPPING)
