# Copyright (c) 2025, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ProgramRequirement(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.program_elective_course.program_elective_course import (
			ProgramElectiveCourse,
		)
		from academia.academia.doctype.study_plan_course.study_plan_course import StudyPlanCourse
		from frappe.types import DF

		academic_degree: DF.Literal[
			"",
			"Post-Secondary Diploma",
			"Bachelor's Degree",
			"Postgraduate Diploma",
			"Master Degree",
			"PHD Degree",
		]
		academic_program: DF.Link
		active: DF.Check
		approval_date: DF.Date | None
		date_of_development: DF.Date
		elective_courses: DF.Table[ProgramElectiveCourse]
		implementation_start_academic_year: DF.Link | None
		required_courses: DF.Table[StudyPlanCourse]
		title: DF.Data
	# end: auto-generated types
	pass
