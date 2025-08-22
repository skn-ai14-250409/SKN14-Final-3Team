from django.db import models


# ===== 공통 ENUM 선택지 =====
EMPLOYMENT_STATUS_CHOICES = [
    ("ON_DUTY", "On Duty"),
    ("ON_LEAVE", "On Leave"),
    ("RESIGNED", "Resigned"),
]

MESSAGE_FROM_CHOICES = [
    ("AI", "AI"),
    ("USER", "User"),
]

CALENDAR_STATUS_CHOICES = [
    ("CONFIRMED", "Confirmed"),
    ("TENTATIVE", "Tentative"),
    ("CANCELLED", "Cancelled"),
]

CALENDAR_VISIBILITY_CHOICES = [
    ("PUBLIC", "Public"),
    ("PRIVATE", "Private"),
]


# ===== USER 관련 =====
class Position(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Department(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BankLocation(models.Model):
    name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EmploymentType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    employee_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    manager = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    bank_location = models.ForeignKey(BankLocation, null=True, on_delete=models.SET_NULL)

    hire_date = models.DateField()
    ext_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    employment_status = models.CharField(
        max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default="ON_DUTY"
    )
    employment_type = models.ForeignKey(EmploymentType, null=True, on_delete=models.SET_NULL)

    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    password_changed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ===== TO-DO & 캘린더 =====
class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CalendarEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=CALENDAR_STATUS_CHOICES, default="CONFIRMED")
    visibility = models.CharField(max_length=20, choices=CALENDAR_VISIBILITY_CHOICES, default="PUBLIC")
    location = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventAttendee(models.Model):
    event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    attendee_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    attendee_email = models.EmailField(null=True, blank=True)
    response_status = models.CharField(
        max_length=20,
        choices=[
            ("NEEDS_ACTION", "Needs Action"),
            ("ACCEPTED", "Accepted"),
            ("DECLINED", "Declined"),
            ("TENTATIVE", "Tentative"),
        ],
        default="NEEDS_ACTION",
    )
    is_optional = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# ===== 챗봇 =====
class ChatbotHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChatbotSession(models.Model):
    chatbot_history = models.ForeignKey(ChatbotHistory, on_delete=models.CASCADE)
    content_from = models.CharField(max_length=10, choices=MESSAGE_FROM_CHOICES, default="USER")
    content = models.TextField()
    sent_at = models.DateTimeField()


class ChatbotRetrivalEvent(models.Model):
    session_msg = models.ForeignKey(ChatbotSession, on_delete=models.CASCADE)
    retriever = models.CharField(max_length=100)
    query_text = models.TextField()
    k = models.IntegerField(default=5)
    score_type = models.CharField(max_length=50, default="cosine")
    latency_ms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class ChatbotRetrievedChunk(models.Model):
    retriever_event = models.ForeignKey(ChatbotRetrivalEvent, on_delete=models.CASCADE)
    rank = models.IntegerField()
    doc_id = models.CharField(max_length=255)
    chunk_id = models.CharField(max_length=255)
    score = models.FloatField()
    used_in_context = models.BooleanField(default=False)


# ===== 고객 관련 =====
class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ("INDIVIDUAL", "Individual"),
        ("CORPORATE", "Corporate"),
    ]
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default="INDIVIDUAL")
    display_name = models.CharField(max_length=255)
    bank_location = models.ForeignKey(BankLocation, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default="ACTIVE")
    risk_segment = models.CharField(max_length=20, default="RETAIL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IndustryCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EducationLevel(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class HousingStatus(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CustomerPerson(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.BooleanField()  # 0/1 대신 BooleanField
    rrn = models.CharField(max_length=50, unique=True)
    mobile = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    account_number = models.CharField(max_length=50)
    account_amount = models.DecimalField(max_digits=15, decimal_places=2)
    education_level = models.ForeignKey(EducationLevel, null=True, on_delete=models.SET_NULL)
    housing_status = models.ForeignKey(HousingStatus, null=True, on_delete=models.SET_NULL)
    income_annual = models.DecimalField(max_digits=15, decimal_places=2)
    work_experience_years = models.IntegerField(null=True, blank=True)
    employment_type = models.ForeignKey(EmploymentType, null=True, on_delete=models.SET_NULL)
    industry_code = models.ForeignKey(IndustryCode, null=True, on_delete=models.SET_NULL)
    has_delinquency = models.BooleanField(default=False)
    credit_history_length = models.IntegerField(default=0)
    credit_rating = models.IntegerField()


class CustomerCorporate(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    industry_code = models.ForeignKey(IndustryCode, null=True, on_delete=models.SET_NULL)
    legal_name = models.CharField(max_length=255, unique=True)
    biz_reg_no_masked = models.CharField(max_length=50, unique=True)
    incorporation_date = models.DateField()
    employees_count = models.IntegerField()
    mobile = models.CharField(max_length=50)
    roa = models.DecimalField(max_digits=10, decimal_places=2)
    net_profit_margin = models.DecimalField(max_digits=10, decimal_places=2)
    operating_roa = models.DecimalField(max_digits=10, decimal_places=2)
    operating_margin = models.DecimalField(max_digits=10, decimal_places=2)
    current_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    quick_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    debt_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    equity_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    equity_to_debt_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    long_term_debt_to_equity_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    asset_turnover = models.DecimalField(max_digits=10, decimal_places=2)
    receivables_turnover = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_turnover = models.DecimalField(max_digits=10, decimal_places=2)
    approval = models.IntegerField(default=0)  # 0=거절, 1=심사중, 2=승인


# ===== 문서 =====
class Document(models.Model):
    DOC_TYPE_CHOICES = [
        ("PDF", "PDF"),
        ("REPORT", "Report"),
    ]
    title = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    storage_path = models.CharField(max_length=512)
    mime_type = models.CharField(max_length=100, default="application/pdf")
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default="PDF")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class DocumentBinding(models.Model):
    BIND_TYPE_CHOICES = [
        ("CHAT", "Chat"),
        ("REVIEW", "Review"),
    ]
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    bind_type = models.CharField(max_length=20, choices=BIND_TYPE_CHOICES)
    bind_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
