// Copyright (c) 2023, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Course", {
	refresh: function (frm) {
		update_fields(frm);
	},
	elective_template: function (frm) {
		update_fields(frm);
	},
	course_type: function (frm) {
		update_fields(frm);
	},
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

function update_fields(frm) {
	// إذا كان elective_template = 1
	if (frm.doc.elective_template == 1) {
		// إذا كان course_type = "University Elective"
		if (frm.doc.course_type === "University Elective") {
			frm.set_value("faculty", null);
			frm.set_value("program", null);
			frm.set_value("reference_department", null);
		}
		// إذا كان course_type = "Faculty Elective"
		else if (frm.doc.course_type === "Faculty Elective") {
			frm.set_value("program", null);
		}
		// إذا كان course_type = "Program Elective"
		else if (frm.doc.course_type === "Program Elective") {
			frm.set_value("faculty", null);
			frm.set_value("reference_department", null);
		}
	}
	// إذا كان elective_template = 0
	else if (frm.doc.elective_template == 0) {
		frm.set_value("program", null);
		frm.set_value("course_type", null);
	}
}
