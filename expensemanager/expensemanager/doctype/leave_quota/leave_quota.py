# Copyright (c) 2024, t.p and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaveQuota(Document):
    def validate(self):
        # Automatically calculate Leave Balance
        self.calculate_leave_balance()

    def calculate_leave_balance(self):
        # Ensure that Leave Taken is set to 0 if it is None
        if self.leave_taken is None:
            self.leave_taken = 0
        
        # Calculate Leave Balance
        self.leave_balance = self.maximum_allowed - self.leave_taken
        
        # Log for debugging
        frappe.log_error(f"Leave Taken: {self.leave_taken}, Maximum Allowed: {self.maximum_allowed}, Leave Balance: {self.leave_balance}", "Leave Quota Calculation")
