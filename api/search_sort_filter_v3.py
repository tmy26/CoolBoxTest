import re
from django.http import HttpRequest
from django.db import connection
from django.core.cache import cache
from .algorithms import Algorithms


class ManualSQLQueryEngine:
    """ A service class that handles manual SQL querying, caching, and in-memory operations.
    
        This class loads and caches all company related data into memory to perform
        search, filtering, and sorting operations without repeated database hits.
        
        Methods
        _______
        _get_all_data() -> list[dict]
            Loads and caches the full dataset from the database.
        _execute_sql(sql: str, params: list) -> list[dict]
            Executes raw SQL safely and returns results as a list of dictionaries.
        _parse_query(query_string: str) -> list[dict]
            Parses text-based search queries into structured filter clauses.
        _filter_data(data: list, clauses: list) -> list[dict]
            Filters cached data in memory based on query clauses.
        search_data(request)
            Main public method for performing full in-memory search and sort operations.
    """

    QUERY_RE = re.compile(r'(\w+)\s*(>=|<=|>|<|:|=|~)\s*"?([^"]+)"?')
    LOGIC_RE = re.compile(r'\s+(AND|OR)\s+', re.IGNORECASE)

    FIELD_MAP = {
        "id": "id",
        "name": "name",
        "country": "country",
        "industry": "industry",
        "founded_year": "founded_year",
        "company_type": "company_type",
        "size": "size",
        "ceo_name": "ceo_name",
        "headquarters": "headquarters",
        "financial_year": "financial_year",
        "revenue": "revenue",
        "net_income": "net_income",
    }

    CACHE_KEY = "inmemory:all_company_data"
    CACHE_TTL = 60 * 5  # 5 minutes

    @classmethod
    def _get_all_data(cls) -> list:
        """Fetches and caches the entire company dataset with joined details.
        :return: A list of all company records (each as a dictionary).
        :rType: list of dicts.
        """
        data = cache.get(cls.CACHE_KEY)
        if data is not None:
            # If a cache is avaibel return it
            print('yaya abundaba you did hit the spot')
            print('dasdasdasdasdas Test dasdasdasdasdasdad')
            return data

        sql = """
            SELECT 
                c.id, c.name, c.industry, c.country, c.founded_year,
                d.company_type, d.size, d.ceo_name, d.headquarters,
                f.year AS financial_year, f.revenue, f.net_income
            FROM api_company AS c
            LEFT JOIN api_companydetails AS d ON d.company_id = c.id
            LEFT JOIN api_financialdata AS f ON f.company_id = c.id;
        """
        data = cls._execute_sql(sql, [])
        cache.set(cls.CACHE_KEY, data, cls.CACHE_TTL)
        return data

    def _execute_sql(sql: str, params: list) -> list:
        """Executes raw SQL safely and returns query results.
        
        :param sql: The SQL query string to execute.
        :type sql: str.
        :param params: List of query parameters for safe substitution.
        :type params: list.
        :return: Query results as a list of dictionaries.
        :rType: list of dictionaries.
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    @classmethod
    def _parse_query(cls, query_string: str) -> list:
        """Parses a structured search query into logical filter clauses.
        
        :param query_string: The text query (e.g. "industry:Tech AND revenue>1000").
        :type query_string: str.
        :return: A list of filter clauses with logic connectors (AND/OR).
        :rType: list of dictionaries.
        """
        if not query_string:
            return []
        parts = re.split(cls.LOGIC_RE, query_string.strip())
        clauses = []
        for i in range(0, len(parts), 2):
            filters = [{"field": f, "op": o, "val": v} for f, o, v in cls.QUERY_RE.findall(parts[i])]
            logic = parts[i + 1].upper() if i + 1 < len(parts) else None
            clauses.append({"filters": filters, "logic": logic})
        return clauses

    def _match(record: dict, f: dict) -> bool:
        """Compares a single record field against a filter condition.
            Bassically said, this function checks whether a given record satisfies a single
            query condition based on the provided field, operator and value.
        
        :param record: The data record that is going to be checked.
        :type record: dict.
        :param f: The dictionary containing a 'filter' condition with keys "field", "op", and "val".
        :type f: dict.
        :return: True if the record satisfies the condition else False.
        :rType: bool.
        """
        
        field = f["field"]
        op = f["op"]
        val = f["val"]
        rec_val = record.get(field)

        if rec_val is None:
            return False

        # Normalize case for string comparison
        if isinstance(rec_val, str):
            rec_val_lower = rec_val.lower()
            val_lower = str(val).lower()
        else:
            rec_val_lower = rec_val
            val_lower = val

        # Operator logic
        try:
            if op in (":", "="):
                return str(rec_val_lower) == str(val_lower)
            elif op == "~":
                return str(val_lower) in str(rec_val_lower)
            elif op == ">":
                return float(rec_val) > float(val)
            elif op == "<":
                return float(rec_val) < float(val)
            elif op == ">=":
                return float(rec_val) >= float(val)
            elif op == "<=":
                return float(rec_val) <= float(val)
        except (ValueError, TypeError):
            return False
        return False


    @classmethod
    def filter_data(cls, data: list, clauses: list) -> list:
        """Applies search filters on cached data entirely in memory.
        
        :param data: List of all records (from cache).
        :type data: list[dict].
        :param clauses: Parsed query filters from `_parse_query`.
        :type clauses: list[dict].
        :return: Filtered subset of the input data.
        :rType: list[dict].
        """
        if not clauses:
            return data

        result = data
        for clause in clauses:
            subfiltered = [r for r in result if all(cls._match(r, f) for f in clause["filters"])]
            if clause["logic"] == "OR":
                result = list({id(r): r for r in (result + subfiltered)}.values())
            else:
                result = subfiltered
        return result

    @classmethod
    def search_data(cls, request: HttpRequest) -> list:
        """The 'orchestrator' function, combines all of the above methods,
            performs filtering / sorting if needed and returns the results as a list.
        
        :param request: The HTTP request data.
        :type request: HttpRequest.
        :return: A NON / filtered /& sorted list of company records.
        :rType: list[dict].
        
        Example
        _______
        request.data = {
            "search input": "industry:Tech AND revenue>1000000",
            "sort_by": "revenue",
            "sort order": "desc",
            "algorithm": "quicksort"
        }
        """

        # Get requerid data
        query_string = request.data.get("search input", "")
        sort_field = request.data.get("sort_by")
        sort_order = (request.data.get("sort order") or "asc").lower()
        algo_to_use = request.data.get("algorithm", "mergesort")

        # Load the cached data
        all_data = cls._get_all_data()

        # Apply filters
        clauses = cls._parse_query(query_string)
        filtered = cls.filter_data(all_data, clauses)

        # Sorting
        if sort_field:
            reverse = sort_order == "desc"
            if algo_to_use == "mergesort":
                filtered = Algorithms.merge_sort(filtered, sort_field, reverse)
            else:
                filtered = Algorithms.quick_sort(filtered, sort_field, reverse)

        return filtered


# TODO: write tests, fix docstrings and fill the READ.me document w explanations.