from rest_framework import serializers
from api.models import Company, FinancialData, CompanyDetails


class SerializerFinancialData(serializers.ModelSerializer):
    """Serializer for FinancialData model."""
    class Meta:
        model = FinancialData
        fields = ['year', 'revenue', 'net_income']


class SerializerCompanyDetails(serializers.ModelSerializer):
    """Serializer for CompanyDetails model."""
    class Meta:
        model = CompanyDetails
        fields = ['company_type', 'size', 'ceo_name', 'headquarters']


class SerializerCompany(serializers.ModelSerializer):
    """Main serializer for Company, including details and financial data."""
    details = SerializerCompanyDetails(read_only=True)
    financial_data = SerializerFinancialData(many=True, read_only=True)

    class Meta:
        model = Company
        fields = [
            'name',
            'country',
            'industry',
            'founded_year',
            'details',
            'financial_data'
        ]


class SerializerCompanyCompact(serializers.ModelSerializer):
    """Lighter seriazlier for smaller JSON responses."""
    class Meta:
        model = Company
        fields = ['name', 'industry', 'country', 'founded_year']
