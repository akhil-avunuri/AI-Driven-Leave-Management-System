var url = "assets/json/",
  userListData = [],
  editList = false;

// Fetch JSON data
function getJSON(e, t) {
  var a = new XMLHttpRequest();
  a.open("GET", url + e, true);
  a.responseType = "json";
  a.onload = function () {
    var e = a.status;
    t(200 === e ? null : e, a.response);
  };
  a.send();
}

// Load DataTable
function loadUserList(e) {
  if (!Array.isArray(e) || e.length === 0) {
    console.warn("No valid data found for DataTable!");
    return;
  }

  $("#userList-table").DataTable({
    data: e,
    destroy: true,
    bLengthChange: false,
    order: [[0, "desc"]],
    language: {
      oPaginate: {
        sNext: '<i class="mdi mdi-chevron-right"></i>',
        sPrevious: '<i class="mdi mdi-chevron-left"></i>',
      },
    },
    columns: [
      {
        data: "departmentName",
        defaultContent: "No Department"
      },
      {
        data: "subjects",
        render: function (e, t, a) {
          return Array.isArray(a.subjects) ? a.subjects.length : 0;
        },
        defaultContent: "0"
      },
      {
        data: null,
        bSortable: false,
        render: function (e, t, a) {
          return `
            <ul class="list-inline font-size-20 contact-links mb-0">
              <li class="list-inline-item">
                <a href="javascript:void(0);" class="px-2 view-list" data-view-id="${a.id}"><i class="bx bx-show"></i></a>
              </li>
              <li class="list-inline-item">
                <a href="javascript:void(0);" class="px-2 add-subject" data-id="${a.id}" data-bs-toggle="modal" data-bs-target="#newContactModal"><i class="bx bx-plus"></i></a>
              </li>
              <li class="list-inline-item">
                <div class="dropdown">
                  <a href="javascript:void(0);" class="dropdown-toggle card-drop px-2" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="mdi mdi-dots-horizontal font-size-18"></i>
                  </a>
                  <ul class="dropdown-menu dropdown-menu-end">
                    <li><a href="#newContactModal" data-bs-toggle="modal" class="dropdown-item edit-list" data-edit-id="${a.id}"><i class="mdi mdi-pencil font-size-16 text-success me-1"></i> Edit</a></li>
                    <li><a href="#removeItemModal" data-bs-toggle="modal" class="dropdown-item remove-list" data-remove-id="${a.id}"><i class="mdi mdi-trash-can font-size-16 text-danger me-1"></i> Delete</a></li>
                  </ul>
                </div>
              </li>
            </ul>`;
        }
      }
    ],
    drawCallback: function () {
      editContactList();
      removeItem();
      viewContact();
      addSubject();
    }
  });
}

// Fetch data from JSON
getJSON("contact-user-list.json", function (e, t) {
  if (e !== null) {
    console.log("Something went wrong: " + e);
  } else {
    console.log("Loaded Data:", t);
    userListData = t;
    loadUserList(userListData);
  }
});

// Find next unique ID
function findNextId() {
  return userListData.length > 0 ? Math.max(...userListData.map((d) => d.id)) + 1 : 1;
}

// Add New Department
$(".addContact-modal").on("click", function () {
  editList = false;
  $("#newContactModalLabel").text("Add Department");
  $("#addContact-btn").text("Add");

  $("#createContact-form").html(`
    <div class="mb-3">
      <label for="department-input" class="form-label">Department</label>
      <input type="text" id="department-input" class="form-control" placeholder="Enter Department" required />
      <div class="invalid-feedback">Please enter a department.</div>
    </div>
    <div class="text-end">
      <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
      <button type="submit" class="btn btn-success">Add</button>
    </div>
  `);

  $("#createContact-form").off("submit").on("submit", function (e) {
    e.preventDefault();
    let departmentName = $("#department-input").val().trim();

    if (departmentName === "") {
      alert("Please enter a valid department name!");
      return;
    }

    let newDepartment = {
      id: findNextId(),
      departmentName: departmentName,
      subjects: []
    };

    userListData.push(newDepartment);
    loadUserList(userListData);
    $("#newContactModal").modal("hide"); // Close modal after adding
  });
});

// Add Subject Functionality
function addSubject() {
  $(".add-subject").on("click", function () {
    let id = $(this).data("id");

    $("#newContactModalLabel").text("Add Subject");
    $("#addContact-btn").text("Add Subject");

    $("#createContact-form").html(`
      <div class="mb-3">
        <label for="subject-input" class="form-label">Subject</label>
        <input type="text" id="subject-input" class="form-control" placeholder="Enter Subject" required />
        <div class="invalid-feedback">Please enter a subject.</div>
      </div>
      <div class="text-end">
        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="submit" class="btn btn-success">Add Subject</button>
      </div>
    `);

    $("#createContact-form").off("submit").on("submit", function (e) {
      e.preventDefault();
      let subject = $("#subject-input").val().trim();
      let department = userListData.find((item) => item.id == id);

      if (subject === "") {
        alert("Please enter a valid subject!");
        return;
      }

      if (department) {
        department.subjects.push(subject);
        loadUserList(userListData);
        $("#newContactModal").modal("hide"); // Close modal after adding
      }
    });
  });
}

// Remove Department
function removeItem() {
  $(".remove-list").on("click", function () {
    let id = $(this).data("remove-id");

    $("#remove-item").on("click", function () {
      userListData = userListData.filter((item) => item.id != id);
      loadUserList(userListData);
      $("#removeItemModal").modal("hide");
    });
  });
}

// View Department Details
function viewContact() {
  $(".view-list").on("click", function () {
    let id = $(this).data("view-id");
    let department = userListData.find((item) => item.id == id);

    if (department) {
      alert("Department Details: " + JSON.stringify(department, null, 2));
    }
  });
}
