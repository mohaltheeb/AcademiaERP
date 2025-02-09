// Copyright (c) 2025, SanU and contributors
// For license information, please see license.txt

// frappe.ui.form.on("University Requirement", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Study Plan Course", {
	required_courses_add: function (frm) {
		frm.fields_dict["required_courses"].grid.get_field("course_code").get_query = function (
			doc
		) {
			var courses_list = [];
			$.each(doc.required_courses, function (idx, val) {
				if (val.course_code) courses_list.push(val.course_code);
			});
			return { filters: [["Course Specification", "name", "not in", courses_list]] };
		};
	},
});

frappe.ui.form.on("Program Elective Course", {
	elective_courses_add: function (frm) {
		frm.fields_dict["elective_courses"].grid.get_field("course_code").get_query = function (
			doc
		) {
			var courses_list = [];
			$.each(doc.elective_courses, function (idx, val) {
				if (val.course_code) courses_list.push(val.course_code);
			});
			return { filters: [["Course Specification", "name", "not in", courses_list]] };
		};
	},
});
