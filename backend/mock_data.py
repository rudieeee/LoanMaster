# Customer Database - 12 synthetic customer profiles
customers = {
    "12345": {
        "id": "12345",
        "name": "Rajesh Kumar",
        "age": 32,
        "city": "Delhi",
        "phone": "9876543210",
        "email": "rajesh.kumar@email.com",
        "credit_score": 750,
        "pre_approved_limit": 500000,
        "salary": 80000,
        "existing_loans": 150000,
        "kyc_status": "verified",
        "pan": "ABCDE1234F",
        "aadhaar": "1234-5678-9012"
    },
    "67890": {
        "id": "67890", 
        "name": "Priya Sharma",
        "age": 28,
        "city": "Mumbai",
        "phone": "9123456789",
        "email": "priya.sharma@email.com",
        "credit_score": 820,
        "pre_approved_limit": 800000,
        "salary": 120000,
        "existing_loans": 0,
        "kyc_status": "verified",
        "pan": "FGHIJ5678K",
        "aadhaar": "2345-6789-0123"
    },
    "11111": {
        "id": "11111",
        "name": "Amit Patel",
        "age": 35,
        "city": "Ahmedabad",
        "phone": "9988776655",
        "email": "amit.patel@email.com",
        "credit_score": 680,
        "pre_approved_limit": 300000,
        "salary": 60000,
        "existing_loans": 200000,
        "kyc_status": "verified",
        "pan": "KLMNO9012P",
        "aadhaar": "3456-7890-1234"
    },
    "22222": {
        "id": "22222",
        "name": "Sneha Reddy",
        "age": 26,
        "city": "Hyderabad",
        "phone": "9887766554",
        "email": "sneha.reddy@email.com",
        "credit_score": 850,
        "pre_approved_limit": 1000000,
        "salary": 150000,
        "existing_loans": 50000,
        "kyc_status": "verified",
        "pan": "QRSTU3456V",
        "aadhaar": "4567-8901-2345"
    },
    "33333": {
        "id": "33333",
        "name": "Vikram Singh",
        "age": 40,
        "city": "Bangalore",
        "phone": "9776655443",
        "email": "vikram.singh@email.com",
        "credit_score": 650,
        "pre_approved_limit": 200000,
        "salary": 55000,
        "existing_loans": 300000,
        "kyc_status": "pending",
        "pan": "WXYZ7890A",
        "aadhaar": "5678-9012-3456"
    },
    "44444": {
        "id": "44444",
        "name": "Ananya Iyer",
        "age": 29,
        "city": "Chennai",
        "phone": "9665544332",
        "email": "ananya.iyer@email.com",
        "credit_score": 780,
        "pre_approved_limit": 600000,
        "salary": 95000,
        "existing_loans": 100000,
        "kyc_status": "verified",
        "pan": "BCDEF1234G",
        "aadhaar": "6789-0123-4567"
    },
    "55555": {
        "id": "55555",
        "name": "Rahul Verma",
        "age": 33,
        "city": "Pune",
        "phone": "9554433221",
        "email": "rahul.verma@email.com",
        "credit_score": 720,
        "pre_approved_limit": 450000,
        "salary": 75000,
        "existing_loans": 180000,
        "kyc_status": "verified",
        "pan": "GHIJK5678L",
        "aadhaar": "7890-1234-5678"
    },
    "66666": {
        "id": "66666",
        "name": "Kavya Nair",
        "age": 31,
        "city": "Kochi",
        "phone": "9443322110",
        "email": "kavya.nair@email.com",
        "credit_score": 800,
        "pre_approved_limit": 700000,
        "salary": 110000,
        "existing_loans": 0,
        "kyc_status": "verified",
        "pan": "MNOPQ9012R",
        "aadhaar": "8901-2345-6789"
    },
    "77777": {
        "id": "77777",
        "name": "Arjun Mehta",
        "age": 38,
        "city": "Jaipur",
        "phone": "9332211009",
        "email": "arjun.mehta@email.com",
        "credit_score": 630,
        "pre_approved_limit": 150000,
        "salary": 48000,
        "existing_loans": 250000,
        "kyc_status": "verified",
        "pan": "STUVW3456X",
        "aadhaar": "9012-3456-7890"
    },
    "88888": {
        "id": "88888",
        "name": "Meera Desai",
        "age": 27,
        "city": "Surat",
        "phone": "9221100998",
        "email": "meera.desai@email.com",
        "credit_score": 760,
        "pre_approved_limit": 550000,
        "salary": 88000,
        "existing_loans": 120000,
        "kyc_status": "verified",
        "pan": "YZABC7890D",
        "aadhaar": "0123-4567-8901"
    },
    "99999": {
        "id": "99999",
        "name": "Karthik Ramesh",
        "age": 34,
        "city": "Coimbatore",
        "phone": "9110099887",
        "email": "karthik.ramesh@email.com",
        "credit_score": 810,
        "pre_approved_limit": 750000,
        "salary": 125000,
        "existing_loans": 75000,
        "kyc_status": "verified",
        "pan": "DEFGH1234I",
        "aadhaar": "1234-5678-9012"
    },
    "00000": {
        "id": "00000",
        "name": "Divya Krishnan",
        "age": 25,
        "city": "Trivandrum",
        "phone": "9009988776",
        "email": "divya.krishnan@email.com",
        "credit_score": 690,
        "pre_approved_limit": 350000,
        "salary": 65000,
        "existing_loans": 80000,
        "kyc_status": "pending",
        "pan": "IJKLM5678N",
        "aadhaar": "2345-6789-0123"
    }
}

