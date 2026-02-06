from enum import Enum


class OrderBy(Enum):
    ASC = "asc"
    DESC = "desc"


class ShowBy(Enum):
    ARTICULE = "articule"
    SIZE = "size"


class CashbackFilter(Enum):
    ID = "id"
    NAME = "name"
    DATE = "date"
    SUM = "sum"


class UserFilter(Enum):
    ID = "id"
    FIRST_NAME = "first_name"
    L_NAME = "l_name"
    TG = "tg"
    PHONE = "phone"
    EMAIL = "email"


class ProductIncomesFilter(Enum):
    ID = "id"
    TITLE = "title"
    DATE = "date"
    ARTICLE_CH = "article_ch"
    ARTICLE_WB = "article_wb"
    ARTICLE_SUPPLIER = "article_supplier"
    COUNT = "count"
    PACKAGE_COUNT = "package_count"
    SIZE_WIDTH = "size_width"
    SIZE_LENGTH = "size_length"
    SIZE_HEIGHT = "size_height"


class FilterCol(Enum):
    ARTICULE = "articule"
    CATEGORY = "category"
    ARTICLE_SUPPLIER = "article_supplier"


class ChartType(Enum):
    PRICE = "price"
    KEYWORD = "keyword"
    CASHBACK = "cashback"
    BUYOUT = "buyout"
    EXPENSE = "expense"


class FinResType(Enum):
    WEEK = "weeks"
    QUARTER = "quarter"
    MONTH = "months"
    YEAR = "years"


class KeyWordsPositionTypes(Enum):

    ALL = "all"
    ADS = "ads"


class CashbackAdExpenseFilter(Enum):
    ID = "id"
    CASHBACK = "cashback"
    ANALYTIC = "analytic"
    PAYMENT_URL = "payment_url"
    PAYED_WHOM = "payed_whom"
    SUM_PAYED = "sum_payed"


class CashbackUserExpenseFilter(Enum):
    ID = "id"
    USER = "user"
    ANALYTIC = "analytic"
    CASHBACK = "cashback"
    AGREED = "agreed"
    MANAGED = "managed"


class OperationalExpencesFilter(Enum):
    ID = "id"
    SELLER = "seller"
    PAYMENT_TYPE = "payment_type"
    DESCRIPTION = "description"
    SUM = "sum"
    START_DATE = "start_date"
    END_DATE = "end_date"


class SelfCostFilter(Enum):
    ID = "id"
    COST = "cost"
    ARTICLE = "article"
    SIZE = "size"
    AMOUNT = "amount"
    DATE = "date"


class StatusGenerationVideo(Enum):
    IN_QUEUE = "in_queue"
    GENERATING = "generating"
    FINISHED = "finished"
    FAILED = "failed"
