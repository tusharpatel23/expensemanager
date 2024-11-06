# # Copyright (c) 2024, t.p and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document

# class LeaveApplication(Document):
#     def validate(self):
#         # Calculate total days before validation
#         self.calculate_total_days()
        
#         # Validate leave quota before submission
#         self.validate_leave_quota()

#     def calculate_total_days(self):
#         # Ensure that Start Date and End Date are set
#         if not self.start_date or not self.end_date:
#             frappe.throw("Start Date and End Date must be set to calculate Total Days.")

#         # Calculate the number of days
#         start_date = frappe.utils.getdate(self.start_date)
#         end_date = frappe.utils.getdate(self.end_date)
        
#         if end_date < start_date:
#             frappe.throw("End Date cannot be earlier than Start Date.")

#         # Calculate total days (inclusive)
#         self.total_days = (end_date - start_date).days + 1  # Adding 1 to include the start day

#     def validate_leave_quota(self):
#         leave_quota = frappe.get_doc('Leave Quota', {
#             'employee': self.employee,
#             'leave_type': self.leave_type
#         })

#         # Check if leave_quota exists
#         if not leave_quota:
#             frappe.throw(f"No leave quota found for employee {self.employee} and leave type {self.leave_type}. Please create a leave quota.")

#         # Set default values if None
#         leave_quota.leave_taken = leave_quota.leave_taken or 0
#         leave_quota.leave_balance = leave_quota.leave_balance or 0

#         # Validate leave balance
#         if leave_quota.leave_balance < self.total_days:
#             frappe.throw(f"Insufficient leave balance for {self.leave_type}. Available: {leave_quota.leave_balance} days.")

#     def on_update_after_submit(self):
#         # Update leave quota after approval
#         if self.status == 'Approved':
#             self.update_leave_quota()

#     def update_leave_quota(self):
#         leave_quota = frappe.get_doc('Leave Quota', {
#             'employee': self.employee,
#             'leave_type': self.leave_type
#         })

#         # Update leave taken and calculate new leave balance
#         leave_quota.leave_taken += self.total_days
#         leave_quota.leave_balance = leave_quota.maximum_allowed - leave_quota.leave_taken

#         # Log values for debugging
#         frappe.log_error(f"Updated Leave Taken: {leave_quota.leave_taken}, New Leave Balance: {leave_quota.leave_balance}", "Leave Quota Update")

#         leave_quota.save()


import frappe
from frappe.model.document import Document

class LeaveApplication(Document):
    def validate(self):
        # Calculate total days
        self.calculate_total_days()

        # Validate leave quota before submission
        self.validate_leave_quota()

    def calculate_total_days(self):
        if not self.start_date or not self.end_date:
            frappe.throw("Start Date and End Date must be set to calculate Total Days.")

        # Calculate the number of days between Start and End Date
        start_date = frappe.utils.getdate(self.start_date)
        end_date = frappe.utils.getdate(self.end_date)

        if end_date < start_date:
            frappe.throw("End Date cannot be earlier than Start Date.")
        
        # Adding 1 to include the start date in the total days
        self.total_days = (end_date - start_date).days + 1

    def validate_leave_quota(self):
        # Fetch the Leave Quota for the employee and leave type
        leave_quota = frappe.get_doc('Leave Quota', {
            'employee': self.employee,
            'leave_type': self.leave_type
        })

        # Check if the leave balance is sufficient
        if leave_quota.leave_balance < self.total_days:
            frappe.throw(f"Insufficient leave balance for {self.leave_type}. Available: {leave_quota.leave_balance} days.")

    def on_update_after_submit(self):
        if self.status == 'Approved':
            self.update_leave_quota()

    def update_leave_quota(self):
        # Update leave balance after approval
        leave_quota = frappe.get_doc('Leave Quota', {
            'employee': self.employee,
            'leave_type': self.leave_type
        })
        
        # Update the leave taken and leave balance
        leave_quota.leave_taken += self.total_days
        leave_quota.leave_balance = leave_quota.maximum_allowed - leave_quota.leave_taken
        leave_quota.save()