# CRM Server - KYC Verification Data
kyc_database = {
    "verified": ["12345", "67890", "11111", "22222", "44444", "55555", "66666", "77777", "88888", "99999"],
    "pending": ["33333", "00000"],
    "rejected": []
}

# Credit Bureau API - Credit Score Data (out of 900)
credit_bureau = {
    "12345": {"score": 750, "last_updated": "2025-10-01", "status": "good"},
    "67890": {"score": 820, "last_updated": "2025-10-05", "status": "excellent"},
    "11111": {"score": 680, "last_updated": "2025-09-28", "status": "fair"},
    "22222": {"score": 850, "last_updated": "2025-10-10", "status": "excellent"},
    "33333": {"score": 650, "last_updated": "2025-09-15", "status": "poor"},
    "44444": {"score": 780, "last_updated": "2025-10-03", "status": "good"},
    "55555": {"score": 720, "last_updated": "2025-09-25", "status": "good"},
    "66666": {"score": 800, "last_updated": "2025-10-08", "status": "excellent"},
    "77777": {"score": 630, "last_updated": "2025-09-20", "status": "poor"},
    "88888": {"score": 760, "last_updated": "2025-10-02", "status": "good"},
    "99999": {"score": 810, "last_updated": "2025-10-07", "status": "excellent"},
    "00000": {"score": 690, "last_updated": "2025-09-30", "status": "fair"}
}

# Offer Management System - Pre-approved Loan Offers
loan_offers = {
    "personal_loan": {
        "min_amount": 50000,
        "max_amount": 2000000,
        "min_tenure": 12,
        "max_tenure": 60,
        "interest_rate_range": {
            "excellent": 10.5,  # Credit score 800+
            "good": 11.5,       # Credit score 700-799
            "fair": 13.5,       # Credit score 650-699
            "poor": 15.5        # Credit score < 650
        }
    },
    "home_loan": {
        "min_amount": 500000,
        "max_amount": 10000000,
        "min_tenure": 60,
        "max_tenure": 240,
        "interest_rate": 8.5
    },
    "car_loan": {
        "min_amount": 100000,
        "max_amount": 2000000,
        "min_tenure": 12,
        "max_tenure": 84,
        "interest_rate": 9.5
    }
}

# File Upload System - Simulated Salary Slip Verification
salary_slips = {
    "12345": {"verified": True, "salary": 80000, "company": "Tech Corp"},
    "67890": {"verified": True, "salary": 120000, "company": "Finance Ltd"},
    "11111": {"verified": False, "salary": 60000, "company": "Unknown"},
    "22222": {"verified": True, "salary": 150000, "company": "IT Solutions"},
    "33333": {"verified": False, "salary": 55000, "company": "Unknown"},
    "44444": {"verified": True, "salary": 95000, "company": "Consulting Inc"},
    "55555": {"verified": True, "salary": 75000, "company": "Marketing Co"},
    "66666": {"verified": True, "salary": 110000, "company": "Healthcare Ltd"},
    "77777": {"verified": False, "salary": 48000, "company": "Unknown"},
    "88888": {"verified": True, "salary": 88000, "company": "Retail Corp"},
    "99999": {"verified": True, "salary": 125000, "company": "Engineering Ltd"},
    "00000": {"verified": False, "salary": 65000, "company": "Unknown"}
}

# Approval Rules
APPROVAL_RULES = {
    "min_credit_score": 700,
    "max_emi_to_salary_ratio": 0.50,  # 50% of salary
    "instant_approval_multiplier": 1.0,  # <= pre-approved limit
    "conditional_approval_multiplier": 2.0  # <= 2× pre-approved limit
}
