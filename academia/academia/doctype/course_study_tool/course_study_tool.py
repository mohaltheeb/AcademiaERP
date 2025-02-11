# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class CourseStudyTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.course_study_course.course_study_course import CourseStudyCourse
		from frappe.types import DF

		academic_program: DF.Literal["", "All Programs", "Specific Program"]
		academic_term: DF.Link
		academic_year: DF.Link
		based_on: DF.Literal["", "Program", "Batch"]
		courses: DF.Table[CourseStudyCourse]
		current_level: DF.ReadOnly
		current_semester: DF.Link | None
		faculty: DF.Link
		level: DF.Literal["", "All Levels", "Specific Level"]
		program_specification: DF.ReadOnly | None
		semester: DF.Literal["", "All Semester", "Specific Semester"]
		specific_level: DF.Link | None
		specific_program: DF.Link | None
		specific_semester: DF.Link | None
		student_batch: DF.Link | None
	# end: auto-generated types

	@frappe.whitelist()
	def get_courses(self):
		child_table_data = []

		if self.based_on == "Batch":
			if not self.student_batch:
				frappe.throw(_("Mandatory field - Student Batch"))

			batch_doc = frappe.get_doc("Student Batch", self.student_batch)
			if batch_doc.status == "Finished":
				frappe.throw(_("This Batch is already finished..."))

			program_specification_doc = frappe.get_doc(
				"Program Specification", batch_doc.program_specification
			)
			for child in program_specification_doc.table_ytno:
				if (
					child.study_level == batch_doc.current_level
					and child.semester == batch_doc.current_semester
				):
					child_data = child.as_dict()
					child_data["batch"] = self.student_batch
					child_table_data.append(child_data)

		elif self.based_on == "Program":
			if not self.academic_program:
				frappe.throw(_("Mandatory field - Academic Program"))

			filters = {"status": "Continue"}
			if self.academic_program != "All Programs":
				if not self.specific_program:
					frappe.throw(_("Mandatory field - Specific Program"))
				filters["program"] = self.specific_program

			batches = frappe.get_list(
				"Student Batch",
				filters=filters,
				fields=["name", "program_specification", "current_level", "current_semester"],
			)

			for batch in batches:
				if self.level == "Specific Level" and batch.current_level != self.specific_level:
					continue
				if (
					self.academic_term == "Specific Semester"
					and batch.current_semester != self.specific_semester
				):
					continue

				program_specification_doc = frappe.get_doc(
					"Program Specification", batch.program_specification
				)
				for child in program_specification_doc.table_ytno:
					if child.study_level == batch.current_level and child.semester == batch.current_semester:
						child_data = child.as_dict()
						child_data["batch"] = batch.name
						child_table_data.append(child_data)

		else:
			frappe.throw(_("Mandatory field - Based On"))

		if child_table_data:
			return child_table_data
		else:
			frappe.throw(_("No courses found"))

	@frappe.whitelist()
	def generate_courses(self):
		if not self.academic_year:
			frappe.throw(_("Mandatory field - Academic Year"))
		elif not self.academic_term:
			frappe.throw(_("Mandatory field - Academic term"))
		else:
			for cour in self.courses:
				child_hours_data = {}

				key = cour.course_code
				course_specification_doc = frappe.get_doc("Course Specification", key)
				for child in course_specification_doc.credit_hours:
					child_hours = child.as_dict()
					child_hours_data[child.hour_type] = child_hours

				num = len(child_hours_data)
				if num < 1:
					frappe.msgprint(
						_(
							"You have to add at least one row for the credit hours table in {0} course specification..."
						).format(cour.course_name)
					)
				elif num >= 1:
					for i, hour_table in child_hours_data.items():
						course_exists_in_course_study = frappe.db.exists(
							"Course Study",
							{"course_code": cour.course_code, "course_type": hour_table["hour_type"]},
						)
						if course_exists_in_course_study:
							frappe.msgprint(
								_("This course {0} already generated...").format(
									cour.course_name + " " + hour_table["hour_type"]
								)
							)
						else:
							course_study = frappe.new_doc("Course Study")
							course_study.course_code = (
								cour.batch + " " + cour.course_code + " " + hour_table["hour_type"]
							)
							course_study.student_batch = cour.batch
							course_study.program = cour.parent
							course_study.academic_year = self.academic_year
							course_study.academic_term = self.academic_term
							course_study.level = cour.study_level
							course_study.course_type = hour_table["hour_type"]
							course_study.hours = hour_table["hours"]
							course_study.lab_type = hour_table["lab_type"]
							course_study.suitable_env = hour_table["suitable_env"]
							course_study.save()

			frappe.msgprint(_("Generated Successfully..."))
