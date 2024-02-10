//Query All input fields
var form_fields = document.getElementsByTagName("input");
var form_label = document.getElementsByTagName("label");
var form_span = document.getElementsByTagName("span");
var form_select = document.getElementsByTagName("select");

for (var field in form_fields) {
  form_fields[field].className +=
    "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md";
}

for (var field in form_label) {
  form_label[field].className +=
    "mb-3 block text-base font-medium text-[#07074D]";
}

for (var field in form_span) {
  form_span[field].className +=
    "mt-2 block w-full px-4 py-2 text-gray-500 font-italic hover:text-Orange-400 ";
}
for (var field in form_select) {
  form_select[field].className +=
    "mt-2 block w-full rounded-md border border-gray-200 bg-white px-4 py-2 text-gray-700 placeholder-gray-400 focus:border-orange-400 focus:outline-none focus:ring focus:ring-orange-400 focus:ring-opacity-40 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300 dark:placeholder-gray-600 dark:focus:border-orange-400";
}
