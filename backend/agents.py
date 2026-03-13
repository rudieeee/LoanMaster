import random
import json
from datetime import datetime
from mock_data import customers, loan_offers, kyc_database, credit_bureau, salary_slips, APPROVAL_RULES
from blockchain import loan_blockchain


class SalesAgent:
    """Handles loan negotiation and understands customer needs"""
    
    def negotiate_loan(self, customer_data, requested_amount, tenure):
        customer_name = customer_data.get("name", "Customer")
        pre_approved = customer_data.get("pre_approved_limit", 0)
        credit_score = customer_data.get("credit_score", 0)
        salary = customer_data.get("salary", 0)
        
        # Determine interest rate based on credit score
        if credit_score >= 800:
            interest_rate = 10.5
            rate_category = "excellent"
            rate_pitch = "your outstanding credit score has earned you our *best rate*"
        elif credit_score >= 700:
            interest_rate = 11.5
            rate_category = "good"
            rate_pitch = "your solid credit history qualifies you for a *great rate*"
        elif credit_score >= 650:
            interest_rate = 13.5
            rate_category = "fair"
            rate_pitch = "I've secured you a *competitive rate* based on your profile"
        else:
            interest_rate = 15.5
            rate_category = "poor"
            rate_pitch = "I understand this rate might seem high, but here's the good news - after 6 months of timely payments, we can review and potentially lower it"
        
        # Calculate EMI
        monthly_rate = interest_rate / (12 * 100)
        emi = (requested_amount * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
        
        # Calculate EMI to salary ratio for persuasive messaging
        emi_ratio = (emi / salary * 100) if salary > 0 else 0
        
        # Personalized opening based on amount vs pre-approved
        if requested_amount <= pre_approved:
            opening = f"Excellent news, {customer_name}! 🎉 I love what you're doing here. ₹{requested_amount:,} for {tenure} months - that's well within your pre-approved limit of ₹{pre_approved:,}. This is going to be smooth sailing!"
        elif requested_amount <= pre_approved * 1.5:
            opening = f"Alright {customer_name}, I see you're thinking bigger - ₹{requested_amount:,} is a bit above your pre-approved ₹{pre_approved:,}, but you know what? I think we can make this work! Let me show you what I can do..."
        elif requested_amount <= pre_approved * 2:
            opening = f"I appreciate your ambition, {customer_name}! ₹{requested_amount:,} is definitely stretching beyond your pre-approved ₹{pre_approved:,}, but hey - I'm here to help you get what you need. Let's explore this together..."
        else:
            alternative_amount = int(pre_approved * 1.8)
            opening = f"Okay {customer_name}, I'll be straight with you - ₹{requested_amount:,} is quite a jump from your pre-approved ₹{pre_approved:,}. But before you worry, let me show you something that might actually work better for you..."
        
        response = f"{opening}\n\n"
        response += f"📊 **Here's what I've crafted for you:**\n\n"
        response += f"💰 **Loan Amount:** ₹{requested_amount:,}\n"
        response += f"📅 **Tenure:** {tenure} months ({tenure//12} year{'s' if tenure > 12 else ''})\n"
        response += f"💳 **Interest Rate:** {interest_rate}% per annum\n"
        response += f"   *({rate_pitch})*\n\n"
        response += f"📈 **Your Monthly EMI:** ₹{emi:,.2f}\n"
        
        # Personalized EMI commentary
        if emi_ratio < 30:
            response += f"   *That's just {emi_ratio:.1f}% of your monthly income - very comfortable! 👍*\n"
        elif emi_ratio < 40:
            response += f"   *About {emi_ratio:.1f}% of your income - manageable and sustainable.*\n"
        elif emi_ratio < 50:
            response += f"   *This is {emi_ratio:.1f}% of your income - a bit on the higher side, but doable.*\n"
        else:
            response += f"   *I notice this would be {emi_ratio:.1f}% of your income - let me suggest a better option below.*\n"
        
        response += f"\n💵 **Total Repayment:** ₹{emi * tenure:,.2f}\n"
        response += f"   *Interest component: ₹{(emi * tenure) - requested_amount:,.2f}*\n\n"
        
        # Smart recommendations and persuasion
        if requested_amount <= pre_approved:
            response += "✨ **Why this is perfect for you:**\n"
            response += "• ⚡ Instant approval - no extra paperwork needed\n"
            response += "• 🎯 Pre-approved means you're already qualified\n"
            response += "• 💨 Money in your account within 24 hours\n"
            response += "• 🎁 Special processing fee waiver for pre-approved customers\n\n"
            response += "Honestly? This is as good as it gets. Shall we lock this in? 😊"
        elif requested_amount <= pre_approved * 1.5:
            response += "✨ **Here's the deal:**\n"
            response += "• 📋 Just need to verify your latest salary slips (takes 30 mins)\n"
            response += "• ✅ Your credit score is strong enough to support this\n"
            response += "• 🚀 We can still get you approved today\n\n"
            response += "💡 **My honest advice?** Go for it! You deserve this upgrade. What do you say?"
        elif requested_amount <= pre_approved * 2:
            response += "⚠️ **Real talk:** This is stretching it, but I believe in finding solutions!\n\n"
            alternative_amount = int(pre_approved * 1.5)
            alt_emi = (alternative_amount * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
            response += f"🤔 **Two options for you:**\n\n"
            response += f"**Option A (Recommended):** ₹{alternative_amount:,}\n"
            response += f"   • Monthly EMI: ₹{alt_emi:,.2f}\n"
            response += f"   • Faster approval\n"
            response += f"   • Lower interest rate possible\n"
            response += f"   • You can always top-up later!\n\n"
            response += f"**Option B (Challenging):** ₹{requested_amount:,}\n"
            response += f"   • Needs 3 months salary slips + bank statements\n"
            response += f"   • 2-3 days approval time\n"
            response += f"   • Might need a co-applicant\n\n"
            response += "💭 Between you and me? Option A gets you the money faster and keeps your EMI comfortable. But I'm here to support whatever you choose!"
        else:
            max_amount = int(pre_approved * 2)
            max_emi = (max_amount * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
            response += f"❌ **Here's where I need to be honest with you, {customer_name}...**\n\n"
            response += f"₹{requested_amount:,} is beyond what I can approve right now. I know that's not what you wanted to hear, but let me show you what I *can* do:\n\n"
            response += f"💎 **Best alternative - ₹{max_amount:,}:**\n"
            response += f"   • Monthly EMI: ₹{max_emi:,.2f}\n"
            response += f"   • Instant approval guaranteed\n"
            response += f"   • Better interest rate\n"
            response += f"   • After 6 months of good repayment, we can review for a top-up!\n\n"
            response += f"🎯 **Smart strategy:** Many of my clients take ₹{max_amount:,} now, build a great repayment history, and then we top them up to their desired amount in 6 months at an even *better* rate!\n\n"
            response += "Think about it - ₹{max_amount:,} in your hands tomorrow vs waiting weeks for a maybe. What makes more sense for you? 🤔"
        
        return {
            "message": response,
            "data": {
                "interest_rate": interest_rate,
                "emi": round(emi, 2),
                "total_repayment": round(emi * tenure, 2),
                "rate_category": rate_category,
                "requested_amount": requested_amount,
                "pre_approved": pre_approved
            }
        }


class VerificationAgent:
    """Validates customer KYC details"""
    
    def verify_kyc(self, customer_id, customer_data):
        customer_name = customer_data.get("name", "Customer")
        kyc_status = customer_data.get("kyc_status", "unknown")
        pan = customer_data.get("pan", "N/A")
        aadhaar = customer_data.get("aadhaar", "N/A")
        
        if customer_id in kyc_database["verified"]:
            response = f"✅ **Perfect! Your documents are all good, {customer_name}!**\n\n"
            response += f"I just cross-checked everything and you're verified! 🎯\n\n"
            response += f"**What I confirmed:**\n"
            response += f"• PAN: {pan} ✓\n"
            response += f"• Aadhaar: {aadhaar} ✓\n"
            response += f"• Address: Verified ✓\n\n"
            response += "This is great - no hiccups here! Let me now check your credit profile to get you the best possible terms... ⏱️"
            
            return {
                "verified": True,
                "message": response,
                "details": {
                    "pan": pan,
                    "aadhaar": aadhaar,
                    "status": "verified"
                }
            }
        
        elif customer_id in kyc_database["pending"]:
            response = f"⏳ **Okay {customer_name}, quick pause here...**\n\n"
            response += f"I'm seeing your KYC verification is still pending. Don't worry though - this is super common and easy to fix! 😊\n\n"
            response += f"**What I need from you:**\n"
            response += f"📄 Clear photo of your PAN Card\n"
            response += f"📄 Aadhaar or any address proof\n\n"
            response += f"💡 **Here's the thing:** Once you upload these, I can verify them in about 10-15 minutes and we'll be back on track. Most of my clients just snap a quick photo with their phone and we're done!\n\n"
            response += "Can you upload those now? Or would you prefer to come back when you have them handy? (I'll save your application, no worries!)"
            
            return {
                "verified": False,
                "message": response,
                "details": {
                    "status": "pending",
                    "reason": "KYC documents pending verification"
                }
            }
        
        else:
            response = f"❌ **Hmm, {customer_name}... I'm hitting a small roadblock here.**\n\n"
            response += f"I couldn't verify your identity with the information I have. This usually happens when:\n"
            response += f"• PAN or Aadhaar numbers might have a typo\n"
            response += f"• Documents are registered under a different name\n"
            response += f"• Details need to be updated in our system\n\n"
            response += f"🤝 **Let's fix this together:** Can you double-check your PAN ({pan}) and Aadhaar ({aadhaar}) and resend? Or if you prefer, I can connect you with our verification team who can sort this out on a quick call.\n\n"
            response += "What works better for you?"
            
            return {
                "verified": False,
                "message": response,
                "details": {
                    "status": "failed",
                    "reason": "Invalid or missing KYC information"
                }
            }


class UnderwritingAgent:
    """Performs credit assessment and applies approval logic"""
    
    def assess_creditworthiness(self, customer_id, customer_data, loan_amount, emi):
        customer_name = customer_data.get("name", "Customer")
        credit_score = customer_data.get("credit_score", 0)
        pre_approved_limit = customer_data.get("pre_approved_limit", 0)
        salary = customer_data.get("salary", 0)
        existing_loans = customer_data.get("existing_loans", 0)
        
        # Get credit bureau data
        bureau_data = credit_bureau.get(customer_id, {})
        bureau_score = bureau_data.get("score", credit_score)
        
        # Calculate EMI to salary ratio
        emi_ratio = (emi / salary) if salary > 0 else 1.0
        max_emi_ratio = APPROVAL_RULES["max_emi_to_salary_ratio"]
        
        # Apply approval logic
        decision = self._make_decision(
            loan_amount, pre_approved_limit, bureau_score, 
            emi_ratio, max_emi_ratio, customer_id
        )
        
        response = f"🔍 **Alright {customer_name}, let me walk you through what I found...**\n\n"
        response += f"I just pulled your credit report and ran the numbers. Here's the full picture:\n\n"
        response += f"**Your Credit Profile:**\n"
        response += f"• Credit Score: {bureau_score}/900 "
        
        # Add encouraging commentary based on score
        if bureau_score >= 800:
            response += "(*Wow, that's exceptional!* 🌟)\n"
        elif bureau_score >= 750:
            response += "(*That's really strong!* 💪)\n"
        elif bureau_score >= 700:
            response += "(*Pretty solid!* 👍)\n"
        elif bureau_score >= 650:
            response += "(*Room for improvement, but workable* 📈)\n"
        else:
            response += "(*This is our main challenge here* 😕)\n"
        
        response += f"• Monthly Income: ₹{salary:,}\n"
        response += f"• Proposed EMI: ₹{emi:,.2f} ({emi_ratio*100:.1f}% of income)\n"
        
        if existing_loans > 0:
            response += f"• Existing EMIs: ₹{existing_loans:,}\n"
            total_emi = emi + existing_loans
            total_ratio = (total_emi / salary * 100) if salary > 0 else 0
            response += f"• Total EMI Load: ₹{total_emi:,.2f} ({total_ratio:.1f}% of income)\n"
        
        response += f"• Pre-approved Limit: ₹{pre_approved_limit:,}\n\n"
        
        response += decision["message"]
        
        return {
            "approved": decision["approved"],
            "approval_type": decision["type"],
            "message": response,
            "details": decision["details"]
        }
    
    def _make_decision(self, loan_amount, pre_approved_limit, credit_score, 
                      emi_ratio, max_emi_ratio, customer_id):
        
        # Check minimum credit score
        if credit_score < APPROVAL_RULES["min_credit_score"]:
            gap = APPROVAL_RULES["min_credit_score"] - credit_score
            return {
                "approved": False,
                "type": "rejected",
                "message": f"❌ **Okay, I need to be real with you here...**\n\nYour credit score is {credit_score}, and our minimum requirement is {APPROVAL_RULES['min_credit_score']}. That's a gap of {gap} points.\n\n**But listen - this isn't the end!** 🌱\n\n💡 **Here's my advice as your loan advisor:**\n\n1. **Quick wins (30-60 days):**\n   • Pay all pending credit card bills immediately\n   • Clear any small outstanding dues\n   • Don't apply for new credit cards\n\n2. **Build it up (3-6 months):**\n   • Set up auto-payments for all EMIs\n   • Keep credit card usage below 30% of limit\n   • Check your credit report for errors (free on CIBIL)\n\n3. **Come back to me:**\n   Once you hit {APPROVAL_RULES['min_credit_score']}, I'll personally fast-track your application with even better rates!\n\n📞 Want me to connect you with our credit counseling team? They've helped tons of people improve scores in just 3 months!",
                "details": {
                    "reason": "Credit score too low",
                    "credit_score": credit_score,
                    "required_score": APPROVAL_RULES["min_credit_score"],
                    "gap": gap
                }
            }
        
        # Instant Approval: Amount <= pre-approved limit
        if loan_amount <= pre_approved_limit:
            return {
                "approved": True,
                "type": "instant",
                "message": f"✅ **YES! YES! YES! 🎉🎊**\n\nOkay {customer_id}, I'm absolutely thrilled to tell you this - **YOU'RE APPROVED!**\n\n🚀 **And here's the best part:** This is an *instant approval*! No waiting, no extra paperwork, no committees to convince!\n\n**Why? Because:**\n• Your credit score is solid ✓\n• The amount is within your pre-approved limit ✓\n• Your EMI ratio is comfortable ✓\n• Your documents are verified ✓\n\n💰 **What happens next:**\n1. I'm generating your sanction letter right now ⏱️\n2. Sign it digitally (takes 2 minutes)\n3. Money hits your account in 24 hours! 💸\n\n🎁 **Special bonus:** Since you're pre-approved, we're waiving the ₹{loan_amount * 0.01:,.0f} processing fee!\n\nReady to proceed? Let's get you that money! 🚀",
                "details": {
                    "approval_type": "instant",
                    "reason": "Within pre-approved limit",
                    "conditions": []
                }
            }
        
        # Conditional Approval: Amount <= 2× pre-approved limit
        elif loan_amount <= pre_approved_limit * APPROVAL_RULES["conditional_approval_multiplier"]:
            # Check EMI ratio
            if emi_ratio > max_emi_ratio:
                alternative_tenure = None
                for test_tenure in [36, 48, 60, 72]:
                    monthly_rate = 0.12 / 12  # assume 12% for calculation
                    test_emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** test_tenure) / ((1 + monthly_rate) ** test_tenure - 1)
                    test_ratio = test_emi / (emi_ratio * max_emi_ratio * test_emi)
                    if test_ratio <= max_emi_ratio:
                        alternative_tenure = test_tenure
                        break
                
                message = f"❌ **Okay, we've hit a snag, but I have solutions!**\n\n"
                message += f"The EMI of ₹{emi_ratio * 100:.1f}% of your income is above our {max_emi_ratio * 100}% comfort zone. I can't approve it like this because honestly? I don't want you struggling with payments.\n\n"
                message += f"🤔 **But here's what we CAN do:**\n\n"
                
                # Suggest reducing amount
                safe_amount = int(loan_amount * 0.7)
                message += f"**Option 1 (My Recommendation):** Take ₹{safe_amount:,} now\n"
                message += f"   • EMI will be super comfortable\n"
                message += f"   • Instant approval guaranteed\n"
                message += f"   • Top-up available after 6 months\n\n"
                
                # Suggest extending tenure if possible
                if alternative_tenure:
                    message += f"**Option 2:** Keep ₹{loan_amount:,} but extend to {alternative_tenure} months\n"
                    message += f"   • Brings EMI within your budget\n"
                    message += f"   • Still gets approved today\n"
                    message += f"   • You can prepay anytime after 6 EMIs\n\n"
                
                message += f"💭 **Real talk:** I've seen people overstretch and it's stressful. Option 1 keeps you financially healthy AND you still get most of what you need.\n\n"
                message += f"Which route feels right to you? Or want to explore other amounts?"
                
                return {
                    "approved": False,
                    "type": "rejected",
                    "message": message,
                    "details": {
                        "reason": "EMI ratio too high",
                        "emi_ratio": round(emi_ratio * 100, 2),
                        "max_allowed": max_emi_ratio * 100,
                        "alternative_amount": safe_amount,
                        "alternative_tenure": alternative_tenure
                    }
                }
            
            # Check salary slip verification
            salary_verification = salary_slips.get(customer_id, {})
            if not salary_verification.get("verified", False):
                return {
                    "approved": False,
                    "type": "pending",
                    "message": f"⏳ **So close! Just one quick thing...**\n\n"
                             f"Everything looks great on your application! Credit score ✓ EMI ratio ✓ Documents ✓\n\n"
                             f"**The only thing I need:** Your last 3 months' salary slips for final verification.\n\n"
                             f"🎯 **Why I need this:** You're going slightly above your pre-approved limit, so the bank needs to confirm your current income. It's purely procedural - takes me about 30 minutes to verify once you upload.\n\n"
                             f"📱 **Upload them here and I'll:**\n"
                             f"   • Verify within 30 minutes\n"
                             f"   • Get you instant approval\n"
                             f"   • Have money in your account by tomorrow\n\n"
                             f"Or if you're not near your payslips right now, I can save this application and send you a reminder later today. Your call! 😊",
                    "details": {
                        "approval_type": "conditional",
                        "reason": "Salary verification pending",
                        "required_documents": ["salary_slips", "bank_statements"]
                    }
                }
            
            return {
                "approved": True,
                "type": "conditional",
                "message": f"✅ **APPROVED! 🎉 (with a tiny asterisk)**\n\n"
                         f"Great news! Your loan of ₹{loan_amount:,} is **APPROVED**!\n\n"
                         f"**Here's what sealed the deal:**\n"
                         f"• Your salary slips checked out perfectly ✓\n"
                         f"• EMI is within your comfortable range ✓\n"
                         f"• Credit score meets our criteria ✓\n\n"
                         f"Now, I say 'conditional' only because you're going above your pre-approved limit. But honestly? All the hard stuff is done. Your salary verification came through clean, so this is basically a green light! 🚦\n\n"
                         f"**Next steps:**\n"
                         f"1. I'm generating your sanction letter now\n"
                         f"2. Review and e-sign it (2 mins)\n"
                         f"3. Money in your account within 48 hours!\n\n"
                         f"Excited for you! Let's finish this up! 🚀",
                "details": {
                    "approval_type": "conditional",
                    "reason": "Above pre-approved but within limits",
                    "conditions": ["salary_verified", "emi_acceptable"]
                }
            }
        
        # Rejection: Amount > 2× pre-approved limit
        else:
            max_eligible = int(pre_approved_limit * APPROVAL_RULES["conditional_approval_multiplier"])
            monthly_rate = 0.12 / 12
            tenure = 36  # assume 3 years
            max_emi = (max_eligible * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
            
            return {
                "approved": False,
                "type": "rejected",
                "message": f"❌ **Okay, let's have an honest conversation...**\n\n"
                         f"I really wish I could approve ₹{loan_amount:,} for you right now, but it's significantly beyond your current eligibility of ₹{max_eligible:,}. And I'll tell you why I can't push it through - because I genuinely care about your financial health.\n\n"
                         f"**But here's what I CAN do for you today:**\n\n"
                         f"💎 **Instant Approval - ₹{max_eligible:,}**\n"
                         f"   • Monthly EMI: ~₹{max_emi:,.2f}\n"
                         f"   • Approved in the next 5 minutes\n"
                         f"   • Money in your account tomorrow\n"
                         f"   • Better interest rate\n"
                         f"   • Zero processing fees\n\n"
                         f"🎯 **Smart strategy many clients use:**\n"
                         f"1. Take ₹{max_eligible:,} now (instant)\n"
                         f"2. Make 6-12 months of perfect payments\n"
                         f"3. Your limit automatically increases\n"
                         f"4. Top-up to your desired amount at BETTER rates\n\n"
                         f"💭 **Think about it:** ₹{max_eligible:,} in your hands tomorrow vs. waiting weeks/months for a 'maybe' on ₹{loan_amount:,}. Plus, you'll build a great credit history that opens bigger doors later!\n\n"
                         f"What do you think? Shall we go with ₹{max_eligible:,} and secure it right now? 🤝",
                "details": {
                    "reason": "Amount exceeds eligibility",
                    "requested_amount": loan_amount,
                    "max_eligible": max_eligible
                }
            }


class SanctionLetterGenerator:
    """Creates automated approval letters"""
    
    def generate_letter(self, customer_data, loan_details, approval_details):
        customer_name = customer_data.get("name", "Customer")
        customer_id = customer_data.get("id", "N/A")
        
        letter = f"📄 **LOAN SANCTION LETTER**\n"
        letter += "=" * 50 + "\n\n"
        letter += f"**Date:** {datetime.now().strftime('%B %d, %Y')}\n"
        letter += f"**Sanction Letter No:** SL{customer_id}{datetime.now().strftime('%Y%m%d')}\n\n"
        letter += f"**Dear {customer_name},**\n\n"
        letter += "We are pleased to inform you that your personal loan application has been **APPROVED**! 🎉\n\n"
        
        letter += "**LOAN DETAILS:**\n"
        letter += f"• Sanctioned Amount: ₹{loan_details['amount']:,}\n"
        letter += f"• Interest Rate: {loan_details['interest_rate']}% per annum\n"
        letter += f"• Loan Tenure: {loan_details['tenure']} months\n"
        letter += f"• Monthly EMI: ₹{loan_details['emi']:,.2f}\n"
        letter += f"• Processing Fee: ₹{loan_details['amount'] * 0.01:,.2f} (1%)\n\n"
        
        letter += "**DISBURSEMENT:**\n"
        letter += "• Funds will be credited to your account within 24-48 hours\n"
        letter += "• First EMI due date: " + (datetime.now().replace(day=1) if datetime.now().day < 15 else datetime.now().replace(month=datetime.now().month+1, day=1)).strftime('%B %d, %Y') + "\n\n"
        
        letter += "**TERMS & CONDITIONS:**\n"
        letter += "1. This sanction is valid for 30 days\n"
        letter += "2. Prepayment allowed after 6 EMIs with no charges\n"
        letter += "3. Late payment charges: 2% per month\n"
        letter += "4. Insurance premium: As applicable\n\n"
        
        letter += "**NEXT STEPS:**\n"
        letter += "1. Sign the loan agreement (sent separately)\n"
        letter += "2. Complete insurance formalities\n"
        letter += "3. Funds will be disbursed upon completion\n\n"
        
        letter += "Thank you for choosing LoanMaster! 🙏\n\n"
        letter += "For queries, contact: support@loanmaster.com\n"
        letter += "=" * 50
        
        return letter


class MasterAgent:
    """Main orchestrator that coordinates all specialized agents"""
    
    def __init__(self):
        self.current_customer = None
        self.current_customer_id = None
        self.conversation_state = "greeting"
        self.loan_application = {
            "amount": None,
            "tenure": None,
            "purpose": None,
            "interest_rate": None,
            "emi": None,
            "stage": "initial"
        }
        self.agents = {
            "sales": SalesAgent(),
            "verification": VerificationAgent(),
            "underwriting": UnderwritingAgent(),
            "sanction": SanctionLetterGenerator()
        }
        self.conversation_history = []
    
    def process_message(self, message, customer_id=None):
        """Main entry point for processing customer messages"""
        
        # Handle customer ID input
        if self.conversation_state == "awaiting_customer_id" or (customer_id and not self.current_customer_id):
            return self._handle_customer_id(message if not customer_id else customer_id)
        
        # If no customer is set, ask for ID
        if not self.current_customer:
            return self._request_customer_id()
        
        # Route to appropriate handler based on conversation state
        if self.conversation_state == "greeting_done":
            return self._handle_loan_inquiry(message)
        
        elif self.conversation_state == "awaiting_loan_amount":
            return self._handle_loan_amount(message)
        
        elif self.conversation_state == "awaiting_tenure":
            return self._handle_tenure(message)
        
        elif self.conversation_state == "sales_negotiation":
            return self._handle_sales_confirmation(message)
        
        elif self.conversation_state == "verification":
            return self._handle_verification()
        
        elif self.conversation_state == "underwriting":
            return self._handle_underwriting()
        
        elif self.conversation_state == "sanction":
            return self._generate_sanction_letter()
        
        elif self.conversation_state == "completed":
            return self._handle_post_completion(message)
        
        else:
            return self._handle_general_inquiry(message)
    
    def _request_customer_id(self):
        self.conversation_state = "awaiting_customer_id"
        return {
            "message": "Hey there! 👋 I'm Sarah from LoanMaster!\n\nThink of me as your personal loan advisor - I'm here to help you get the perfect loan with the best terms possible. I've helped hundreds of customers get approved, and I'm excited to work with you!\n\nTo get started, I'll need your Customer ID so I can pull up your profile and see what amazing offers I can get for you. 😊\n\n💡 **New here? Try these demo IDs:**\n• 12345 - Rajesh (excellent profile, you'll love what I can offer!)\n• 67890 - Priya (top-tier credit, instant approvals!)\n• 77777 - Arjun (needs some work, but I have solutions!)\n• 33333 - Vikram (quick doc upload needed)\n\nWhat's your Customer ID?",
            "agent": "Master Agent"
        }
    
    def _handle_customer_id(self, customer_id):
        customer_id = customer_id.strip()
        
        if customer_id in customers:
            self.current_customer_id = customer_id
            self.current_customer = customers[customer_id]
            self.conversation_state = "greeting_done"
            
            customer_name = self.current_customer.get("name", "Customer")
            city = self.current_customer.get("city", "")
            pre_approved = self.current_customer.get("pre_approved_limit", 0)
            credit_score = self.current_customer.get("credit_score", 0)
            
            # Personalized greeting based on credit profile
            if credit_score >= 750:
                greeting = f"Wow, {customer_name}! 🌟 I just pulled up your profile and I'm impressed!"
            elif credit_score >= 650:
                greeting = f"Great to meet you, {customer_name}! 😊 I've got your profile up and I see some good opportunities for you."
            else:
                greeting = f"Hey {customer_name}! 👋 Thanks for trusting me with this. I've reviewed your profile and I'm here to find the best solution for you."
            
            response = f"{greeting}\n\n"
            response += f"Calling in from {city}, nice! Let me quickly share what I see:\n\n"
            response += f"✨ **Your Pre-approved Limit:** ₹{pre_approved:,}\n"
            
            if credit_score >= 750:
                response += f"   *(With your {credit_score} credit score, this is conservative - we might be able to go higher!)*\n\n"
            elif credit_score >= 650:
                response += f"   *(Based on your {credit_score} credit score - solid foundation!)*\n\n"
            else:
                response += f"   *(Starting point based on your {credit_score} score - but we have options!)*\n\n"
            
            response += "🎯 **What I can help you with today:**\n"
            response += "• Personal loans (debt consolidation, medical, travel, weddings)\n"
            response += "• Home loans (buying that dream house!)\n"
            response += "• Car loans (upgrading your ride!)\n"
            response += "• Business loans (growing your venture!)\n\n"
            
            response += "So tell me, what brings you here today? Looking to apply for a loan, or just exploring options? I'm all ears! 😊"
            
            return {
                "message": response,
                "agent": "Master Agent"
            }
        else:
            return {
                "message": f"Hmm, I'm not finding Customer ID '{customer_id}' in my system. 🤔\n\nLet's try that again - could you double-check the ID? Sometimes there's a typo (happens to the best of us!).\n\n💡 **If you're testing, try these IDs:**\n• 12345 (Rajesh)\n• 67890 (Priya)\n• 77777 (Arjun)\n• 33333 (Vikram)\n\nWhat's the correct Customer ID?",
                "agent": "Master Agent"
            }
    
    def _handle_loan_inquiry(self, message):
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["yes", "loan", "need", "want", "apply", "interested", "sure", "ok", "okay"]):
            self.conversation_state = "awaiting_loan_amount"
            
            pre_approved = self.current_customer.get("pre_approved_limit", 0)
            customer_name = self.current_customer.get("name", "Customer")
            
            response = f"Perfect! I love the enthusiasm! 🎯\n\n"
            response += f"Alright {customer_name}, let's find you the perfect loan amount. Now, I want you to be honest with me - how much do you actually need?\n\n"
            response += f"💡 **Quick context:**\n"
            response += f"• Your pre-approved limit: ₹{pre_approved:,} (instant approval)\n"
            response += f"• Maximum I can stretch to: ₹{int(pre_approved * 2):,} (with some additional docs)\n"
            response += f"• Minimum loan: ₹50,000\n\n"
            response += f"Just type the amount you're thinking. You can write it as:\n"
            response += f"• Plain number: 500000\n"
            response += f"• In lakhs: 5 lakh or 5L\n"
            response += f"• With commas: 5,00,000\n\n"
            response += f"What amount are you looking at? 💰"
            
            return {
                "message": response,
                "agent": "Master Agent"
            }
        elif any(word in message_lower for word in ["no", "not sure", "maybe", "thinking"]):
            return {
                "message": f"No pressure at all! Take your time. 😊\n\nI'm here whenever you're ready. In the meantime, feel free to ask me anything:\n• What interest rates can you get?\n• What documents do you need?\n• How long does approval take?\n• What's the eligibility criteria?\n\nOr just say 'hi' when you're ready to explore loan options. I'll be right here! 🤝",
                "agent": "Master Agent"
            }
        else:
            return {
                "message": f"I'm here to help with whatever you need! Want to:\n\n• **Apply for a loan** → Just say 'yes' or 'apply'\n• **Learn about rates** → Ask me 'what are the interest rates?'\n• **Check eligibility** → Ask 'am I eligible?'\n• **Understand the process** → Ask 'how does it work?'\n\nWhat would you like to know? 😊",
                "agent": "Master Agent"
            }
    
    def _handle_loan_amount(self, message):
        try:
            # Extract number from message
            amount = self._extract_number(message)
            
            if amount < 50000:
                return {
                    "message": f"Hmm, ₹{amount:,} is below our minimum loan amount of ₹50,000.\n\nI get it though - sometimes you need a smaller amount. Here's what I can suggest:\n• Consider a personal loan of ₹50,000 (minimum) and only use what you need\n• Look into a credit card if you need flexibility with smaller amounts\n• Check out our pay-day advance program (if you're employed)\n\nWant to go with ₹50,000 instead, or would you prefer exploring other options? 🤔",
                    "agent": "Master Agent"
                }
            
            if amount > 2000000:
                return {
                    "message": f"Whoa! ₹{amount:,} - you're thinking big! I like it! 💪\n\nHere's the thing though - our maximum personal loan limit is ₹20,00,000. BUT don't give up yet!\n\n🎯 **Here's what I can do:**\n\n**Option 1:** Personal loan of ₹20,00,000 (process today)\n**Option 2:** Combine a personal loan + home equity loan (if you own property)\n**Option 3:** Connect you with our business loans team (if it's business-related)\n\nFor ₹20,00,000, shall we proceed? Or tell me more about why you need ₹{amount:,} - maybe I can suggest a better product! 💡",
                    "agent": "Master Agent"
                }
            
            self.loan_application["amount"] = amount
            self.conversation_state = "awaiting_tenure"
            
            pre_approved = self.current_customer.get("pre_approved_limit", 0)
            
            # Personalized response based on amount requested
            if amount <= pre_approved:
                enthusiasm = f"Love it! ₹{amount:,} is well within your comfort zone! 🎯"
            elif amount <= pre_approved * 1.5:
                enthusiasm = f"Great choice! ₹{amount:,} - slightly above your pre-approved limit, but totally doable! 💪"
            else:
                enthusiasm = f"Ambitious! ₹{amount:,} - that's a stretch, but let's see what I can work out for you! 🚀"
            
            response = f"{enthusiasm}\n\n"
            response += f"Now, here's an important question that'll affect your EMI - how long do you want to repay this?\n\n"
            response += f"🗓️ **Tenure Options:**\n\n"
            response += f"• **12 months** (1 year) - Higher EMI, but you're debt-free quickly!\n"
            response += f"• **24 months** (2 years) - Balanced approach, moderate EMI\n"
            response += f"• **36 months** (3 years) - Popular choice, comfortable EMI ⭐\n"
            response += f"• **48 months** (4 years) - Lower EMI, more breathing room\n"
            response += f"• **60 months** (5 years) - Lowest EMI, maximum flexibility\n\n"
            response += f"💡 **My tip:** Most customers love the 36-month option - it's the sweet spot between manageable EMIs and not being in debt forever!\n\n"
            response += f"What tenure feels right for you? (Just enter the number of months)"
            
            return {
                "message": response,
                "agent": "Master Agent"
            }
            
        except ValueError:
            return {
                "message": "Oops! I couldn't quite catch that number. 😅\n\nCould you type the loan amount again? You can write it as:\n• 500000\n• 5 lakh\n• 5L\n• 5,00,000\n\nWhat amount do you need?",
                "agent": "Master Agent"
            }
    
    def _handle_tenure(self, message):
        try:
            tenure = self._extract_number(message)
            
            if tenure < 12:
                return {
                    "message": f"I appreciate you wanting to clear this quickly, but {tenure} months is too short for us to process. 😅\n\nOur minimum tenure is 12 months. Even if you want to pay it off faster, you can always prepay after 6 EMIs with ZERO prepayment charges!\n\n💡 So my suggestion: Take 12 months, and if you get extra cash, prepay anytime. Best of both worlds!\n\nShall we go with 12 months?",
                    "agent": "Master Agent"
                }
            
            if tenure > 60:
                return {
                    "message": f"{tenure} months? That's {tenure//12} years - quite a long commitment!\n\nOur maximum tenure is 60 months (5 years). Honestly, stretching beyond 5 years means you'll end up paying a lot more in interest.\n\n🤔 **Let me ask you this:** Would 60 months work? That'll give you a pretty low EMI while keeping the total interest reasonable.\n\nOr if you want an even lower EMI, maybe we should look at reducing the loan amount slightly?\n\nWhat do you think?",
                    "agent": "Master Agent"
                }
            
            self.loan_application["tenure"] = tenure
            self.conversation_state = "sales_negotiation"
            
            # Invoke Sales Agent
            sales_result = self.agents["sales"].negotiate_loan(
                self.current_customer,
                self.loan_application["amount"],
                tenure
            )
            
            self.loan_application["interest_rate"] = sales_result["data"]["interest_rate"]
            self.loan_application["emi"] = sales_result["data"]["emi"]
            
            # Record loan application on blockchain
            try:
                loan_blockchain.add_loan_application(
                    customer_id=self.current_customer_id,
                    loan_amount=float(self.loan_application["amount"]),
                    loan_purpose=self.loan_application.get("purpose", "Personal loan"),
                    status="pending"
                )
            except Exception as e:
                print(f"Blockchain recording error: {e}")
            
            response = sales_result["message"]
            response += "\n\n" + "="*50 + "\n"
            response += "\n🎯 **So, what do you think?**\n\n"
            response += "I've laid it all out for you. This is probably the best deal I can craft for your situation. \n\n"
            response += "Ready to move forward? Just say:\n"
            response += "• **'Yes'** or **'Let's do it'** → I'll process this immediately\n"
            response += "• **'Change amount'** → We'll adjust the loan amount\n"
            response += "• **'Different tenure'** → We'll try another tenure\n"
            response += "• **'Let me think'** → I'll save this for you\n\n"
            response += "What's it going to be? 😊"
            
            return {
                "message": response,
                "agent": "Sales Agent"
            }
            
        except ValueError:
            return {
                "message": "Hmm, I didn't catch that number. 🤔\n\nJust type the number of months like:\n• 36 (for 3 years)\n• 48 (for 4 years)\n• 60 (for 5 years)\n\nHow many months do you want?",
                "agent": "Master Agent"
            }
    
    def _handle_sales_confirmation(self, message):
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["yes", "proceed", "confirm", "do it", "go ahead", "sure", "ok", "okay", "approve", "accept"]):
            self.conversation_state = "verification"
            customer_name = self.current_customer.get("name", "Customer")
            return {
                "message": f"YESS! 🎉 Love the decision, {customer_name}!\n\nAlright, let's get this ball rolling. First things first - I need to verify your identity and documents. This is just a quick security check, takes like 30 seconds...\n\n🔒 Checking your KYC status...",
                "agent": "Master Agent"
            }
        
        elif any(word in message_lower for word in ["no", "change", "modify", "different", "adjust"]):
            if "amount" in message_lower:
                self.conversation_state = "awaiting_loan_amount"
                return {
                    "message": "No problem! Let's find the right amount for you. 😊\n\nWhat loan amount would work better? (Remember, you can go from ₹50,000 to ₹20,00,000)",
                    "agent": "Master Agent"
                }
            elif "tenure" in message_lower or "month" in message_lower or "year" in message_lower:
                self.conversation_state = "awaiting_tenure"
                return {
                    "message": "Absolutely! Let's adjust the tenure.\n\nHow many months would you prefer? (12 to 60 months)",
                    "agent": "Master Agent"
                }
            else:
                return {
                    "message": "Sure thing! What would you like to change?\n\n• Type **'amount'** to change the loan amount\n• Type **'tenure'** to change the repayment period\n• Type **'both'** to start fresh\n\nWhat should we adjust? 🔧",
                    "agent": "Master Agent"
                }
        
        elif any(word in message_lower for word in ["think", "later", "wait", "maybe"]):
            customer_name = self.current_customer.get("name", "Customer")
            return {
                "message": f"Totally understand, {customer_name}! This is a big decision and you should feel 100% confident. 😊\n\n✅ **I've saved your quote:**\n• Loan Amount: ₹{self.loan_application['amount']:,}\n• Tenure: {self.loan_application['tenure']} months\n• EMI: ₹{self.loan_application['emi']:,.2f}\n• Interest Rate: {self.loan_application['interest_rate']}%\n\n💡 **This quote is valid for 7 days.** After that, rates might change based on market conditions.\n\nWhen you're ready, just say 'ready' or 'let's proceed' and we'll pick up right where we left off!\n\nAny questions I can answer while you think? 🤔",
                "agent": "Master Agent"
            }
        
        elif any(word in message_lower for word in ["negotiate", "lower", "reduce", "better rate", "discount"]):
            credit_score = self.current_customer.get("credit_score", 0)
            current_rate = self.loan_application["interest_rate"]
            
            if credit_score >= 800:
                return {
                    "message": f"I love that you're negotiating! 💪 Shows you're financially savvy.\n\nHere's the thing though - at {current_rate}%, you're already getting our BEST rate because of your excellent {credit_score} credit score. This is literally the lowest we can go for anyone!\n\n🎁 **But here's what I CAN offer:**\n• Waive the 1% processing fee (saves you ₹{self.loan_application['amount'] * 0.01:,.0f})\n• Zero prepayment charges (some banks charge 2-3%)\n• Free credit insurance for first year\n\nThat's about ₹{self.loan_application['amount'] * 0.015:,.0f} in actual savings!\n\nHow's that sound? Fair deal? 🤝",
                    "agent": "Sales Agent"
                }
            elif credit_score >= 700:
                potential_rate = current_rate - 0.5
                return {
                    "message": f"I hear you! Let me see what I can do... 🤔\n\n*Checking with my manager...*\n\nOkay, here's the deal: Your current offer is {current_rate}%. The absolute best I can do is {potential_rate}% IF you:\n\n✅ Set up auto-debit (ensures timely payments)\n✅ Bring in one more banking product (credit card or savings account)\n\nThis would save you about ₹{((current_rate - potential_rate) * self.loan_application['amount'] * self.loan_application['tenure'] / 1200):,.0f} over the loan period!\n\nInterested in this deal? 🤝",
                    "agent": "Sales Agent"
                }
            else:
                return {
                    "message": f"I respect the negotiation attempt! 😊 \n\nHere's the honest truth: At {current_rate}%, this is already the best rate I can offer given your current credit score of {credit_score}.\n\n💡 **But here's a BETTER strategy:**\n\n1. Take this loan at {current_rate}%\n2. Make 6 perfect on-time payments\n3. Your credit score will jump 30-50 points\n4. Come back to me for a rate revision to 11-12%\n\nI've seen this work for SO many customers! You'll actually save more in the long run than if I shaved off 0.5% now.\n\nTrust me on this one? 🙏",
                    "agent": "Sales Agent"
                }
        
        else:
            return {
                "message": "I want to make sure I understand you correctly! Are you:\n\n• ✅ **Ready to proceed?** (say 'yes')\n• 🔄 **Want to change something?** (say 'change')\n• 💭 **Need more time?** (say 'think')\n• 💰 **Want to negotiate?** (say 'negotiate')\n\nWhat's on your mind? 😊",
                "agent": "Sales Agent"
            }
    
    def _handle_verification(self):
        # Invoke Verification Agent
        verification_result = self.agents["verification"].verify_kyc(
            self.current_customer_id,
            self.current_customer
        )
        
        if verification_result["verified"]:
            self.conversation_state = "underwriting"
            response = verification_result["message"]
            response += "\n\n⏭️ Moving to credit assessment..."
            return {
                "message": response,
                "agent": "Verification Agent"
            }
        else:
            self.conversation_state = "completed"
            return {
                "message": verification_result["message"] + "\n\n❌ Unable to proceed without KYC verification. Please complete your KYC and try again.",
                "agent": "Verification Agent"
            }
    
    def _handle_underwriting(self):
        # Invoke Underwriting Agent
        underwriting_result = self.agents["underwriting"].assess_creditworthiness(
            self.current_customer_id,
            self.current_customer,
            self.loan_application["amount"],
            self.loan_application["emi"]
        )
        
        if underwriting_result["approved"]:
            self.conversation_state = "sanction"
            self.loan_application["stage"] = "approved"
            
            # Record approval on blockchain
            try:
                loan_id = f"LOAN-{self.current_customer_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.loan_application["loan_id"] = loan_id
                loan_blockchain.add_loan_approval(
                    customer_id=self.current_customer_id,
                    loan_id=loan_id,
                    approved=True,
                    reason="Credit assessment passed - all criteria met"
                )
            except Exception as e:
                print(f"Blockchain recording error: {e}")
            
            response = underwriting_result["message"]
            response += "\n\n📄 Generating your sanction letter..."
            return {
                "message": response,
                "agent": "Underwriting Agent"
            }
        else:
            self.conversation_state = "completed"
            self.loan_application["stage"] = "rejected"
            
            # Record rejection on blockchain
            try:
                loan_id = f"LOAN-{self.current_customer_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                loan_blockchain.add_loan_approval(
                    customer_id=self.current_customer_id,
                    loan_id=loan_id,
                    approved=False,
                    reason=underwriting_result.get("reason", "Credit assessment failed")
                )
            except Exception as e:
                print(f"Blockchain recording error: {e}")
            
            return {
                "message": underwriting_result["message"],
                "agent": "Underwriting Agent"
            }
    
    def _generate_sanction_letter(self):
        # Invoke Sanction Letter Generator
        sanction_letter = self.agents["sanction"].generate_letter(
            self.current_customer,
            self.loan_application,
            {"approval_type": "approved"}
        )
        
        self.conversation_state = "completed"
        
        return {
            "message": sanction_letter + "\n\n✅ **Application Complete!**\n\nIs there anything else I can help you with?",
            "agent": "Sanction Letter Generator"
        }
    
    def _handle_post_completion(self, message):
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["new", "another", "more", "yes"]):
            # Reset for new application
            self.conversation_state = "greeting_done"
            self.loan_application = {
                "amount": None,
                "tenure": None,
                "purpose": None,
                "interest_rate": None,
                "emi": None,
                "stage": "initial"
            }
            return {
                "message": "Great! Let's start a new loan application. How much would you like to borrow?",
                "agent": "Master Agent"
            }
        else:
            return {
                "message": "Thank you for choosing LoanMaster! If you need any assistance in the future, feel free to reach out. Have a great day! 😊",
                "agent": "Master Agent"
            }
    
    def _handle_general_inquiry(self, message):
        message_lower = message.lower()
        customer_name = self.current_customer.get("name", "Customer") if self.current_customer else "there"
        
        if any(word in message_lower for word in ["rate", "interest", "percentage", "%"]):
            return {
                "message": f"Great question, {customer_name}! Let me break down our interest rates for you. 💡\n\n"
                         f"**Our rates are personalized based on YOUR credit score:**\n\n"
                         f"🌟 **Excellent (800+):** 10.5% per annum\n"
                         f"   *You're a rockstar borrower!*\n\n"
                         f"💪 **Good (700-799):** 11.5% per annum\n"
                         f"   *Strong profile, great rates!*\n\n"
                         f"📈 **Fair (650-699):** 13.5% per annum\n"
                         f"   *Competitive and workable!*\n\n"
                         f"😕 **Below 650:** 15.5% per annum\n"
                         f"   *Higher rate, but we can review after 6 months!*\n\n"
                         f"💡 **Pro tip:** The better your credit score, the better your rate. Simple as that!\n\n"
                         f"Want to apply and see what rate YOU qualify for? 😊",
                "agent": "Master Agent"
            }
        
        elif any(word in message_lower for word in ["document", "paper", "proof", "kyc", "requirement"]):
            return {
                "message": f"Good thinking ahead, {customer_name}! 📄\n\n"
                         f"Here's what you'll need (don't worry, it's simpler than you think!):\n\n"
                         f"**📋 Basic Documents (Everyone needs these):**\n"
                         f"• PAN Card (identity proof)\n"
                         f"• Aadhaar Card (address proof)\n"
                         f"• Last 3 months' bank statements\n\n"
                         f"**💼 Income Proof (Pick what applies):**\n"
                         f"• Salaried: Last 3 salary slips\n"
                         f"• Self-employed: Last 2 years' ITR\n"
                         f"• Business owner: Bank statements + GST returns\n\n"
                         f"**🎁 Bonus:** If you're within your pre-approved limit, you might skip some of these! \n\n"
                         f"Most people just snap photos on their phone and upload. Takes 5 minutes, tops! 📱\n\n"
                         f"Ready to start your application?",
                "agent": "Master Agent"
            }
        
        elif any(word in message_lower for word in ["time", "how long", "duration", "fast", "quick", "when"]):
            return {
                "message": f"Ah, the million-dollar question! ⏱️\n\n"
                         f"**Here's the honest timeline:**\n\n"
                         f"🚀 **Pre-approved customers:** 24-48 hours\n"
                         f"   *Fastest route! Documents ready → Money in account*\n\n"
                         f"⚡ **Good credit, above pre-approved:** 2-3 days\n"
                         f"   *Quick salary verification → Approval → Disbursement*\n\n"
                         f"📋 **Needs review:** 5-7 days\n"
                         f"   *Additional docs → Committee review → Approval*\n\n"
                         f"💡 **Most of my customers?** They get money in 48 hours because they have their documents ready!\n\n"
                         f"Want to start and see how fast we can get you approved? I bet we can do it in 24 hours! 🎯",
                "agent": "Master Agent"
            }
        
        elif any(word in message_lower for word in ["eligible", "qualify", "can i get", "will i"]):
            if self.current_customer:
                pre_approved = self.current_customer.get("pre_approved_limit", 0)
                credit_score = self.current_customer.get("credit_score", 0)
                
                if credit_score >= 700:
                    response = f"Based on what I see, {customer_name}? You're in GREAT shape! 🌟\n\n"
                    response += f"• Credit score: {credit_score} ✅ (Excellent!)\n"
                    response += f"• Pre-approved limit: ₹{pre_approved:,} ✅\n"
                    response += f"• Can potentially go up to: ₹{int(pre_approved * 2):,} 🚀\n\n"
                    response += f"Honestly? You're exactly the kind of customer we LOVE working with!\n\n"
                    response += f"Shall we get you that loan? 😊"
                else:
                    response = f"Let me be straight with you, {customer_name}. 🤝\n\n"
                    response += f"• Credit score: {credit_score}\n"
                    response += f"• Pre-approved limit: ₹{pre_approved:,}\n\n"
                    response += f"You ARE eligible, but we'll need to work within ₹{pre_approved:,} for now. The good news? "
                    response += f"After 6 months of good repayment, we can bump that up significantly!\n\n"
                    response += f"Want to start with what you're pre-approved for?"
                
                return {
                    "message": response,
                    "agent": "Master Agent"
                }
            else:
                return {
                    "message": "I'd love to tell you about your eligibility! But first, I need to pull up your profile.\n\nCould you share your Customer ID? 😊",
                    "agent": "Master Agent"
                }
        
        elif any(word in message_lower for word in ["help", "hello", "hi", "hey"]):
            return {
                "message": f"Hey {customer_name}! 👋 I'm here and ready to help!\n\n"
                         f"What's on your mind? I can help you with:\n\n"
                         f"💰 **Apply for a loan** → Just say 'I need a loan'\n"
                         f"💡 **Learn about rates** → Ask 'what are the rates?'\n"
                         f"📄 **Check requirements** → Ask 'what documents?'\n"
                         f"⚡ **Process timeline** → Ask 'how long does it take?'\n"
                         f"✅ **Your eligibility** → Ask 'am I eligible?'\n\n"
                         f"Or just tell me what you need - I'm pretty good at figuring things out! 😊",
                "agent": "Master Agent"
            }
        
        elif any(word in message_lower for word in ["emi", "monthly", "payment", "installment"]):
            return {
                "message": f"EMI questions - smart! Let me explain. 📊\n\n"
                         f"Your EMI depends on 3 things:\n"
                         f"1. **Loan amount** (how much you borrow)\n"
                         f"2. **Tenure** (how long you repay)\n"
                         f"3. **Interest rate** (based on credit score)\n\n"
                         f"**Quick example:**\n"
                         f"₹5,00,000 loan at 11.5% interest:\n"
                         f"• 24 months → ~₹23,300/month\n"
                         f"• 36 months → ~₹16,500/month\n"
                         f"• 48 months → ~₹13,100/month\n\n"
                         f"💡 **Rule of thumb:** We keep your EMI under 40% of your monthly income to keep you comfortable!\n\n"
                         f"Want me to calculate exact EMIs for your specific situation? Just start an application! 🚀",
                "agent": "Master Agent"
            }
        
        elif any(word in message_lower for word in ["prepay", "close", "foreclosure", "early payment"]):
            return {
                "message": f"Love that you're thinking ahead! 💪\n\n"
                         f"**Our Prepayment Policy:**\n\n"
                         f"✅ **After 6 EMIs:** Prepay anytime with ZERO charges!\n"
                         f"✅ **Partial prepayment:** Allowed (reduces tenure or EMI)\n"
                         f"✅ **Full foreclosure:** No penalties after 6 months\n\n"
                         f"💡 **Pro tip:** Many banks charge 2-5% for prepayment. We charge NOTHING! Why? Because we want you to become debt-free faster!\n\n"
                         f"Plus, early repayment BOOSTS your credit score like crazy! 🚀\n\n"
                         f"Want to get started with a loan? You can always pay it off early! 😊",
                "agent": "Master Agent"
            }
        
        else:
            return {
                "message": f"Hmm, I'm not 100% sure what you're asking, but I'm here to help! 😊\n\n"
                         f"Could you rephrase that? Or pick from these common questions:\n\n"
                         f"• 'What are the interest rates?'\n"
                         f"• 'What documents do I need?'\n"
                         f"• 'How long does approval take?'\n"
                         f"• 'Am I eligible for a loan?'\n"
                         f"• 'I want to apply for a loan'\n\n"
                         f"Or just tell me what you're trying to do and I'll figure it out! 🤝",
                "agent": "Master Agent"
            }
    
    def _extract_number(self, text):
        """Extract number from text (handles formats like '5 lakh', '500000', etc.)"""
        text = text.lower().replace(',', '').replace(' ', '')
        
        # Handle "lakh" and "lakhs"
        if 'lakh' in text:
            text = text.replace('lakhs', '').replace('lakh', '')
            try:
                number = float(''.join(filter(str.isdigit, text)))
                return int(number * 100000)
            except:
                pass
        
        # Extract plain number
        try:
            return int(''.join(filter(str.isdigit, text)))
        except:
            raise ValueError("Could not extract number")
