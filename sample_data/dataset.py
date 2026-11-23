"""
Dataset of job offers, recruitment emails, and scam messages for training
and heuristic validation. Curated based on FTC, IC3, and academic job scam corpora.
"""

TRAINING_DATA = [
    # --- SCAM EXAMPLES (label: 1) ---
    (
        "Congratulations! You have been selected for the position of Remote Data Entry Clerk. "
        "The pay is $65 per hour. No prior experience is required. We will send you a certified cashier's "
        "check for $3,500 to purchase your home office equipment and laptop from our approved vendor. "
        "Deposit the check in your bank account, deduct $500 for your advance salary, and wire the remaining "
        "funds via Zelle or Bitcoin to the equipment supplier.",
        1
    ),
    (
        "Dear Applicant, your resume on Indeed has been reviewed by our HR Department and you are shortlisted. "
        "The interview will be conducted via Telegram app. Please download Telegram and message our hiring manager "
        "Dr. Robert Evans at @Evans_Recruiter immediately for the briefing. Salary is $50/hour, 15 hours a week.",
        1
    ),
    (
        "URGENT EMPLOYMENT OFFER: You have been hired on the spot as an Online Assistant. "
        "To confirm your slot, a mandatory background verification and training registration fee of $199 is required. "
        "This fee is 100% refundable after 30 days of employment. Pay via Western Union or CashApp to secure your spot.",
        1
    ),
    (
        "Google Recruitment Team is pleased to offer you the position of Junior Executive. "
        "Work from home, salary $4,500 weekly. You will receive an equipment check. Please reply with your full name, "
        "home address, direct phone number, and Social Security Number (SSN) along with your bank routing number "
        "so we can set up direct deposit before the interview.",
        1
    ),
    (
        "Hello! I am Linda from Apex Global Solutions. We have reviewed your profile and want to offer you a flexible "
        "part-time remote job. Earn $300 to $800 daily by simply rating apps and completing tasks on our portal. "
        "Contact me on WhatsApp at +1-987-654-3210 to start immediately.",
        1
    ),
    (
        "JOB OFFER LETTER: Dear candidate, you are appointed as Customer Care Associate. "
        "Accept this offer within 24 hours or it will be revoked. A check of $4,200 will be delivered to your address "
        "by FedEx. Once deposited, buy Apple gift cards or cryptocurrency and send the redemption codes to our vendor.",
        1
    ),
    (
        "Earn $5,000 every week working just 2 hours a day from the comfort of your home! "
        "No skills or interview required. Guaranteed placement for everyone. Send your registration fee of $75 to get started.",
        1
    ),
    (
        "Dear Jobseeker, we saw your CV on LinkedIn. We are impressed by your profile. "
        "The interview is scheduled right now on Skype chat (text only). No voice or video required. "
        "You will be paid $70 per hour for basic typing work.",
        1
    ),
    (
        "Offer of Employment at Amazon Logistics. Note: Due to corporate security protocols, "
        "all communication must be handled via personal email hr.amazoncareers2024@gmail.com and WhatsApp. "
        "Do not contact our corporate offices directly.",
        1
    ),
    (
        "Congratulations! You are selected for a paid summer internship. Stipend: $6,000/month. "
        "To receive your offer letter and welcome kit, deposit the mandatory processing and onboarding fee "
        "of $250 through cryptocurrency or MoneyGram within 48 hours.",
        1
    ),
    (
        "Mystery Shopper / Secret Evaluator wanted! We will mail you a check for $2,800. "
        "Cash it at your local bank, keep $400 for your commission, and test Walmart or Western Union by wiring "
        "the remaining $2,400 to our regional agent.",
        1
    ),
    (
        "Exclusive opportunity: Work as a financial package forwarding agent. "
        "Receive packages at your residential address, repackage them, and ship them overseas. "
        "No experience needed. Quick payout via crypto wallet or wire transfer.",
        1
    ),
    (
        "Dear Candidate, You have been selected without interview due to urgent vacancy. "
        "Kindly forward your photo ID, SSN, copy of passport, and mother's maiden name to hr-department@mail.com "
        "for instant payroll generation.",
        1
    ),
    (
        "Remote Proofreader / Copy Editor. $80/hr. Full equipment provided via check. "
        "Must be willing to purchase specialized software licenses using our vendor check before commencing work.",
        1
    ),
    (
        "Hi! Good news! You passed our initial screening for remote assistant. "
        "Download Signal or Telegram and text our manager immediately. The position must be filled today or the vacancy closes.",
        1
    ),

    # --- LEGITIMATE EXAMPLES (label: 0) ---
    (
        "Dear Alex, Following our series of technical and managerial interviews, "
        "we are delighted to offer you the position of Software Development Engineer I at Stripe. "
        "Your annual base salary will be $135,000, along with equity grants and comprehensive healthcare benefits. "
        "Please review the formal offer letter on our Workday portal and sign by Friday, November 28.",
        0
    ),
    (
        "We are pleased to extend an offer for the Summer 2025 Software Engineering Internship at Microsoft. "
        "This is a 12-week program located in Redmond, WA. You will receive a competitive monthly stipend, "
        "intern housing stipend, and relocation support. Our university recruiting team will guide you through "
        "the background check process managed by our third-party partner HireRight.",
        0
    ),
    (
        "Dear Candidate, Thank you for taking the time to speak with our engineering team last week. "
        "We were very impressed by your problem-solving skills in the system design round. We would love to welcome you "
        "as a Frontend Developer at Datadog. Attached is your official employment agreement detailing compensation, "
        "401(k) matching, and PTO policy. Please reach out to your recruiter if you have any questions.",
        0
    ),
    (
        "Job Description: Junior Data Analyst. Responsibilities: Clean and analyze marketing datasets using SQL and Python; "
        "build dashboards in Tableau; collaborate with cross-functional product teams. Qualifications: Bachelor's degree in "
        "Computer Science, Statistics, or related quantitative field. Strong knowledge of relational databases. "
        "Apply directly on our careers page at https://careers.airbnb.com.",
        0
    ),
    (
        "Thank you for interviewing for the Product Marketing Manager role at Spotify. "
        "We are excited to move forward with an offer. Our compensation package includes competitive base pay, "
        "annual bonus incentive, flexible working arrangement, and wellness benefits. You will receive an onboarding "
        "email from Greenhouse with your digital signature link.",
        0
    ),
    (
        "Acme Corp is hiring a remote Customer Support Specialist. Starting pay is $22 to $25 per hour based on experience. "
        "Requirements: Excellent written communication skills, experience with Zendesk or similar ticketing systems, "
        "and a quiet home work environment. Standard hardware will be shipped directly from our IT department. "
        "Interviews will be held via Zoom video with our team lead.",
        0
    ),
    (
        "Dear Priya, On behalf of Accenture, I am pleased to offer you the role of Associate Software Engineer. "
        "Your joining location will be Bangalore. Please submit your degree transcripts and employment verification documents "
        "through the official Accenture candidate portal. Never share financial credentials or pay any fees for recruitment.",
        0
    ),
    (
        "Role: DevOps Engineer (Kubernetes, AWS, Terraform). Company: CloudTech Innovations. "
        "We are looking for an engineer with 2+ years of production experience in container orchestration, CI/CD pipelines, "
        "and cloud infrastructure as code. Competitive salary $110,000-$130,000 + stock options. "
        "Two technical interview rounds including a hands-on coding session.",
        0
    ),
    (
        "Internship Offer: Research Intern in Machine Learning. Location: Boston, MA. "
        "Duration: 6 months. You will work alongside our research scientists publishing at top-tier conferences (NeurIPS, ICML). "
        "Requirements: Proficiency in PyTorch, solid math foundation, prior research experience preferred. "
        "Formal offer letter sent via DocuSign.",
        0
    ),
    (
        "We are glad to offer you employment as an Account Executive at Salesforce. "
        "Your start date is planned for January 15. The role includes a competitive base plus commission structure, "
        "health insurance, and employee stock purchase plan (ESPP). All onboarding documentation will be handled via Workday.",
        0
    ),
    (
        "Job Opportunity: Administrative Coordinator. City of Austin Public Works. "
        "Salary: $48,000 - $55,000/year. Full state government benefits, pension plan, and paid sick leave. "
        "Candidates must pass standard background check. Apply via official government portal at austintexas.gov/jobs.",
        0
    ),
    (
        "Thank you for attending the onsite interview loop yesterday. The hiring committee has reviewed your feedback "
        "and approved the offer for Senior Backend Engineer (Go/Distributed Systems). Let us schedule a 15-minute call "
        "with our VP of Engineering to discuss the details and team placement.",
        0
    )
]

