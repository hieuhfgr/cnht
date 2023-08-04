// Lấy giá trị toggle lịch từ localStorage (nếu có)
const isCalendarVisible = localStorage.getItem("isCalendarVisible") || "true";

// Ẩn/hiện lịch dựa trên giá trị toggle từ localStorage
const calendar = document.getElementById("calendar");
calendar.style.display = isCalendarVisible === "true" ? "block" : "none";

// Xử lý sự kiện khi click vào button toggle
const toggleButton = document.getElementById("toggle-calendar");
toggleButton.addEventListener("click", () => {
    if (calendar.style.display === "block") {
        // Nếu đang hiện lịch, ẩn lịch và lưu giá trị toggle vào localStorage
        calendar.style.display = "none";
        localStorage.setItem("isCalendarVisible", "false");
    } else {
        // Nếu đang ẩn lịch, hiện lịch và lưu giá trị toggle vào localStorage
        calendar.style.display = "block";
        localStorage.setItem("isCalendarVisible", "true");
    }
});