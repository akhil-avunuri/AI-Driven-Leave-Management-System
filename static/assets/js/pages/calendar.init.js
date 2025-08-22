"use strict";
!(function (e, t) {
  var l, n, c, i;

  function o(e, t) {
    var n = [],
      a = moment(e.start.toUTCString());
    return (
      t || n.push("<strong>" + a.format("HH:mm") + "</strong> "),
      e.isPrivate
        ? (n.push('<span class="calendar-font-icon ic-lock-b"></span>'),
          n.push(" Private"))
        : (e.isReadOnly
            ? n.push('<span class="calendar-font-icon ic-readonly-b"></span>')
            : e.recurrenceRule
            ? n.push('<span class="calendar-font-icon ic-repeat-b"></span>')
            : e.attendees.length
            ? n.push('<span class="calendar-font-icon ic-user-b"></span>')
            : e.location &&
              n.push('<span class="calendar-font-icon ic-location-b"></span>'),
          n.push(" " + e.title)),
      n.join("")
    );
  }

  function r(e) {
    var t = $(e.target).closest('a[role="menuitem"]')[0],
      n = f(t),
      a = l.getOptions(),
      o = "";
    switch ((console.log(t), console.log(n), n)) {
      case "toggle-daily":
        o = "day";
        break;
      case "toggle-weekly":
        o = "week";
        break;
      case "toggle-monthly":
        (a.month.visibleWeeksCount = 0), (o = "month");
        break;
      case "toggle-weeks2":
        (a.month.visibleWeeksCount = 2), (o = "month");
        break;
      case "toggle-weeks3":
        (a.month.visibleWeeksCount = 3), (o = "month");
        break;
      case "toggle-narrow-weekend":
        (a.month.narrowWeekend = !a.month.narrowWeekend),
          (a.week.narrowWeekend = !a.week.narrowWeekend),
          (o = l.getViewName()),
          (t.querySelector("input").checked = a.month.narrowWeekend);
        break;
      case "toggle-start-day-1":
        (a.month.startDayOfWeek = a.month.startDayOfWeek ? 0 : 1),
          (a.week.startDayOfWeek = a.week.startDayOfWeek ? 0 : 1),
          (o = l.getViewName()),
          (t.querySelector("input").checked = a.month.startDayOfWeek);
        break;
      case "toggle-workweek":
        (a.month.workweek = !a.month.workweek),
          (a.week.workweek = !a.week.workweek),
          (o = l.getViewName()),
          (t.querySelector("input").checked = !a.month.workweek);
    }
    l.setOptions(a, !0), l.changeView(o, !0), k(), p(), w();
  }

  function d(e) {
    switch (f(e.target)) {
      case "move-prev":
        l.prev();
        break;
      case "move-next":
        l.next();
        break;
      case "move-today":
        l.today();
        break;
      default:
        return;
    }
    p(), w();
  }

  function u(e) {
    var t,
      n,
      a,
      o,
      r = f($(e.target).closest('a[role="menuitem"]')[0]);
    (t = r),
      (n = document.getElementById("calendarName")),
      (a = findCalendar(t)),
      (o = []).push(
        '<span class="calendar-bar" style="background-color: ' +
          a.bgColor +
          "; border-color:" +
          a.borderColor +
          ';"></span>'
      ),
      o.push('<span class="calendar-name">' + a.name + "</span>"),
      (n.innerHTML = o.join("")),
      (i = a);
  }

  function m(e) {
    var t = e.target.value,
      n = e.target.checked,
      a = document.querySelector(".lnb-calendars-item input"),
      o = Array.prototype.slice.call(
        document.querySelectorAll("#calendarList input")
      ),
      r = !0;
    "all" === t
      ? ((r = n),
        o.forEach(function (e) {
          var t = e.parentNode;
          (e.checked = n),
            (t.style.backgroundColor = n ? t.style.borderColor : "transparent");
        }),
        CalendarList.forEach(function (e) {
          e.checked = n;
        }))
      : ((findCalendar(t).checked = n),
        (r = o.every(function (e) {
          return e.checked;
        })),
        (a.checked = !!r)),
      h();
  }

  function h() {
    var e = Array.prototype.slice.call(
      document.querySelectorAll("#calendarList input")
    );
    CalendarList.forEach(function (e) {
      l.toggleSchedules(e.id, !e.checked, !1);
    }),
      l.render(!0),
      e.forEach(function (e) {
        var t = e.nextElementSibling;
        t.style.backgroundColor = e.checked
          ? t.style.borderColor
          : "transparent";
      });
  }

  function k() {
    var e = document.getElementById("calendarTypeName"),
      t = document.getElementById("calendarTypeIcon"),
      n = l.getOptions(),
      a = l.getViewName(),
      o =
        "day" === a
          ? ((a = "Daily"), "calendar-icon ic_view_day")
          : "week" === a
          ? ((a = "Weekly"), "calendar-icon ic_view_week")
          : 2 === n.month.visibleWeeksCount
          ? ((a = "2 weeks"), "calendar-icon ic_view_week")
          : 3 === n.month.visibleWeeksCount
          ? ((a = "3 weeks"), "calendar-icon ic_view_week")
          : ((a = "Monthly"), "calendar-icon ic_view_month");
    (e.innerHTML = a), (t.className = o);
  }

  function p() {
    var e = document.getElementById("renderRange"),
      t = l.getOptions(),
      n = l.getViewName(),
      a = [];
    "day" === n
      ? a.push(moment(l.getDate().getTime()).format("YYYY.MM.DD"))
      : "month" === n &&
        (!t.month.visibleWeeksCount || 4 < t.month.visibleWeeksCount)
      ? a.push(moment(l.getDate().getTime()).format("YYYY.MM"))
      : (a.push(moment(l.getDateRangeStart().getTime()).format("YYYY.MM.DD")),
        a.push(" ~ "),
        a.push(moment(l.getDateRangeEnd().getTime()).format(" MM.DD"))),
      (e.innerHTML = a.join(""));
  }

  function w() {
    l.clear();
    fetch("{% url 'get_schedules' %}")
      .then(response => response.json())
      .then(data => {
        console.log("Loaded schedules:", data);
        l.createSchedules(data);
        l.render();
        h();
      })
      .catch(error => console.error("Error loading schedules:", error));
  }

  function f(e) {
    return e.dataset ? e.dataset.action : e.getAttribute("data-action");
  }

  l = new t("#calendar", {
    defaultView: "month",
    useCreationPopup: false,
    useDetailPopup: true,
    calendars: CalendarList,
    template: {
      milestone: function (e) {
        return (
          '<span class="calendar-font-icon ic-milestone-b"></span> <span style="background-color: ' +
          e.bgColor +
          '">' +
          e.title +
          "</span>"
        );
      },
      allday: function (e) {
        return o(e, !0);
      },
      time: function (e) {
        return o(e, !1);
      },
    },
  }).on({
    clickMore: function (e) {
      console.log("clickMore", e);
    },
    clickSchedule: function (e) {
      console.log("clickSchedule", e);
    },
    clickDayname: function (e) {
      console.log("clickDayname", e);
    },
    beforeUpdateSchedule: function (e) {
      var t = e.schedule,
        n = e.changes;
      console.log("beforeUpdateSchedule", e);
      l.updateSchedule(t.id, t.calendarId, n);
      h();
    },
    beforeDeleteSchedule: function (e) {
      console.log("beforeDeleteSchedule", e);
      l.deleteSchedule(e.schedule.id, e.schedule.calendarId);
    },
    afterRenderSchedule: function (e) {
      e.schedule;
    },
    clickTimezonesCollapseBtn: function (e) {
      console.log("timezonesCollapsed", e);
      return e
        ? l.setTheme({
            "week.daygridLeft.width": "77px",
            "week.timegridLeft.width": "77px",
          })
        : l.setTheme({
            "week.daygridLeft.width": "60px",
            "week.timegridLeft.width": "60px",
          }),
        !0;
    },
  });

  $("#btn-new-schedule").off("click").on("click", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $("#newScheduleModal").modal("show");
  });

  $("#save-schedule").on("click", function () {
    var sectionName = $("#section-name").val(),
      startTime = $("#start-time").val(),
      endTime = $("#end-time").val();

    if (sectionName && startTime && endTime) {
      fetch("{% url 'create_schedule' %}", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": "{{ csrf_token }}",
        },
        body: JSON.stringify({
          section_name: sectionName,
          start_time: startTime,
          end_time: endTime,
        }),
      })
        .then(response => response.json())
        .then(data => {
          console.log("Server response:", data);
          l.createSchedules([
            {
              id: String(data.id),
              title: data.section_name,
              start: new Date(data.start),
              end: new Date(data.end),
              category: "time",
            },
          ]);
          l.render();
          $("#newScheduleModal").modal("hide");
          $("#new-schedule-form")[0].reset();
        })
        .catch(error => console.error("Error saving schedule:", error));
    } else {
      alert("Please fill in all fields.");
    }
  });

  n = tui.util.throttle(function () {
    l.render();
  }, 50);

  e.cal = l;
  k();
  p();
  w();

  $("#menu-navi").on("click", d);
  $(document).on("click", '.dropdown-menu a[role="menuitem"]', function(e) {
    e.preventDefault();
    console.log("Dropdown item clicked:", $(this).data("action"));
    r(e);
  });
  $("#lnb-calendars").on("change", m);
  $("#dropdownMenu-calendars-list").on("click", u);
  e.addEventListener("resize", n);
})(window, tui.Calendar);

(function () {
  var e = document.getElementById("calendarList"),
    t = [];
  CalendarList.forEach(function (e) {
    t.push(
      '<div class="lnb-calendars-item"><label><input type="checkbox" class="tui-full-calendar-checkbox-round" value="' +
        e.id +
        '" checked><span style="border-color: ' +
        e.borderColor +
        "; background-color: " +
        e.borderColor +
        ';"></span><span>' +
        e.name +
        "</span></label></div>"
    );
  });
  e.innerHTML = t.join("\n");
})();