SAMPLE_OFFERS = {
    "fake_check": {
        "title": "Fake Check & Equipment Scam (High Risk)",
        "company": "Apex Global Logistics Inc.",
        "email": "hr.apexlogistics@gmail.com",
        "text": (
            "Congratulations! Following your resume submission, you have been selected for the position of "
            "Remote Data Entry & Administrative Assistant at Apex Global Logistics. The starting pay is $65.00 per hour, "
            "working 20 to 25 hours per week with full flexibility.\n\n"
            "Because this is a remote position, you will be required to set up a home office. Our company will issue "
            "you a certified Cashier's Check of $3,850.00 to cover the purchase of an Apple MacBook Pro, laser printer, "
            "and time-tracking software from our certified vendor. Once you receive the check, deposit it into your bank "
            "account, deduct $500 as your signing bonus, and immediately transfer the balance of $3,350 via Zelle or "
            "Bitcoin to our logistics supplier to deliver your workstation.\n\n"
            "Please confirm your physical mailing address and bank name so we can courier your payment immediately."
        )
    },
    "telegram_interview": {
        "title": "Telegram Interview / Impersonation Scam (High Risk)",
        "company": "Google LLC",
        "email": "google-recruiting-desk@outlook.com",
        "text": (
            "Dear Candidate,\n\n"
            "We have reviewed your profile on LinkedIn/Indeed and found your qualifications suitable for the "
            "position of Junior Remote Software Tester. The salary is $55.00/hour with immediate commencement.\n\n"
            "Due to high applicant volume, the preliminary interview will be conducted via Telegram Instant Messenger. "
            "Download Telegram from the app store and add our Senior Talent Acquisition Director Mr. David Vance "
            "via username @GoogleHR_DavidVance. Message him your verification code #GOOG-9021 to commence your interview.\n\n"
            "Note: This vacancy is strictly confidential and closes within 24 hours. Do not contact Google offices directly."
        )
    },
    "internship_fee": {
        "title": "Paid Internship with Mandatory Training Fee (High Risk)",
        "company": "NextGen Innovations Tech",
        "email": "careers@nextgen-tech-interns.site",
        "text": (
            "Subject: Formal Internship Selection Letter - Software Engineering\n\n"
            "Congratulations! You have been selected for the 3-month Summer Internship Program at NextGen Innovations. "
            "You will receive a guaranteed monthly stipend of $4,500.\n\n"
            "To confirm your seat, all selected students must complete the mandatory Cloud Onboarding & DevOps toolchain "
            "certification. A nominal refundable security deposit and server allocation fee of $199 must be paid before "
            "your offer letter is counter-signed. This amount will be 100% refunded in your first paycheck.\n\n"
            "Make payment via CashApp or Western Union within 48 hours to lock your position."
        )
    },
    "suspicious_remote": {
        "title": "Ambiguous Remote Role with Free Email (Moderate Risk)",
        "company": "Horizon Media Partners",
        "email": "recruiting.horizonmedia@yahoo.com",
        "text": (
            "Hello,\n\n"
            "We are seeking an energetic individual to join our growing media firm as a Remote Content Assistant. "
            "The position pays $32/hour for simple online research, scheduling social media posts, and answering emails. "
            "Hours are flexible (10-15 hrs/week). No technical background or previous experience is needed.\n\n"
            "If interested, please email back your updated resume and phone number. We will send you an employment form "
            "to begin right away without complicated interview rounds."
        )
    },
    "legitimate_offer": {
        "title": "Legitimate Tech Company Offer Letter (Low Risk / Safe)",
        "company": "Stripe, Inc.",
        "email": "recruiting@stripe.com",
        "text": (
            "Dear Alex Morgan,\n\n"
            "On behalf of Stripe, Inc., I am delighted to extend an offer of employment for the position of "
            "Software Engineer - Platform Infrastructure, reporting to Sarah Jenkins, Engineering Director.\n\n"
            "Compensation details:\n"
            "- Base Salary: $140,000 annualized, paid semi-monthly\n"
            "- Sign-on Bonus: $15,000\n"
            "- Equity Grant: $120,000 in Restricted Stock Units (RSUs) vesting over 4 years\n"
            "- Comprehensive health, dental, and vision insurance\n"
            "- 401(k) retirement plan with 50% company match up to 6%\n\n"
            "This offer is contingent upon successful completion of a standard background verification conducted by "
            "our partner HireRight. You will receive an invitation to access our official Workday candidate portal where "
            "you can electronically sign your offer agreement and review our employee handbook.\n\n"
            "Please review and sign by Friday, December 5th. We look forward to welcoming you to the Stripe team!\n\n"
            "Sincerely,\n"
            "Marcus Chen\n"
            "Senior Technical Recruiter | Stripe, Inc."
        )
    }
}
