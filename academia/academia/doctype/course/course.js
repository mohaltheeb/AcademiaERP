// Copyright (c) 2023, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Course", {
	faculty: function (frm) {
		var faculty = frm.doc.faculty;
		frm.set_query("program", function () {
			return {
				filters: {
					faculty: faculty,
				},
			};
		});
		frm.set_value("program", "");
	},
	before_save: function (frm) {
		if (
			frm.doc.course_type === "University Requirement" ||
			frm.doc.course_type === "Faculty Requirement"
		) {
			frm.set_value("program", "");
		}
	},
	after_save: function (frm) {
		// التأكد من أن السجل جديد (عند إنشاء السجل تكون قيمة creation مساوية لـ modified)
		if (frm.doc.creation === frm.doc.modified) {
			frappe.msgprint({
				title: __("Attention"),
				indicator: "orange",
				message: __(
					"You must add a course specification for the course you just created."
				),
				primary_action: {
					label: __("Go to Course Specification"),
					action: function () {
						// إنشاء سجل جديد في doctype "Course Specification" مع تمرير قيمة حقل course_code
						frappe.new_doc("Course Specification", { course_code: frm.doc.name });
					},
				},
			});
		}
	},
});
