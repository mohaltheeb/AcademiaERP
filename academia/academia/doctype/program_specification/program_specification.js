// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Study Plan Course", {
	table_ytno_add: function (frm) {
		frm.fields_dict["table_ytno"].grid.get_field("course_code").get_query = function (doc) {
			var courses_list = [];
			$.each(doc.table_ytno, function (idx, val) {
				if (val.course_code) courses_list.push(val.course_code);
			});
			return { filters: [["Course Specification", "name", "not in", courses_list]] };
		};
	},
});

frappe.ui.form.on("Program Specification", {
	refresh: function (frm) {
		// Import University Courses
		frm.add_custom_button(__("Import University Courses"), function () {
			frappe.call({
				method: "academia.academia.doctype.program_specification.program_specification.get_required_courses",
				args: {
					doc: JSON.stringify(frm.doc),
				},
				callback: function (r) {
					if (r.message) {
						let courses = r.message;
						let added = 0;

						courses.forEach(function (course) {
							if (course.source === "required") {
								// التحقق من عدم وجود المادة مسبقاً في جدول المواد الإلزامية (table_ytno)
								let exists = frm.doc.table_ytno.some(function (row) {
									return row.course_code === course.course_code;
								});
								if (!exists) {
									frm.add_child("table_ytno", {
										course_code: course.course_code,
										course_name: course.course_name,
										course_type: course.course_type,
										study_level: course.study_level,
										semester: course.semester,
									});
									added++;
								}
							} else if (course.source === "elective") {
								// التحقق من عدم وجود المادة مسبقاً في جدول المواد الاختيارية (university_elective_course)
								let exists = frm.doc.university_elective_course.some(function (
									row
								) {
									return row.course_code === course.course_code;
								});
								if (!exists) {
									frm.add_child("university_elective_course", {
										course_code: course.course_code,
										course_name: course.course_name,
									});
									added++;
								}
							}
						});

						frm.refresh_field("table_ytno");
						frm.refresh_field("university_elective_course");
						frappe.msgprint(added + " courses imported successfully.");
					}
				},
			});
		});

		// Import Faculty Courses
		frm.add_custom_button(__("Import Faculty Courses"), function () {
			frappe.call({
				method: "academia.academia.doctype.program_specification.program_specification.get_required_faculty_courses",
				args: {
					doc: JSON.stringify(frm.doc),
				},
				callback: function (r) {
					if (r.message) {
						let coursess = r.message;
						let added = 0;

						coursess.forEach(function (course) {
							if (course.source === "required") {
								// التحقق من عدم وجود المادة مسبقاً في جدول المواد الإلزامية (table_ytno)
								let exists = frm.doc.table_ytno.some(function (row) {
									return row.course_code === course.course_code;
								});
								if (!exists) {
									frm.add_child("table_ytno", {
										course_code: course.course_code,
										course_name: course.course_name,
										course_type: course.course_type,
										study_level: course.study_level,
										semester: course.semester,
									});
									added++;
								}
							} else if (course.source === "elective") {
								// التحقق من عدم وجود المادة مسبقاً في جدول المواد الاختيارية (faculty_elective_course)
								let exists = frm.doc.faculty_elective_course.some(function (row) {
									return row.course_code === course.course_code;
								});
								if (!exists) {
									frm.add_child("faculty_elective_course", {
										course_code: course.course_code,
										course_name: course.course_name,
									});
									added++;
								}
							}
						});

						frm.refresh_field("table_ytno");
						frm.refresh_field("faculty_elective_course");
						frappe.msgprint(added + " courses imported successfully.");
					}
				},
			});
		});
	},
});
