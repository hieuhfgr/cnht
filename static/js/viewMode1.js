const viewModeForm = document.querySelector('#view-mode-form');
const viewModeSelect = document.querySelector('#view-mode');

// Lấy giá trị từ localStorage nếu có
const savedViewMode = localStorage.getItem('viewMode');
if (savedViewMode) {
viewModeSelect.value = savedViewMode;
}

// Thêm listener cho sự kiện submit của form
viewModeForm.addEventListener('submit', (event) => {
event.preventDefault(); // Ngăn chặn form submit
const selectedValue = viewModeSelect.value;
localStorage.setItem('viewMode', selectedValue); // Luu gia tri vào localStorage
viewModeForm.submit(); // Submit form
});