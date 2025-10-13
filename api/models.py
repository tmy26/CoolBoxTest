from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=25)
    country = models.CharField(max_length=20)
    industry = models.CharField(max_length=30)
    founded_year = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class FinancialData(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='financial_data'
    )
    year = models.PositiveIntegerField()
    revenue = models.DecimalField(max_digits=20, decimal_places=2)
    net_income = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = ('company', 'year')
        ordering = ['-year']

    def __str__(self):
        return f"{self.company.name} - {self.year}"


class CompanyDetails(models.Model):
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name='details'
    )
    company_type = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    ceo_name = models.CharField(max_length=30)
    headquarters = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.company.name} Details"
