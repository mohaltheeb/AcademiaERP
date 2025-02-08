# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ProgramSpecification(Document):
	def get_course_list(self):
		return [
			frappe.get_doc("Course Specification", study_plan_course.course_code)
			for study_plan_course in self.table_ytno
		]

	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from academia.academia.doctype.course_language.course_language import CourseLanguage
		from academia.academia.doctype.credit_hours_course.credit_hours_course import CreditHoursCourse
		from academia.academia.doctype.program_elective_course.program_elective_course import (
			ProgramElectiveCourse,
		)
		from academia.academia.doctype.study_plan_course.study_plan_course import StudyPlanCourse

		abbr: DF.ReadOnly
		academic_degree: DF.ReadOnly
		academic_system: DF.Literal["", "Semester System", "Credit Hours System", "Annual System"]
		amended_from: DF.Link | None
		approval_date: DF.Date | None
		course_language: DF.TableMultiSelect[CourseLanguage]
		courses: DF.Check
		date_of_programe_development: DF.Date
		date_of_starting_the_program: DF.Date | None
		delivery_mode: DF.Literal["", "On Campus", "Online"]
		department: DF.ReadOnly
		faculty: DF.ReadOnly
		faculty_elective_course: DF.Table[ProgramElectiveCourse]
		faculty_requirements: DF.Link
		file: DF.Attach | None
		implementation_start_academic_year: DF.Link | None
		maximum_research_period: DF.Int
		minimum_course_average_to_start_research: DF.Data | None
		minimum_research_period: DF.Int
		program_elective_course: DF.Table[ProgramElectiveCourse]
		program_name: DF.Link
		program_name_english: DF.ReadOnly
		program_requirements: DF.Link
		research_or_thesis: DF.Check
		table_omcu: DF.Table[CreditHoursCourse]
		table_ytno: DF.Table[StudyPlanCourse]
		total_elective_hours: DF.Int
		total_hours_required_to_award_degree: DF.Int
		university_elective_course: DF.Table[ProgramElectiveCourse]
		university_requirements: DF.Link
	# end: auto-generated types


# Funcation to get University Requirement Course
@frappe.whitelist()
def get_required_courses(doc):
	"""
	Fetches courses from the selected University Requirement document.
	It collects courses from both child tables: course_required_tab and course_elective_tab,
	and returns a list of courses with their details.
	"""
	doc = frappe.parse_json(doc)
	if not doc.get("university_requirements"):
		frappe.throw(_("Please select University Requirements before fetching courses."))

	courses = []

	# جلب سجل University Requirement
	university_requirement = frappe.get_doc("University Requirement", doc.get("university_requirements"))

	# جلب المواد من جدول المواد الإلزامية (required_courses)
	if university_requirement.get("required_courses"):
		for row in university_requirement.get("required_courses"):
			courses.append(
				{
					"course_code": row.get("course_code"),
					"course_name": row.get("course_name"),
					"course_type": row.get("course_type"),
					"study_level": row.get("study_level"),
					"semester": row.get("semester"),
					"source": "required",
				}
			)

	# جلب المواد من جدول المواد الاختيارية (elective_courses)
	if university_requirement.get("elective_courses"):
		for row in university_requirement.get("elective_courses"):
			courses.append(
				{
					"course_code": row.get("course_code"),
					"course_name": row.get("course_name"),
					"source": "elective",
				}
			)

	if not courses:
		frappe.throw(_("No courses found in the selected University Requirements."))

	return courses


# Funcation to get Faculty Requirement Course
@frappe.whitelist()
def get_required_faculty_courses(doc):
	"""
	Fetches courses from the selected Faculty Requirement document.
	It collects courses from both child tables: course_required_tab and course_elective_tab,
	and returns a list of courses with their details.
	"""
	doc = frappe.parse_json(doc)
	if not doc.get("faculty_requirements"):
		frappe.throw(_("Please select Faculty Requirements before fetching courses."))

	coursess = []

	# جلب سجل Faculty Requirement
	faculty_requirement = frappe.get_doc("Faculty Requirement", doc.get("faculty_requirements"))

	# جلب المواد من جدول المواد الإلزامية (required_courses)
	if faculty_requirement.get("required_courses"):
		for row in faculty_requirement.get("required_courses"):
			coursess.append(
				{
					"course_code": row.get("course_code"),
					"course_name": row.get("course_name"),
					"course_type": row.get("course_type"),
					"study_level": row.get("study_level"),
					"semester": row.get("semester"),
					"source": "required",
				}
			)

	# جلب المواد من جدول المواد الاختيارية (elective_courses)
	if faculty_requirement.get("elective_courses"):
		for row in faculty_requirement.get("elective_courses"):
			coursess.append(
				{
					"course_code": row.get("course_code"),
					"course_name": row.get("course_name"),
					"source": "elective",
				}
			)

	if not coursess:
		frappe.throw(_("No courses found in the selected Faculty Requirements."))

	return coursess


# Funcation to get Program Requirement Course
@frappe.whitelist()
def get_required_Program_courses(doc):
	"""
	Fetches courses from the selected Program Requirement document.
	It collects courses from both child tables: course_required_tab and course_elective_tab,
	and returns a list of courses with their details.
	"""
	doc = frappe.parse_json(doc)
	if not doc.get("program_requirements"):
		frappe.throw(_("Please select Program Requirements before fetching courses."))

	coursesss = []

	# جلب سجل University Requirement
	program_requirement = frappe.get_doc("Program Requirement", doc.get("program_requirements"))

	# جلب المواد من جدول المواد الإلزامية (required_courses)
	if program_requirement.get("required_courses"):
		for row in program_requirement.get("required_courses"):
			coursesss.append(
				{
					"course_code": row.get("course_code"),
					"course_name": row.get("course_name"),
					"course_type": row.get("course_type"),
					"study_level": row.get("study_level"),
					"semester": row.get("semester"),
					"source": "required",
				}
			)

	# جلب المواد من جدول المواد الاختيارية (elective_courses)
	if program_requirement.get("elective_courses"):
		for row in program_requirement.get("elective_courses"):
			coursesss.append(
				{
					"course_code": row.get("course_code"),
					"course_name": row.get("course_name"),
					"source": "elective",
				}
			)

	if not coursesss:
		frappe.throw(_("No courses found in the selected Prpgram Requirements."))

	return coursesss
