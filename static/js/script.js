var form_fields = document.getElementsByTagName("input");
var form_label = document.getElementsByTagName("label");
var form_textarea = document.getElementsByTagName("textarea");
var form_option = document.getElementsByTagName("option");
var form_select = document.getElementsByTagName("select");

for (var field in form_fields) {
  form_fields[field].className +=
  "block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-red-500 focus:ring-red-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-red-500 dark:focus:ring-red-500";
}
for (var field in form_textarea) {
  form_textarea[field].className +=
  "block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-red-500 focus:ring-red-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-red-500 dark:focus:ring-red-500";
}

for (var field in form_label) {
  form_label[field].className +=
  "block mb-4 pt-4 text-sm font-medium text-gray-900 dark:text-white";
}
for (var field in form_select) {
  form_select[field].className +=
  "block inline-flex w-full items-center rounded-lg border border-gray-300 bg-gray-50 p-2.5 px-4 py-2.5 text-center text-sm font-medium text-red-600 focus:outline-none focus:ring-4 focus:ring-red-300 dark:focus:ring-red-800";
}
for (var field in form_option) {
  form_option[field].className +=
  "ml-2 text-sm font-medium text-gray-900 dark:text-gray-100 text-left";
}
